---
file_role: skill-reference
topic: preflight
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Pre-flight and post-flight (project-context v0.7.0)

This file is the authoritative specification for the pre-flight protocol and the symmetric post-flight summary introduced in v0.5.0 and extended in v0.6.0 with topology awareness, Scenario F (v0.5.0 to v0.6.0 upgrade), stale-spoke detection, and the audit trigger handler. v0.7.0 adds: the `pc-NNNN-*` recognition contract and counter-assignment logic (section 3.4), the operation-start model advisory and two-tier confirmation gate (section 4.6), the standardized set-integrity directive in post-flight (section 9.6), the generation self-consistency check (section 3.5), and Scenario G (v0.6.0 to v0.7.0 upgrade: generation/naming bump). SKILL.md's `## Protocol` section structurally gates every operation on the completion of pre-flight as defined here. Operation files (`operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`) cite this file in their pre-flight prerequisite notes.

**Two counters (v0.7.0).** The skill carries two distinct frontmatter counters. `generation` (new in schema 0.5) is the identity counter that matches the filename `pc-NNNN-*`; it is assigned at pre-flight (section 3.4) and resets to 1 on Scenario G. `update_count` (retained from schema 0.2) is the scoring lifecycle counter that drives update-based decay (`references/scoring.md`); it is preserved verbatim across all migrations and is never reset. Counter assignment in section 3.4 concerns `generation` only.

Naming: pre-flight is the dominant operation (search, classify, surface, await confirmation); post-flight is the symmetric closing block (report what was actually written). Both live in this file for protocol cohesion — they share a verdict-glyph convention, a structured-fields convention, and a "skippability is a protocol violation" rule.

## 1. Purpose

The pre-flight protocol exists because v0.4.0 shipped with a prose-described pre-flight that the model could skip under inference-time load. The 2026-05-19 postmortem (`2026-05-19-postmortem-project-context-skill-schema-mismatch.md`) documented the real-world failure mode: a stale skill zip caused an older skill version to execute against a project already running a newer schema, and the older skill happily wrote v0.1-era format records without first checking the project state. The root cause was protocol enforcement at the language level (prose instructions) rather than at the structural level (a gate the model cannot bypass).

v0.5.0 closes this gap. Pre-flight is now a structural gate: SKILL.md's `## Protocol` section is the first content after frontmatter, the model cannot reach operational content without passing through it, and the model must emit a pre-flight report block as the first content of every response before any generation. The `_managed_by: project-context-skill` field in schema "0.3" frontmatter makes pre-flight detection reliable.

## 2. The first principle

**The project's active state is authoritative. The executing skill is not.**

When the skill is invoked, it must validate against the project's existing state before performing any operation. If the project declares schema "0.3" and skill version v0.5.0, and the executing skill is an older version, the executing skill surfaces the mismatch and refuses to proceed until the operator resolves it. The executing skill never assumes correctness on the basis of being the running instance.

This principle inverts the implicit v0.4.0 assumption that the executing skill's instructions were authoritative. The postmortem failure was a direct consequence of that assumption.

Downstream implications:

| Downstream design element | Implication |
|---|---|
| Pre-flight as structural gate (section 7) | Mandatory; skill cannot proceed without validating against project. |
| Pre-flight report block (section 4) | Mandatory; validation outcome must be operator-visible. |
| Version-compatibility check (section 3) | Mandatory; schema and skill version comparison are the substance. |
| Registry marker (`_managed_by`) | Optimization for the validation lookup; makes pre-flight detection reliable. |
| Confirmation token (section 5) | Operator's acknowledgment of the validation outcome before any write. |

## 3. Pre-flight algorithm

Pre-flight is a six-step classification preceded by a four-tier search strategy. The full sequence:

### 3.1 Four-tier search strategy

The search strategy is sequential; each tier runs only if the prior returned nothing relevant. Relevance means: a `project_knowledge_search` result chunk that includes actual frontmatter signals (not merely references to the filenames or fields in some other context like recap files or design specs).

1. **Primary search:** `project_knowledge_search` for the literal `_managed_by: project-context-skill` AND `schema_version: "0.5"`.
   - **Purpose:** directly find files under skill management at the current schema.
   - **Hit signal:** chunks containing actual frontmatter with `_managed_by: project-context-skill` AND `schema_version: "0.5"` AND a `generation:` field AND a `topology:` block, on files whose names match the `pc-NNNN-{context,entities,archive}.md` pattern (the recognition contract; see section 3.5).

2. **Scenario G search (if primary returns nothing relevant):** `project_knowledge_search` for `_managed_by: project-context-skill` AND `schema_version: "0.4"`.
   - **Purpose:** find v0.6.0-managed files at schema "0.4" (old canonical names, topology present, no `generation` field, no `pc-NNNN-*` files) that need Scenario G (v0.6.0 to v0.7.0 upgrade: generation field, `pc-NNNN-*` naming, config relocation).
   - **Hit signal:** chunks containing actual frontmatter with `_managed_by: project-context-skill` AND `schema_version: "0.4"` AND a `topology:` block, on files whose names match the OLD canonical set (`project-context.md`, `entities.md`, `project-context-archive.md`), AND no `pc-NNNN-*` files are present in the inventory.

3. **Scenario F search (if primary and Scenario G both return nothing relevant):** `project_knowledge_search` for `_managed_by: project-context-skill` AND `schema_version: "0.3"`.
   - **Purpose:** find v0.5.0-managed files at schema "0.3" that need Scenario F (v0.5.0 to v0.6.0 upgrade adding topology block). After Scenario F reaches schema "0.4", the operator re-invokes and Scenario G carries the project to "0.5".
   - **Hit signal:** chunks containing actual frontmatter with `_managed_by: project-context-skill` AND `schema_version: "0.3"` AND no `topology:` block.

4. **Tertiary search (if the searches above all return nothing relevant):** `project_knowledge_search` for `schema_version: "0.2"`.
   - **Purpose:** find v0.4.0 files (no `_managed_by` marker yet, needs Scenario E upgrade migration to schema "0.3"; operator must then re-invoke for Scenario F to reach schema "0.4").
   - **Hit signal:** chunks containing frontmatter with `schema_version: "0.2"` on a file whose filename matches the canonical set (`project-context.md`, `entities.md`, `project-context-archive.md`).

5. **Quaternary search (if all searches above return nothing relevant):** legacy patterns.
   - `project_knowledge_search` for `schema_version: v0.1` (covers v0.1.x unquoted-skill-version literals).
   - File-name searches for dated legacy patterns (`*-project-context*.md`, including `-consolidated[-N]` variants).
   - **Purpose:** find v0.1-era files (Scenario D legacy migration candidates; v0.6.0 retargets legacy migration to produce schema "0.4" directly per `references/migration.md`; the operator then re-invokes for Scenario G to reach "0.5").
   - **Hit signal:** chunks containing frontmatter that matches the legacy regex `^"?v?0\.(1|2|3)(\.\d+)?"?$` per `references/migration.md`.

