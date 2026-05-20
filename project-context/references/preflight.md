---
file_role: skill-reference
topic: preflight
schema_version_documented: "0.3"
skill_version: "0.5.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Pre-flight and post-flight (project-context v0.5.0)

This file is the authoritative specification for the pre-flight protocol and the symmetric post-flight summary introduced in v0.5.0. SKILL.md's `## Protocol` section structurally gates every operation on the completion of pre-flight as defined here. Operation files (`operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`) cite this file in their pre-flight prerequisite notes.

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

Pre-flight is a six-step classification preceded by a three-tier search strategy. The full sequence:

### 3.1 Three-tier search strategy

The search strategy is sequential; each tier runs only if the prior returned nothing relevant. Relevance means: a `project_knowledge_search` result chunk that includes actual frontmatter signals (not merely references to the filenames or fields in some other context like recap files or design specs).

1. **Primary search:** `project_knowledge_search` for the literal `_managed_by: project-context-skill`.
   - **Purpose:** directly find files under skill management at schema "0.3".
   - **Hit signal:** chunks containing actual frontmatter with this field present and `schema_version: "0.3"` nearby.

2. **Secondary search (if primary returns nothing relevant):** `project_knowledge_search` for `schema_version: "0.2"`.
   - **Purpose:** find v0.4.0 files (no `_managed_by` marker yet, needs upgrade migration).
   - **Hit signal:** chunks containing frontmatter with `schema_version: "0.2"` on a file whose filename matches the canonical set (`project-context.md`, `entities.md`, `project-context-archive.md`).

3. **Tertiary search (if primary and secondary both return nothing relevant):** legacy patterns.
   - `project_knowledge_search` for `schema_version: v0.1` (covers v0.1.x unquoted-skill-version literals).
   - File-name searches for dated legacy patterns (`*-project-context*.md`, including `-consolidated[-N]` variants).
   - **Purpose:** find v0.1-era files (legacy migration candidates).
   - **Hit signal:** chunks containing frontmatter that matches the legacy regex `^"?v?0\.(1|2|3)(\.\d+)?"?$` per `references/migration.md`.

4. **If all three searches return nothing relevant:** classify as fresh project.

### 3.2 Six-step classification

From the chunks returned by the search tiers, perform classification:

1. **Parse YAML frontmatter** wherever present in the returned chunks. Identify files where the filename matches canonical or legacy patterns.
2. **Disregard chunks that merely reference the files** (e.g., recap files quoting frontmatter, design specs describing the schema). Require actual frontmatter signals — the chunk must contain a YAML document with `schema_version` or `_managed_by` as keys.
3. **Apply the four-branch classification from `references/migration.md` section 1** to each file's frontmatter:
   - `_managed_by: project-context-skill` AND `schema_version: "0.3"` → CURRENT.
   - Canonical filename AND `schema_version: "0.2"` AND no `_managed_by` → UPGRADE_AVAILABLE.
   - `schema_version` matches legacy regex (not caught by above) → LEGACY.
   - Else → UNKNOWN.
4. **Identify project state** by combining per-file classifications:
   - All three canonical files CURRENT → ✓ Compatible.
   - All three canonical files UPGRADE_AVAILABLE → ⚠ Upgrade Available.
   - Legacy files only → ⚠ Legacy.
   - Legacy AND canonical files both present → ⚠ Legacy (with migration completion guidance).
   - Some canonical files CURRENT, others missing → ⚠ Partial State.
   - Some canonical files UPGRADE_AVAILABLE, others missing → ⚠ Partial State.
   - Frontmatter present but unparseable → ✗ Parse Error.
   - Multiple canonical-name files (should not occur) → ✗ Parse Error (with ambiguity diagnostic).
   - Newer schema (e.g., a "0.4" produced by a future skill version) → ✗ MISMATCH: project newer than skill.
   - Search succeeded but returned nothing → ✓ Fresh Project.
   - Search failed (`project_knowledge_search` errored) → ✗ Infrastructure Failure.
5. **Emit the pre-flight report block** (section 4) with the verdict and operation proposal as the FIRST content of the response.
6. **Wait for operator confirmation token** (or auto-proceed if Scenario A fresh). Do not generate output, do not write to project knowledge, do not propose files until the matching token is received or auto-proceed conditions are met.

### 3.3 Scenario mapping

| Scenario | Project state | Skill state | Verdict | Operation |
|---|---|---|---|---|
| A. Fresh | No project-context files | v0.5.0 | ✓ Fresh Project | fresh generation, auto-proceeds |
| B. Matched | Schema "0.3" with `_managed_by` | v0.5.0 | ✓ Compatible | default / compact / rebuild (operator picks) |
| C. Skill-too-old | Schema "0.3" project | v0.4.x or earlier | ✗ MISMATCH | refuse; surface resolution options |
| D. Legacy | v0.1-era dated files | v0.5.0 | ⚠ Legacy | legacy migration to schema "0.3" |
| E. v0.4.0 Upgrade | Schema "0.2", no `_managed_by` | v0.5.0 | ⚠ Upgrade Available | in-place upgrade to schema "0.3" |

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
| `✓ Compatible` | v0.5.0 project, schema "0.3", `_managed_by` present, executing skill v0.5.0 |
| `✓ Fresh Project` | No existing project-context system; safe to auto-proceed |
| `⚠ Legacy` | v0.1-era files detected; legacy migration available |
| `⚠ Upgrade Available` | v0.4.0 schema "0.2" files detected; in-place upgrade available |
| `⚠ Partial State` | Some canonical files present, others missing |
| `✗ MISMATCH: Refusing to Proceed` | Project newer than skill, or schema mismatch; refuse to write |
| `✗ Parse Error` | Frontmatter present but unparseable |
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