6. **If all searches return nothing relevant:** classify as fresh project (Scenario A or A'; see section 3.4 for counter assignment).

### 3.2 Six-step classification

From the chunks returned by the search tiers, perform classification:

1. **Parse YAML frontmatter** wherever present in the returned chunks. Identify files where the filename matches canonical or legacy patterns.
2. **Disregard chunks that merely reference the files** (e.g., recap files quoting frontmatter, design specs describing the schema). Require actual frontmatter signals — the chunk must contain a YAML document with `schema_version` or `_managed_by` as keys.
3. **Apply the six-branch classification from `references/migration.md` section 1** to each file's frontmatter:
   - `pc-NNNN-*` filename AND `_managed_by: project-context-skill` AND `schema_version: "0.5"` AND `generation` field present AND `topology` block present → CURRENT.
   - Old canonical filename (`project-context.md`, `entities.md`, `project-context-archive.md`) AND `_managed_by: project-context-skill` AND `schema_version: "0.4"` AND `topology` block present AND no `pc-NNNN-*` files present → UPGRADE_AVAILABLE_GENERATION (Scenario G: v0.6.0 to v0.7.0).
   - `_managed_by: project-context-skill` AND `schema_version: "0.3"` AND no `topology` block → UPGRADE_AVAILABLE_TOPOLOGY (Scenario F: v0.5.0 to v0.6.0).
   - Canonical filename AND `schema_version: "0.2"` AND no `_managed_by` → UPGRADE_AVAILABLE (Scenario E: v0.4.0 to v0.5.0).
   - `schema_version` matches legacy regex (not caught by above) → LEGACY.
   - Else → UNKNOWN.
4. **Identify project state** by combining per-file classifications:
   - All three `pc-NNNN-*` files CURRENT → ✓ Compatible. Apply topology validation per section 10, the generation self-consistency check per section 3.5, and (if `role: spoke-*`) stale-spoke detection per section 11.
   - All three old-canonical files UPGRADE_AVAILABLE_GENERATION → ⚠ Upgrade Available (v0.6.0 to v0.7.0). Scenario G. This is a destructive operation and gates per section 4.6.
   - All three canonical files UPGRADE_AVAILABLE_TOPOLOGY → ⚠ Upgrade Available (v0.5.0 to v0.6.0). Scenario F.
   - All three canonical files UPGRADE_AVAILABLE → ⚠ Upgrade Available. Scenario E.
   - Legacy files only → ⚠ Legacy. Scenario D.
   - Legacy AND canonical files both present → ⚠ Legacy (with migration completion guidance).
   - Some files CURRENT, others missing → ⚠ Partial State.
   - Some files UPGRADE_AVAILABLE_GENERATION, UPGRADE_AVAILABLE_TOPOLOGY, or UPGRADE_AVAILABLE, others missing → ⚠ Partial State.
   - Frontmatter present but unparseable → ✗ Parse Error.
   - Topology block present but invalid per section 10 validation rules → ✗ Parse Error (topology diagnostic).
   - A `pc-NNNN-*` filename whose `NNNN` disagrees with the frontmatter `generation` → surface the generation self-consistency diagnostic per section 3.5 (a note, not necessarily a refusal).
   - Multiple files claiming the same `file_role` at the same generation (should not occur) → ✗ Parse Error (with ambiguity diagnostic).
   - Newer schema (e.g., a "0.6" produced by a future skill version) → ✗ MISMATCH: project newer than skill.
   - Search succeeded but returned nothing → ✓ Fresh Project. Determine the counter per section 3.4 (confirmed-empty → 0001; not confirmable → prompt), then prompt operator for topology role per section 13 (LOCKED TEXT 1) before auto-proceeding.
   - Search failed (`project_knowledge_search` errored) → ✗ Infrastructure Failure.
5. **Emit the pre-flight report block** (section 4) with the verdict and operation proposal as the FIRST content of the response.
6. **Wait for operator confirmation token** (or auto-proceed if Scenario A fresh). Do not generate output, do not write to project knowledge, do not propose files until the matching token is received or auto-proceed conditions are met.

### 3.3 Scenario mapping

| Scenario | Project state | Skill state | Verdict | Operation |
|---|---|---|---|---|
| A. Fresh | No managed files; inventory confirmed empty (zero `pc-NNNN-*` files) | v0.7.0 | ✓ Fresh Project | assign counter 0001 (section 3.4); prompt operator for topology role (LOCKED TEXT 1); fresh generation at schema 0.5 writing `pc-0001-*` |
| A'. Fresh, inventory not confirmable | No readable inventory | v0.7.0 | ✓ Fresh Project (counter prompt) | prompt operator for the counter per section 3.4 (higher than highest seen); do not assume 0001; then prompt for topology role and write |
| B. Matched | `pc-NNNN-*` files at schema "0.5" with `_managed_by`, `generation`, topology block | v0.7.0 | ✓ Compatible | default / compact / rebuild (operator picks); apply topology validation, generation self-consistency (section 3.5), and (for spoke roles) stale-spoke detection |
| C. Skill-too-old | Schema "0.5" project | v0.6.x or earlier | ✗ MISMATCH | refuse; surface resolution options |
| D. Legacy | v0.1-era dated files | v0.7.0 | ⚠ Legacy | legacy migration to schema "0.4" directly; operator declares role as part of migration interview; then re-invoke for Scenario G to reach "0.5" |
| E. v0.4.0 Upgrade | Schema "0.2", no `_managed_by` | v0.7.0 | ⚠ Upgrade Available | in-place upgrade to schema "0.3"; operator re-invokes for Scenario F, then G |
| F. v0.5.0 Upgrade | Schema "0.3" with `_managed_by`, no topology block | v0.7.0 | ⚠ Upgrade Available (v0.5.0 to v0.6.0) | in-place upgrade to schema "0.4" adding topology block (unclassified default); operator declares role; then re-invoke for Scenario G |
| G. v0.6.0 Upgrade | Old canonical names, schema "0.4", topology present, no `pc-NNNN-*` files | v0.7.0 | ⚠ Upgrade Available (v0.6.0 to v0.7.0) | destructive; gates on model setup (section 4.6); token `confirm v0.7.0 upgrade`; renames to `pc-0001-*`, bumps schema to "0.5", adds `generation: 1`, preserves `update_count` and all per-record counters verbatim, carries topology verbatim, applies config treatment and relocation, instructs deletion of old-named files |

### 3.4 Counter assignment (generation identity counter; v0.7.0 NEW)

The `generation` counter is the identity counter that names the file set (`pc-NNNN-*`). It is assigned at pre-flight from the project file inventory. This section concerns `generation` only; `update_count` (the scoring counter) is never assigned here and is never reset.

**Decision table:**

| Inventory state at pre-flight | Action |
|---|---|
| Manifest readable, zero `pc-NNNN-*` files present | Start at `pc-0001`. Confirmed-fresh. |
| Manifest readable, one or more `pc-NNNN-*` sets present | Increment to the highest observed `NNNN` plus one. |
| Inventory cannot be confirmed | Prompt the operator for the number (cannot-confirm prompt below). Do NOT assume `0001`. |

**Confirmed-empty rule (enforce).** Writing `0001` is permitted ONLY on positive confirmation, via a readable manifest, that the project holds zero `pc-NNNN-*` files. Absence of evidence is not confirmation. If the inventory cannot be read, the skill prompts; it never writes `0001` on absence of evidence. A silent `0001` on a non-enumerating surface would collide with an existing `pc-0001` set and reintroduce the duplicate-canonical corruption this scheme exists to remove.

**Enumeration capability.** On Claude.ai hosted Projects the source-file manifest is provided to the skill at invocation, so the inventory is readable and web NEVER prompts: confirmed-empty writes `0001`, populated increments to highest plus one. On surfaces where the inventory cannot be read, the skill prompts. This is detect-and-react behavior, not a config gate; `config/platform-specific-parameters.md` documents `file_inventory_enumerable` per platform for operator reference only. A platform whose `file_inventory_enumerable` is `false` routes through the cannot-confirm prompt rather than a silent `0001`.

**Cannot-confirm prompt (operator-facing; verbatim form, no em or en dashes).** The skill cannot validate an operator-supplied number against existing files in the case where it must prompt, because inability to read the inventory is exactly why it is asking. The prompt therefore puts correctness in the operator's hands and instructs a number higher than the highest they see:

```
I cannot read this project's file list on this surface, so I cannot
confirm which pc-NNNN sets already exist. Open your project file list,
find the highest pc-NNNN among any project-context files, and reply with
a four-digit number higher than that highest one. If you see no pc-NNNN
files at all, reply 0001. I will write the set at the number you give.
```

There is no timestamp fallback and no per-platform `generation_identity` toggle. The operator prompt is the single fallback (locked decision W6).

### 3.5 Generation self-consistency check (v0.7.0 NEW)

For every `pc-NNNN-*` file classified CURRENT, compare the `NNNN` in the filename against the frontmatter `generation` value. They must agree.

- **Match:** no action; proceed.
- **Mismatch:** surface a diagnostic note in the pre-flight report (a `pc-MMMM-*` file carrying `generation: K` with `K != MMMM` indicates the file was hand-renamed or is stale). The note names both values and recommends the operator confirm which set is canonical. This is a diagnostic note, not an automatic refusal; the operator decides. If the mismatch makes the canonical set ambiguous (e.g., two different `NNNN` both claim to be current), escalate to `✗ Parse Error` with the ambiguity diagnostic.

The check guards against counter and `generation` drift after a hand-edit. It does not run on config files (they carry no `generation`).

## 4. Pre-flight report block format

### 4.1 Rendering rules

| Element | Choice |
|---|---|
| Format | Rendered markdown, NOT wrapped in a code block |
| Heading | `## Pre-flight Report` followed by verdict on the same line |
| Verdict glyphs | Unicode `✓` `⚠` `✗` (not emojis). All three are core Unicode and render reliably across hosted Project surfaces. |
| Placement | FIRST content emitted in the response; no preamble |
| Skippability | NEVER. Block absence is a protocol violation, not an optimization. |

### 4.2 Verdict types

| Verdict | Meaning |
|---|---|
| `✓ Compatible` | v0.7.0 project, schema "0.5", `pc-NNNN-*` names, `_managed_by` present, `generation` present, topology block present, executing skill v0.7.0 |
| `✓ Fresh Project` | No existing managed system; assign counter per section 3.4 (confirmed-empty → 0001; not confirmable → counter prompt), prompt for topology role, then proceed |
| `⚠ Legacy` | v0.1-era files detected; legacy migration available (Scenario D) |
| `⚠ Upgrade Available` | v0.4.0 schema "0.2" files detected; in-place upgrade to schema "0.3" available (Scenario E) |
| `⚠ Upgrade Available (v0.5.0 to v0.6.0)` | v0.5.0-managed schema "0.3" files detected with no topology block; in-place upgrade to schema "0.4" available (Scenario F). Informational; gates the Scenario F upgrade. |
| `⚠ Upgrade Available (v0.6.0 to v0.7.0)` | v0.6.0-managed schema "0.4" files (old canonical names, topology present, no `pc-NNNN-*` files) detected; in-place upgrade to schema "0.5" available (Scenario G: rename to `pc-0001-*`, add `generation`, relocate config). Destructive; gates on model setup per section 4.6. Token `confirm v0.7.0 upgrade`. |
| `⚠ Stale Spoke` | Informational, not blocking. On a `role: spoke-*` project, `topology.hub_version` does not match the version parsed from the attached Hub instructions filename. Operation proceeds normally; post-flight surfaces a one-line note recommending project-creator upgrade mode. |
| `⚠ Hub Source Behind` | Informational, not blocking. Rare. On a `role: spoke-*` project, the attached Hub instructions filename version is OLDER than `topology.hub_version`. Suggests the source file was not updated when the topology version was. Operation proceeds normally. |
| `⚠ Hub Source Missing` | Informational, not blocking. On a `role: spoke-*` project, no `ai-engineering-hub-instructions-v*.md` file is attached to project knowledge. Staleness comparison is skipped. Operation proceeds normally. |
| `⚠ Partial State` | Some canonical files present, others missing |
| `✗ MISMATCH: Refusing to Proceed` | Project newer than skill, or schema mismatch; refuse to write |
| `✗ Parse Error` | Frontmatter present but unparseable, OR topology block present but invalid per section 10 validation rules |
| `✗ Infrastructure Failure` | `project_knowledge_search` errored or returned nothing parseable |

### 4.3 Required fields

| Field | Purpose |
|---|---|
| Verdict (in header) | Operator's eye lands here first |
| Project name | Confirms model identified the right project |
| Existing system | Files found, schema versions, skill versions, last-update dates |
| Executing skill | Skill version currently running, with compatibility note |
| Proposing | The operation pre-flight selected based on findings |
| To proceed | Confirmation token (if required) or "Auto-proceeding" (if not) |

For `✗` verdicts, the `Proposing` field is replaced with `Issue` (diagnostic) and `Resolution options` (numbered list of operator paths).

### 4.4 Scenario examples

**Scenario A — Fresh (inventory confirmed empty):**

```
## Pre-flight Report ✓ Fresh Project

No existing managed system detected. Inventory confirmed empty (zero
pc-NNNN files). Executing skill v0.7.0. Counter assigned: 0001.
Proposing fresh generation at schema 0.5, writing pc-0001-context.md,
pc-0001-entities.md, and pc-0001-archive.md with operator-declared
topology role. The skill will prompt for the topology role declaration
(LOCKED TEXT 1 per section 13.1) before writing the three files.

**Configuration:**
- user-config.md and org-config.md read by base name from config/ (or
  project knowledge on flat web); auto-created from templates if absent.
```

**Scenario A' — Fresh (inventory not confirmable):**

```
## Pre-flight Report ✓ Fresh Project

I cannot read this project's file list on this surface, so I cannot
confirm which pc-NNNN sets already exist. Open your project file list,
find the highest pc-NNNN among any project-context files, and reply with
a four-digit number higher than that highest one. If you see no pc-NNNN
files at all, reply 0001. I will write the set at the number you give.
Executing skill v0.7.0.
```

**Scenario B — Matched:**

```
## Pre-flight Report ✓ Compatible

**Project:** [project name]
**Existing system:**
- pc-0003-context.md (schema 0.5, generation 3, _managed_by present, topology present, generated by v0.7.0, last update [date])
- pc-0003-entities.md (schema 0.5, generation 3, _managed_by present, topology present, generated by v0.7.0)
- pc-0003-archive.md (schema 0.5, generation 3, _managed_by present, topology present, generated by v0.7.0)

**Topology:** role: <declared role> (declared_by: operator)
**Executing skill:** v0.7.0 (compatible)
**Generation:** 3 (filename and frontmatter agree)
**Proposing:** default operation (merge new chat content into active records); next write is generation 4 (pc-0004-*)

**To proceed:** type `confirm merge`
```

**Scenario C — Skill-too-old:**

```
## Pre-flight Report ✗ MISMATCH: Refusing to Proceed

**Project:** [project name]
**Existing system:** pc-0003-context.md (schema 0.5, generation 3, generated by v0.7.0, topology present)
**Executing skill:** v0.6.0 (incompatible)
**Issue:** Existing project state is newer than executing skill.
  Proceeding would corrupt project data by writing v0.6.0 format records
  (schema 0.4, old canonical names, no generation field) over a v0.7.0
  schema-0.5 project.

**Resolution options:**
1. Upgrade your local skill copy to v0.7.0 (recommended)
2. Override: type `override version mismatch and proceed`
   (NOT RECOMMENDED, may corrupt project data)
```

**Scenario D — Legacy migration:**

```
## Pre-flight Report ⚠ Legacy Migration Available

**Project:** [project name]
**Existing system:** dated legacy files in v0.1-era format:
- 2026-05-08-project-context.md
- 2026-05-11-project-context.md

**Executing skill:** v0.7.0
**Proposing:** migration from legacy single-file format to three-file
  rolling architecture at schema 0.4 with operator-declared topology
  (LOCKED TEXT 1 per section 13.1 fires during the migration interview).
  After this completes, re-invoke for Scenario G to reach schema 0.5 and
  pc-NNNN naming.

**To proceed:** type `confirm migration`

Migration will produce three new files (project-context.md, entities.md,
project-context-archive.md) and provide an operator brief listing the
legacy files to delete from the project after upload-and-verify.
```

**Scenario E — v0.4.0 upgrade:**

```
## Pre-flight Report ⚠ Upgrade Available

**Project:** [project name]
**Existing system:** project-context.md, entities.md, project-context-archive.md
  (schema 0.2, generated by v0.4.0, no _managed_by field)
**Executing skill:** v0.7.0
**Proposing:** in-place upgrade to schema 0.3 (adds _managed_by marker,
  bumps schema_version, no content changes). After upgrade, re-invoke
  the skill to reach schema 0.4 via Scenario F, then schema 0.5 via
  Scenario G.

**To proceed:** type `confirm upgrade`
```

**Scenario F — v0.5.0 upgrade (v0.6.0):**

```
## Pre-flight Report ⚠ Upgrade Available (v0.5.0 to v0.6.0)

**Project:** [project name]
**Existing system:** project-context.md, entities.md, project-context-archive.md
  (schema 0.3, _managed_by present, generated by v0.5.0, no topology block)
**Executing skill:** v0.7.0
**Proposing:** in-place upgrade to schema 0.4 (adds topology metadata block
  with unclassified defaults, bumps schema_version, no content changes).
  After upgrade, operator declares topology role, then re-invokes for
  Scenario G to reach schema 0.5 and pc-NNNN naming.

**To proceed:** type `confirm v0.6.0 upgrade`
```

**Scenario G — v0.6.0 upgrade (v0.7.0 NEW):**

```
## Pre-flight Report ⚠ Upgrade Available (v0.6.0 to v0.7.0)

**Project:** [project name]
**Existing system:** project-context.md, entities.md, project-context-archive.md
  (schema 0.4, _managed_by present, topology present, generated by v0.6.0,
  no generation field, no pc-NNNN files)
**Topology:** role: <declared role> (carried verbatim)
**Executing skill:** v0.7.0

**Model setup (confirm before proceeding):** This is a destructive
  operation. Run it on the strongest thinking-capable model available on
  your platform, with extended thinking enabled. See section 4.6.

**Proposing:** in-place upgrade to schema 0.5. Renames the three files to
  pc-0001-context.md, pc-0001-entities.md, pc-0001-archive.md; adds
  generation: 1; bumps schema_version 0.4 to 0.5; preserves update_count
  and all per-record counters verbatim; carries the topology block
  verbatim; adds the config self-documenting header and bumps config
  schema to 0.5 (relocating config files to config/ on filesystem
  platforms). After upload, delete the old-named files.

**To proceed:** type `confirm v0.7.0 upgrade`
```

### 4.5 Pressure tests

| Risk | Mitigation |
|---|---|
| Operator habituation | Structured fields make confirmation tokens visually distinct; auto-proceed on Fresh removes friction where no risk exists |
| Verdict glyph rendering | All three glyphs are core Unicode, render reliably across hosted-Project surfaces |
| Project name uncertainty | Use best-available identifier; never blank |
| Token typo | Strict match (case-insensitive, whitespace-tolerant); error message reveals expected token |

### 4.6 Operation-start model advisory and two-tier confirmation gate (v0.7.0 NEW)

The model advisory and confirmation gate render in the pre-flight report block, the single operation-start chokepoint. Operations delegate report emission here and define no advisory or gate text of their own. This is the only place either renders.

**Advisory (non-blocking).** At operation start, the report names the strongest thinking-capable model for the active platform, read from `config/platform-specific-parameters.md` (`strongest_thinking_model` for the active platform), and recommends extended thinking for data integrity. The advisory is informational and never blocks.

- The skill reads the platform's `strongest_thinking_model` value and names it, e.g.: "For data integrity, run this on `<strongest_thinking_model>` with extended thinking enabled."
- **Missing-value fallback.** If the platform entry has no `strongest_thinking_model`, or the value is null, or the active platform cannot be determined, the advisory uses generic wording rather than naming a wrong model: "For data integrity, run this on the strongest thinking-capable model available on your platform, with extended thinking enabled." The skill never names a model it cannot source from the parameters file.

**Two-tier gate.** The gate is not a single global switch. Operations are tiered by destructive potential:

| Tier | Operations | Behavior |
|---|---|---|
| Routine | default, merge_external, regular compact | Advisory only; non-blocking |
| Destructive | rebuild, large compact, migration-on-detection (Scenario G) | Blocking: operator confirms model setup before the operation proceeds |

"Large compact" is a compact run that would demote a batch beyond the routine proposal cap (it surfaces the larger batch per `operations/compact.md` section 4); treat it as destructive-tier for the gate.

The blocking tier exists because the skill cannot inspect or change the active model on hosted platforms (`can_change_active_model_from_skill: false` in `config/platform-specific-parameters.md`); operator confirmation is the only available lever (principle P3). On a destructive operation, the report adds a model-setup confirmation line and the operation does not proceed until the operator confirms.

**Gate confirmation wording (operator-facing; no em or en dashes).** For destructive-tier operations other than migration, the gate uses:

```
This is a destructive operation (it can replace or demote active records).
Confirm your model setup before I proceed: run this on the strongest
thinking-capable model available on your platform, with extended thinking
enabled. Reply `confirm model setup` to proceed, or `cancel` to stop.
```

For Scenario G migration the gate is folded into the migration confirmation: the report names the model-setup recommendation (as in the Scenario G example in section 4.4) and the single token `confirm v0.7.0 upgrade` both confirms model setup and authorizes the migration. No separate `confirm model setup` step is required for migration; the migration token carries the gate.

**Read-only audit exemption.** The spoke audit trigger (section 12) emits its own read-only report block and writes nothing. It is exempt from the gate: no model-setup confirmation is required. The advisory MAY render in the audit report at most; the gate never does. See section 12.5.

## 5. Confirmation token catalog

### 5.1 Tokens by scenario

| Scenario / Operation | Token |
|---|---|
| Scenario A (fresh) | none — auto-proceeds after topology role declaration |
| Scenario B — default (merge) | `confirm merge` |
| Scenario B — compact | `confirm compact` |
| Scenario B — rebuild | `confirm rebuild` |
| Scenario D (legacy migration) | `confirm migration` |
| Scenario E (v0.4.0 upgrade) | `confirm upgrade` |
| Scenario F (v0.5.0 to v0.6.0 upgrade) | `confirm v0.6.0 upgrade` |
| Scenario G (v0.6.0 to v0.7.0 upgrade) | `confirm v0.7.0 upgrade` |
| Destructive-tier model-setup gate (rebuild, large compact) | `confirm model setup` |
| Partial state — rebuild missing | `confirm rebuild missing` |
| Partial state — treat as fresh | `confirm treat as fresh` |
| Override — version mismatch | `override version mismatch and proceed` |
| Override — parse error | `override parse error and treat as fresh` |
| Override — infrastructure failure | `override and treat as fresh` |

### 5.2 Two-tier intentional design

| Tier | Pattern | Examples |
|---|---|---|
| Normal flow | Short verb phrase: `confirm <operation>` | `confirm merge`, `confirm migration`, `confirm upgrade` |
| Override | Long phrase: `override <issue> [and proceed]` | `override version mismatch and proceed` |

The friction differential between tiers signals risk without requiring explicit warnings. Override paths are deliberately verbose; normal paths are deliberately terse.

## 6. Token matching rules

| Rule | Detail |
|---|---|
| Case | Case-insensitive: `confirm merge`, `Confirm Merge`, `CONFIRM MERGE` all match |
| Whitespace | Tolerant: leading, trailing, and intra-token extra whitespace normalized |
| Fuzzy matching | NONE. Strict equality after case-folding and whitespace normalization. Typos do not match. |
| Timeout | NONE. Operator can take any amount of time. Conversation-scoped state. |

### 6.1 Token mismatch error format

```
Token mismatch. Expected `confirm merge`. Received `confirm meege`.
Please retry with the exact token.
```

The error reveals the expected token so the operator can copy-paste. This is a UX win that mildly accelerates habituation; we accept the tradeoff because the friction is in the deliberate two-tier design (override tokens are long enough that habituation is bounded).

### 6.2 Model behavior between report and token

After emitting the pre-flight report block, the model ends its turn. The next operator message is either:

- **The matching token** → proceed with generation, then emit post-flight.
- **A non-matching token** → emit mismatch error per 6.1, end turn, wait again.
- **Something else entirely** → treat as context change; re-run pre-flight if appropriate.

The model does NOT generate output, modify state, or take any action between report emission and token receipt.

## 7. Pre-flight completion criteria

Pre-flight is considered complete when ALL THREE criteria hold:

1. `project_knowledge_search` has been executed for canonical filenames and (as needed by the tiered strategy) legacy patterns and the `_managed_by` marker.
2. Pre-flight report block has been emitted as the FIRST content of the response.
3. (Where required by verdict) Operator confirmation token has been received and exact-matched per section 6.

If ANY criterion is missing, generation must not proceed.

## 8. Infrastructure failure handling

If `project_knowledge_search` errors out or returns nothing parseable:

- Do NOT assume fresh project. The project might have state we cannot see; assuming fresh would risk the failure mode the postmortem documented.
- Emit pre-flight report with verdict `✗ Infrastructure Failure` and a diagnostic line describing what failed.
- Provide override path: `override and treat as fresh` (DESTRUCTIVE, high-friction).
- Operator decides whether to retry or override.

Anti-rationalization clause: operator urgency, perceived skill execution context, or any other condition does not license skipping pre-flight or assuming fresh on infrastructure failure. If pre-flight cannot complete, refuse to proceed and surface the failure to the operator.

## 9. Post-flight summary

Pre-flight is "here's what I am about to do." Post-flight is "here's what I actually did." The symmetry closes the audit loop: the operator can verify execution matched intent and catch discrepancies immediately.

### 9.1 Rendering rules

Mirrors pre-flight: rendered markdown, verdict glyph in heading, structured fields below.

| Element | Choice |
|---|---|
| Heading | `## Post-flight Summary` followed by verdict |
| Verdict glyphs | `✓ Complete`, `✗ Failed`, `⚠ Partial` |
| Placement | LAST structured content emitted, after file writes complete |
| Skippability | NEVER. Failure cases must still produce a post-flight summary with `✗` verdict and diagnostic. |

### 9.2 Required fields

| Field | Purpose |
|---|---|
| Verdict (in header) | Outcome at a glance |
| Files written | List of files with brief operation summary (records added/updated/etc.). Names the `pc-NNNN-*` set just written. |
| Schema | Schema version of files just written (always "0.5" for v0.7.0 writes) |
| Skill version | Version that performed the write (always "0.7.0" for v0.7.0 writes) |
| Generation | The generation `N` just written (matches the `pc-NNNN-*` names) |
| Operation performed | The operation that actually ran; flag if it diverged from pre-flight's proposal |
| Set integrity | The standardized set-integrity directive (section 9.6), rendered unconditionally on every successful write |
| Operator action required | Only when migration produces old-named files to delete or other follow-up needed |
| Token state | Active file's position relative to soft ceiling (informational) |

### 9.3 Scenario examples

**Scenario A — Fresh:**

```
## Post-flight Summary ✓ Complete

**Files written:**
- pc-0001-context.md (fresh generation, 8 records, role: <declared>)
- pc-0001-entities.md (fresh generation, 3 entities)
- pc-0001-archive.md (fresh generation, empty)

**Schema:** 0.5
**Skill version:** 0.7.0
**Generation:** 1
**Operation performed:** fresh generation with topology declaration

**Set integrity:** Replace, do not duplicate. The current canonical set is
pc-0001-context.md, pc-0001-entities.md, and pc-0001-archive.md at
generation 1. After you upload this set, delete any prior pc-MMMM-* set
with a lower counter. Do not upload the same generation twice; a same-name
duplicate can fail the next pre-flight.
```

**Scenario B — Matched, default merge:**

```
## Post-flight Summary ✓ Complete

**Files written:**
- pc-0004-context.md (3 records added, 2 updated, 0 demoted, 0 superseded)
- pc-0004-entities.md (1 entity added, 0 updated)
- pc-0004-archive.md (1 record appended via supersession)

**Schema:** 0.5
**Skill version:** 0.7.0
**Generation:** 4 (update_count also incremented; it is the separate scoring counter)
**Operation performed:** default (merge)

**Set integrity:** Replace, do not duplicate. The current canonical set is
pc-0004-context.md, pc-0004-entities.md, and pc-0004-archive.md at
generation 4. After you upload this set, delete any prior pc-MMMM-* set
with a lower counter. Do not upload the same generation twice; a same-name
duplicate can fail the next pre-flight.

Active file at 23% of soft token ceiling (15.4K / 50K).
```

**Scenario D — Legacy migration:**

```
## Post-flight Summary ✓ Migration Complete

**Files written (new schema 0.4 format, old canonical names):**
- project-context.md
- entities.md
- project-context-archive.md

**Skill version:** 0.7.0
**Operation performed:** legacy migration with topology declaration
**Next step:** re-invoke for Scenario G to reach schema 0.5 and pc-NNNN naming.

**Operator action required:** delete the following legacy files from the
project after verifying the new files have uploaded correctly:
- 2026-05-08-project-context.md
- 2026-05-11-project-context.md
```

**Scenario E — v0.4.0 upgrade:**

```
## Post-flight Summary ✓ Upgrade Complete

**Files upgraded to schema 0.3:**
- project-context.md (added _managed_by marker, bumped schema_version)
- entities.md (added _managed_by marker, bumped schema_version)
- project-context-archive.md (added _managed_by marker, bumped schema_version)

**Skill version:** 0.7.0
**Records:** preserved unchanged (no content modifications, only schema upgrade)
**Operation performed:** in-place schema upgrade

**Operator action required:** re-invoke the skill to reach schema 0.4 via
Scenario F (adds topology block), then schema 0.5 via Scenario G.
```

**Scenario F — v0.5.0 to v0.6.0 upgrade (v0.6.0 NEW):**

```
## Post-flight Summary ✓ Upgrade Complete (v0.5.0 to v0.6.0)

**Files upgraded to schema 0.4:**
- project-context.md (added topology block with unclassified default,
  bumped schema_version from 0.3 to 0.4)
- entities.md (added topology block with unclassified default,
  bumped schema_version from 0.3 to 0.4)
- project-context-archive.md (added topology block with unclassified
  default, bumped schema_version from 0.3 to 0.4)

**Skill version:** 0.7.0
**Records:** preserved unchanged (no content modifications, only schema
  upgrade and topology block addition)
**Operation performed:** in-place schema upgrade to 0.4 with unclassified
  topology default

**Topology:** defaults to 'unclassified'; declare role to complete migration.

**Operator action required:** declare topology role to complete migration.
  The skill will prompt with the role-declaration prompt (section 13). Then
  re-invoke for Scenario G to reach schema 0.5 and pc-NNNN naming.
```

**Scenario G — v0.6.0 to v0.7.0 upgrade (v0.7.0 NEW):**

```
## Post-flight Summary ✓ Upgrade Complete (v0.6.0 to v0.7.0)

**Files written (schema 0.5, renamed):**
- pc-0001-context.md   (was project-context.md)
- pc-0001-entities.md  (was entities.md)
- pc-0001-archive.md   (was project-context-archive.md)

**Schema:** 0.5
**Skill version:** 0.7.0
**Generation:** 1 (identity counter reset to 1)
**Records:** preserved unchanged. update_count and all per-record counters
  (first_seen_update, last_seen_update, times_seen) preserved verbatim;
  only generation (new) and the schema_version literal changed. Topology
  block carried verbatim.
**Config:** user-config.md, org-config.md, platform-specific-parameters.md
  received the config_editable/configure_with header and a schema bump to
  0.5; relocated to config/ on filesystem platforms (no-op at the read
  layer on flat web).
**Operation performed:** in-place generation/naming upgrade

**Set integrity:** Replace, do not duplicate. The current canonical set is
pc-0001-context.md, pc-0001-entities.md, and pc-0001-archive.md at
generation 1. After you upload this set, delete any prior pc-MMMM-* set
with a lower counter. Do not upload the same generation twice; a same-name
duplicate can fail the next pre-flight.

**Operator action required:** after you have uploaded the pc-0001-* set and
verified it, delete the old-named files now superseded by it:
- project-context.md
- entities.md
- project-context-archive.md
```

### 9.4 Failure handling

If file writes fail:

- Post-flight still emits with `✗ Failed` verdict.
- Diagnostic includes which writes succeeded, which failed, and the failure reason if known.
- Operator instructions for partial-state recovery (e.g., re-run upgrade migration; idempotency in `references/migration.md` section 9.7 handles already-upgraded files).

### 9.5 Deviation reporting

If the operation performed differs from the operation pre-flight proposed (rare, but possible if execution finds something pre-flight missed):

```
## Post-flight Summary ✓ Complete (with deviation)

**Operation performed:** legacy migration
**Note:** pre-flight proposed default merge; execution discovered legacy
files in the project not surfaced by initial search and switched to
migration. See file-writes list for full account.

[rest of summary as normal]
```

The deviation note is mandatory whenever execution diverges from the pre-flight proposal. Silent deviation is a protocol violation.

### 9.6 Set-integrity directive (v0.7.0 NEW; canonical single source)

This is the single canonical source of the set-integrity directive. The post-flight summary renders it on every successful write (it is the `Set integrity` field in section 9.2). Operation files do NOT inline their own replace wording; they reference this directive (see `operations/default.md`, `merge_external.md`, `compact.md`, `rebuild.md`). This avoids the per-operation wording drift that existed before v0.7.0.

**Canonical directive string (no em or en dashes):**

```
Replace, do not duplicate. The current canonical set is pc-NNNN-context.md,
pc-NNNN-entities.md, and pc-NNNN-archive.md at generation N. After you upload
this set, delete any prior pc-MMMM-* set with a lower counter. Do not upload the
same generation twice; a same-name duplicate can fail the next pre-flight.
```

When rendering, substitute the actual `NNNN` (the generation just written) for `NNNN` and `N`. The directive is **standalone and unconditional**: it always names all three files of the current generation, regardless of which files changed this run.

**Relationship to the change-aware brief.** Two channels, do not conflate them:

- The operator brief (in each operation file) lists only the files that changed this run and marks unchanged files with its existing `ℹ` indicator. That behavior is unchanged in v0.7.0; do not regress it.
- This set-integrity line states which generation is canonical, naming all three files unconditionally.

The brief says what changed this run; the set-integrity line says which generation is canonical and what to prune. With versioned names the common failure mode shifts from same-name collision to generation accumulation, resolved by highest-counter-wins plus this prune instruction.

## 10. Topology validation (v0.6.0)

After classification identifies a `✓ Compatible` verdict, pre-flight applies topology validation to the project's `pc-NNNN-context.md` frontmatter (the active context file of the current generation). The authoritative schema, role definitions, and validation rules live in `references/topology.md`; this section specifies how pre-flight applies them.

### 10.1 Validation sequence

The validation rules themselves (role enum, declared_by enum, ISO 8601 timestamps, required-by-role fields, no-empty-fields) are specified canonically in `references/topology.md` section 6. Pre-flight applies those rules; it does not redefine them. This section specifies the application behavior — what pre-flight does at each step and what it emits on success or failure.

1. **Parse the topology block** from `pc-NNNN-context.md` frontmatter. If the block is absent on a schema 0.5 file, this is a Parse Error (schema 0.5 requires the topology block, carried verbatim from 0.4, per `references/topology.md` section 6).
2. **Validate `role`** against the enum specified in `references/topology.md` section 6.3. Any deviation is a Parse Error.
3. **Validate `declared_by`** against the enum specified in `references/topology.md` section 6.5. Any deviation is a Parse Error.
4. **Validate `declared_at`** as ISO 8601 per `references/topology.md` section 6.4. Any deviation is a Parse Error.
5. **Apply required-by-role rules** per `references/topology.md` section 6.1 (the per-role required-non-null and required-null field matrix lives there). Any violation is a Parse Error.
6. **Apply the no-empty-fields rule** per `references/topology.md` section 6.2. On violation, emit the Parse Error message specified in topology.md section 6.2: "Topology field `<field>` is empty; expected confident value, explicit placeholder, or null with reason."
7. **For `role: spoke-*` projects:** proceed to stale-spoke detection (section 11).
8. **For `role: unclassified` projects:** emit a follow-up prompt with LOCKED TEXT 1 (section 13) on each invocation until the operator declares a role.

### 10.2 Validation failure

If any validation step fails, pre-flight emits `✗ Parse Error` with a topology diagnostic and refuses the proposed operation. The diagnostic names the offending field and the rule that failed. Operator paths:
- Repair the topology block in `pc-NNNN-context.md` and re-invoke.
- Override path: `override parse error and treat as fresh` (DESTRUCTIVE; loses topology context).

### 10.3 Validation success

A valid topology block enables downstream behaviors:
- For `role: hub`: enables the audit trigger handler (section 12).
- For `role: spoke-*`: invokes stale-spoke detection (section 11).
- For `role: standalone` and `role: unclassified`: no additional pre-flight processing beyond standard verdict emission.

## 11. Stale-spoke detection (v0.6.0 NEW)

Stale-spoke detection runs on `role: spoke-*` projects after topology validation succeeds. It compares the spoke's declared Hub version against the attached Hub instructions file and emits one of three informational verdicts. None of the three blocks the proposed operation; they are informational signals to the operator.

### 11.1 Detection algorithm

1. **Read `topology.hub_version`** from `pc-NNNN-context.md` frontmatter (e.g., `"v0.9"`).
2. **Search project knowledge** for files matching the pattern `ai-engineering-hub-instructions-v*.md`. Use `project_knowledge_search` with the filename pattern.
3. **Parse the version** from the filename of the most recently attached match. Convention: `ai-engineering-hub-instructions-v0-9.md` parses to `v0.9` (dash separator in filename normalizes to dot in version string).
4. **Compare versions** using semantic version arithmetic on minor/patch components:
   - File version equals `topology.hub_version` → no informational verdict; proceed silently.
   - File version is newer than `topology.hub_version` → emit `⚠ Stale Spoke`.
   - File version is older than `topology.hub_version` → emit `⚠ Hub Source Behind` (rare).
5. **If no Hub instructions file is attached:** emit `⚠ Hub Source Missing`.

### 11.2 Verdict block format

When a stale-spoke informational verdict fires, the pre-flight report includes these additional structured fields immediately under the standard pre-flight report fields:

```
**Hub reference:** <topology.hub_reference>
**Spoke source-version:** <topology.hub_version>
**Attached Hub file version:** <parsed from filename, or "(no file attached)">
**Sync state:** stale (recommend project-creator upgrade mode) | hub source behind | hub source missing
```

### 11.3 Post-flight one-liner

When a `⚠ Stale Spoke` verdict fires and the operation proceeds, post-flight appends a one-line note:

```
**Spoke sync:** Spoke is at <topology.hub_version>; current Hub version is <file version>.
  Consider running project-creator upgrade mode.
```

The skill never auto-upgrades the Hub reference. The upgrade flow lives in the project-creator skill (Workstream 3).

### 11.4 Severity classification

The skill reports drift without severity. A spoke 4 minor versions behind and a spoke 1 minor version behind both render as `⚠ Stale Spoke` with their respective version stamps. Operators decide priority. Future releases may add severity thresholds; the skill does not pre-empt that design.

## 12. Audit trigger handler (v0.6.0 NEW)

The audit trigger is a read-only operation invokable in Hub projects only. It produces a staleness report comparing each spoke's source Hub version against the current Hub instructions file version. The trigger does not modify project files.

### 12.1 Trigger phrases

The skill matches any of these phrases (case-insensitive, whitespace-tolerant) in the operator's invocation:

- `audit spoke projects`
- `audit the spokes`
- `which spokes are stale`
- `show me spoke staleness`
- `spoke inventory audit`
- `run spoke audit`

### 12.2 Pre-flight gate

When pre-flight detects an audit trigger phrase, the gate runs before any read of project knowledge beyond the topology validation:

1. Validate the current project's `topology.role`.
2. **If `role: hub`:** proceed to audit execution (section 12.3).
3. **If `role` is any other value (spoke-dev, spoke-solution, standalone, unclassified):** emit the refusal message verbatim:

   ```
   Audit trigger valid only in Hub projects.
   ```

   End the turn. No further operation runs.

### 12.3 Audit execution

1. **Read the spoke inventory** from the body of `pc-NNNN-context.md` (section `## Spoke Inventory` per `references/topology.md` section 3).
2. **Parse the current Hub instructions version** from the filename of an attached `ai-engineering-hub-instructions-v*.md` file. If absent, render the audit report with a placeholder note in place of the current version and emit the inventory rows without Status comparison.
3. **For each spoke row:** compare the `Source Hub Version` cell against the parsed current Hub version.
   - Match → Status `current`.
   - Mismatch (file newer) → Status `STALE`. Compute drift expression on minor/major arithmetic.
4. **Sort:** STALE spokes alphabetical, then current spokes alphabetical.
5. **Emit the audit report block** per `references/topology.md` section 4.4.

### 12.4 Audit is read-only

The audit trigger does not write to `pc-NNNN-context.md`. The Status column in the persistent spoke inventory is operator-maintained between audits. A future trigger (`refresh spoke inventory`, out of scope for v0.7.0) will own write-back.

The audit trigger does not invoke upgrades. The project-creator skill's upgrade mode (Workstream 3) owns the upgrade flow.

### 12.5 Audit report format and gate exemption

See `references/topology.md` section 4.4 for the full audit report block format. Pre-flight emits the audit report block in place of the standard pre-flight report block when the audit trigger fires; the post-flight summary is omitted (audit is read-only, nothing was written).

**Gate exemption (v0.7.0).** Because the audit trigger writes nothing, it is exempt from the two-tier model-setup gate in section 4.6. No model-setup confirmation is required to run an audit. The model advisory MAY render in the audit report (informational); the blocking gate never does. This exemption is specific to the read-only audit; every write-producing operation remains subject to its tier in section 4.6.

## 13. Role-declaration prompts (v0.6.0 NEW)

When the skill needs the operator to declare a topology role — fresh project (Scenario A) or after Scenario F upgrade — it emits a role-declaration prompt. Two locked-text prompts apply to specific situations. The skill may prepend scenario-specific framing (e.g., "Setting up a fresh project." or "Topology defaults to unclassified after upgrade.") before each locked prompt.

### 13.1 LOCKED TEXT 1 — Role declaration

Emit verbatim in Scenario A upfront role solicitation and in Scenario F follow-up role solicitation:

```
Declare this project's topology role to enable correct semantics
for audit, migration, and governance. Options: hub (owns a spoke
inventory), spoke-dev (a development artifact like a skill
referencing a hub), spoke-solution (a delivered solution
referencing a hub), or standalone (no hub relationship). Reply
with the role name.
```

The prompt is not paraphrased. The four operator-selectable role values (`hub`, `spoke-dev`, `spoke-solution`, `standalone`) must remain in the order shown. The fifth role value `unclassified` is the skill-default that fires when the operator does not declare; the skill never offers `unclassified` as an option in this prompt. The skill never declares a role on the operator's behalf; it waits for the operator's reply.

### 13.2 LOCKED TEXT 2 — Missing hub_reference

Emit verbatim when an operator declares `role: spoke-dev` or `role: spoke-solution` but does not provide `hub_reference` and `hub_version`:

```
Spoke roles require hub_reference and hub_version. Reply with
both: the hub project name and the current hub instructions
version, e.g., "AI Engineering Hub, v0.9".
```

The example in the prompt is canonical and must be preserved as-is. The skill does not infer hub_reference from project metadata; it asks.

### 13.3 Role-declaration parsing

When the operator replies with a role declaration, the skill:

1. Parse the role from the operator's reply. Accept any of: `hub`, `spoke-dev`, `spoke-solution`, `standalone`. Case-insensitive.
2. If the parsed role is `spoke-dev` or `spoke-solution` and the reply does not include hub_reference and hub_version, emit LOCKED TEXT 2 and wait again.
3. If the parsed role is `hub`: write `role: hub` to `topology.role` with `declared_by: "operator"` and `declared_at: <current ISO 8601>`. Create an empty `## Spoke Inventory` section in the body of `pc-NNNN-context.md` immediately after the frontmatter per `references/topology.md` section 3.
4. If the parsed role is `spoke-dev` or `spoke-solution`: write `role`, `hub_reference`, `hub_version`, set `last_hub_sync` to current timestamp, `declared_by: "operator"`, `declared_at: <current ISO 8601>`.
5. If the parsed role is `standalone`: write `role: standalone` with all relationship fields null, `declared_by: "operator"`, `declared_at: <current ISO 8601>`.
6. If the operator declines or does not respond: leave topology as `unclassified`. The skill prompts again on next invocation.

The skill never writes a partial spoke topology. If hub_reference or hub_version is missing for a declared spoke role, LOCKED TEXT 2 fires until both are provided.

## 14. Cross-references

- Schema definition and validation (schema 0.5, generation, naming contract, config-file frontmatter): `references/schema.md`.
- Schema-changelog and Supported Schemas matrix: `references/schema-changelog.md`.
- Migration paths (legacy Scenario D, v0.4.0 upgrade Scenario E, v0.5.0 to v0.6.0 upgrade Scenario F, v0.6.0 to v0.7.0 upgrade Scenario G): `references/migration.md`.
- Per-platform `strongest_thinking_model`, `can_change_active_model_from_skill`, `file_inventory_enumerable`, `config_read_location` (read by the advisory and counter logic): `config/platform-specific-parameters.md`.
- Config interview mechanics and the config/references separation: `references/configure.md`.
- Topology metadata schema, role definitions, spoke inventory format, audit trigger semantics, hybrid topology rules, validation rules: `references/topology.md`.
- Operation-level pre-flight prerequisite notes: `operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`.
- SKILL.md `## Protocol` section: the structural gate that cites this file.
- The release-trigger postmortem documenting the v0.4.0 protocol-enforcement gap: `2026-05-19-postmortem-project-context-skill-schema-mismatch.md` (in the v0.5.0 build inputs).