**Scenario A — Fresh:**

```
## Pre-flight Report ✓ Fresh Project

No existing project-context system detected. Executing skill v0.5.0.
Proposing fresh generation. Auto-proceeding.
```

**Scenario B — Matched:**

```
## Pre-flight Report ✓ Compatible

**Project:** [project name]
**Existing system:**
- project-context.md (schema 0.3, _managed_by present, generated by v0.5.0, last update [date])
- entities.md (schema 0.3, _managed_by present, generated by v0.5.0)
- project-context-archive.md (schema 0.3, _managed_by present, generated by v0.5.0)

**Executing skill:** v0.5.0 (compatible)
**Proposing:** default operation (merge new chat content into active records)

**To proceed:** type `confirm merge`
```

**Scenario C — Skill-too-old:**

```
## Pre-flight Report ✗ MISMATCH: Refusing to Proceed

**Project:** [project name]
**Existing system:** project-context.md (schema 0.3, generated by v0.5.0)
**Executing skill:** v0.4.0 (incompatible)
**Issue:** Existing project state is newer than executing skill.
  Proceeding would corrupt project data by writing v0.4.0 format records
  over v0.5.0 schema.

**Resolution options:**
1. Upgrade your local skill copy to v0.5.0 (recommended)
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

**Executing skill:** v0.5.0
**Proposing:** migration from legacy single-file format to three-file
  rolling architecture at schema 0.3

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
**Executing skill:** v0.5.0
**Proposing:** in-place upgrade to schema 0.3 (adds _managed_by marker,
  bumps schema_version, no content changes)

**To proceed:** type `confirm upgrade`
```

### 4.5 Pressure tests

| Risk | Mitigation |
|---|---|
| Operator habituation | Structured fields make confirmation tokens visually distinct; auto-proceed on Fresh removes friction where no risk exists |
| Verdict glyph rendering | All three glyphs are core Unicode, render reliably across hosted-Project surfaces |
| Project name uncertainty | Use best-available identifier; never blank |
| Token typo | Strict match (case-insensitive, whitespace-tolerant); error message reveals expected token |

## 5. Confirmation token catalog

### 5.1 Tokens by scenario

| Scenario / Operation | Token |
|---|---|
| Scenario A (fresh) | none — auto-proceeds |
| Scenario B — default (merge) | `confirm merge` |
| Scenario B — compact | `confirm compact` |
| Scenario B — rebuild | `confirm rebuild` |
| Scenario D (legacy migration) | `confirm migration` |
| Scenario E (v0.4.0 upgrade) | `confirm upgrade` |
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
| Files written | List of files with brief operation summary (records added/updated/etc.) |
| Schema | Schema version of files just written (always "0.3" for v0.5.0 writes) |
| Skill version | Version that performed the write (always "0.5.0" for v0.5.0 writes) |
| Operation performed | The operation that actually ran; flag if it diverged from pre-flight's proposal |
| Operator action required | Only when migration produces legacy files to delete or other follow-up needed |
| Token state | Active file's position relative to soft ceiling (informational) |

### 9.3 Scenario examples

**Scenario A — Fresh:**

```
## Post-flight Summary ✓ Complete

**Files written:**
- project-context.md (fresh generation, 8 records)
- entities.md (fresh generation, 3 entities)
- project-context-archive.md (fresh generation, empty)

**Schema:** 0.3
**Skill version:** 0.5.0
**Operation performed:** fresh generation
```

**Scenario B — Matched, default merge:**

```
## Post-flight Summary ✓ Complete

**Files written:**
- project-context.md (3 records added, 2 updated, 0 demoted, 0 superseded)
- entities.md (1 entity added, 0 updated)
- project-context-archive.md (1 record appended via supersession)

**Schema:** 0.3
**Skill version:** 0.5.0
**Operation performed:** default (merge)

Active file at 23% of soft token ceiling (15.4K / 50K).
```

**Scenario D — Legacy migration:**

```
## Post-flight Summary ✓ Migration Complete

**Files written (new schema 0.3 format):**
- project-context.md
- entities.md
- project-context-archive.md

**Skill version:** 0.5.0
**Operation performed:** legacy migration

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

**Skill version:** 0.5.0
**Records:** preserved unchanged (no content modifications, only schema upgrade)
**Operation performed:** in-place schema upgrade
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

## 10. Cross-references

- Schema definition and validation: `references/schema.md`.
- Schema-changelog and Supported Schemas matrix: `references/schema-changelog.md`.
- Migration paths (legacy and upgrade): `references/migration.md`.
- Operation-level pre-flight prerequisite notes: `operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`.
- SKILL.md `## Protocol` section: the structural gate that cites this file.
- The release-trigger postmortem documenting the v0.4.0 protocol-enforcement gap: `2026-05-19-postmortem-project-context-skill-schema-mismatch.md` (in the v0.5.0 build inputs).
