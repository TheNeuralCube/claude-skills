---
file_role: skill-reference
topic: migration
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Migration (project-context v0.7.0)

This file documents the four migration paths the skill supports:

1. **Legacy migration** (schema "0.1" → "0.4" via Scenario D): one-time, per-project, from the v0.1-era schema used by skill versions v0.1.0 through v0.3.2. v0.6.0 retargets legacy migration to produce schema "0.4" directly; operators with v0.1-era projects skip schemas "0.2" and "0.3". The operator declares topology role as part of the migration interview. After Scenario D, the operator re-invokes for Scenario G to reach schema "0.5" and `pc-NNNN` naming. See sections 1 to 8.
2. **Upgrade migration** (schema "0.2" → "0.3" via Scenario E): one-time, per-project, in-place upgrade from the v0.4.0 schema "0.2" to schema "0.3". Adds the REQUIRED `_managed_by` field; preserves all other content unchanged. After Scenario E, operators re-invoke for Scenario F, then G. See section 9.
3. **Topology upgrade migration** (schema "0.3" → "0.4" via Scenario F): one-time, per-project, in-place upgrade from the v0.5.0 schema "0.3" to schema "0.4". Adds the REQUIRED topology block (with `role: unclassified` default); preserves all other content unchanged. The operator declares topology role in a follow-up exchange, then re-invokes for Scenario G. See section 10.
4. **Generation/naming upgrade migration** (schema "0.4" → "0.5" via Scenario G, v0.7.0 NEW): one-time, per-project, in-place upgrade from the v0.6.0 schema "0.4" to the current schema "0.5". Renames the three files to `pc-0001-{context,entities,archive}.md`, adds the REQUIRED `generation` field (= 1), RETAINS `update_count` and all per-record counters verbatim, carries the topology block verbatim, and applies the config treatment (header + relocation). This is a destructive operation and gates on model setup per `references/preflight.md` section 4.6. See section 11.

**Two counters (v0.7.0).** Scenario G adds `generation` (identity, resets to 1) and preserves `update_count` (scoring lifecycle, never reset). The two are distinct; see `references/schema.md`. No migration ever resets `update_count` or any per-record `*_update` field.

Pre-flight (per `references/preflight.md`) classifies the project's state and routes to the right migration path. This file is the algorithm pre-flight cites for the write phase.

For the history of what was actually written under "0.1", including the unquoted-skill-version-as-schema_version accident, see `references/schema-changelog.md`. For the cross-version compatibility matrix (what the skill reads, writes, migrates from, refuses), see the "Supported Schemas" section of `references/schema-changelog.md`.

## 1. Detection

Pre-flight scans the project for files matching any of:

- The current `pc-NNNN-*` filenames: `pc-NNNN-context.md`, `pc-NNNN-entities.md`, `pc-NNNN-archive.md` (v0.7.0, schema 0.5).
- The old canonical project-context filenames: `project-context.md`, `entities.md`, `project-context-archive.md` (introduced in v0.4.0, used through v0.6.0; now the detection signal and source filenames for Scenarios E, F, and G).
- The legacy filename pattern: `*-project-context*.md` (dated, optionally topic-suffixed, including `-consolidated[-N]` variants).
- A `file_type: project-context` value in the YAML frontmatter.

For every match, parse the frontmatter and run the **six-branch classification** below, in this exact order. The branch ordering is significant: the `_managed_by` requirement in step 1 is the explicit disambiguator that distinguishes the current marker from any legacy literal the broad regex (step 5) would otherwise match. Step 2 (Scenario G detection) sits directly below the current branch because v0.6.0-managed schema-0.4 files share the `_managed_by` marker and topology block with v0.7.0 currents but differ on schema version, the `generation` field, and the filename pattern. Step 3 (Scenario F detection) sits below Scenario G because v0.5.0-managed files share `_managed_by` but lack the topology block.

**Step 1 — Current-schema (v0.7.0).** If the file has a `pc-NNNN-*` filename AND ALL of `_managed_by: project-context-skill` AND `schema_version: "0.5"` AND a `generation` field AND a `topology` block in frontmatter, the file is a v0.7.0 current-schema file. Skip migration; pre-flight classifies as `✓ Compatible` and proceeds with normal operation per `references/preflight.md` (which also applies topology validation per its section 10 and the generation self-consistency check per its section 3.5). Do NOT evaluate later steps.

**Step 2 — Generation-upgrade-available (v0.6.0 → v0.7.0, Scenario G).** If the file has an OLD canonical filename (`project-context.md`, `entities.md`, `project-context-archive.md`) AND `_managed_by: project-context-skill` AND `schema_version: "0.4"` AND a `topology` block AND there are no `pc-NNNN-*` files present, the file is a v0.6.0-managed schema-0.4 file eligible for in-place upgrade to schema "0.5". Pre-flight classifies as `⚠ Upgrade Available (v0.6.0 to v0.7.0)` and routes to the generation/naming upgrade migration in section 11. This is a destructive operation and gates on model setup per `references/preflight.md` section 4.6. Operator confirmation token: `confirm v0.7.0 upgrade`. Do NOT evaluate later steps for this file.

**Step 3 — Topology-upgrade-available (v0.5.0 → v0.6.0, Scenario F).** If the file has `_managed_by: project-context-skill` AND `schema_version: "0.3"` AND no `topology` block, the file is a v0.5.0-managed schema-0.3 file eligible for in-place upgrade to schema "0.4". Pre-flight classifies as `⚠ Upgrade Available (v0.5.0 to v0.6.0)` and routes to the topology-upgrade migration in section 10. Operator confirmation token: `confirm v0.6.0 upgrade`. After section 10 completes, the operator re-invokes for Scenario G. Do NOT evaluate later steps for this file.

**Step 4 — Upgrade-available (v0.4.0 → v0.5.0).** If the file has a canonical project-context filename AND `schema_version: "0.2"` (the v0.4.0 literal) AND no `_managed_by` field, the file is a v0.4.0 schema-0.2 file eligible for in-place upgrade. Pre-flight classifies as `⚠ Upgrade Available` and routes to the upgrade migration in section 9. Operator confirmation token: `confirm upgrade`. After section 9 completes, the file reaches schema "0.3" with `_managed_by`; pre-flight on the next invocation then matches step 3 and routes through Scenario F, then Scenario G. Do NOT evaluate later steps for this file.

**Step 5 — Legacy regex (v0.1-era).** If steps 1 through 4 all did not match, test `schema_version` against the legacy regex `^"?v?0\.(1|2|3)(\.\d+)?"?$`. The regex matches the following forms:

```
v0.1, v0.1.0, v0.1.x, 0.1, 0.1.0, "0.1", "v0.1.0",
v0.2, v0.2.0, v0.2.x, 0.2, 0.2.0, "0.2.0",   # NOTE: SHORT "0.2" is handled by step 4 above (canonical-filename + no _managed_by); only NON-canonical or v0.2.0-shaped legacy literals reach this step
v0.3, v0.3.0, v0.3.x, v0.3.1, v0.3.2, 0.3, 0.3.0, 0.3.1, 0.3.2
```

The regex is intentionally permissive about quoting and the leading `v` because v0.1.0-v0.3.2 serialized this field in multiple shapes (see `references/schema-changelog.md`). A match routes to the full legacy migration in section 3. Operator confirmation token: `confirm migration`. v0.6.0 retargets legacy migration to produce schema "0.4" directly (with operator-declared topology); operators with v0.1-era projects skip schemas "0.2" and "0.3" entirely.

**Disambiguation notes (v0.7.0).**

- A file with `schema_version: "0.4"` AND a `topology` block AND an OLD canonical name, with no `pc-NNNN-*` files present, is Scenario G (step 2): a v0.6.0 file eligible for the generation/naming upgrade. It is NOT a parse error.
- A file with `schema_version: "0.4"` but NO `topology` block is malformed v0.6.0 data (schema 0.4 requires topology). It does not match step 1 (wrong schema, no `pc-NNNN`, no `generation`), step 2 (missing topology), step 3 (wrong schema), or step 4 (wrong schema, `_managed_by` may be present), and is not in the legacy regex range. Pre-flight surfaces it as `✗ Parse Error`.
- A file with `schema_version: "0.5"` but NO `generation` field, or whose filename is not `pc-NNNN-*`, is malformed v0.7.0 data. It does not satisfy step 1's full predicate. Pre-flight surfaces it as `✗ Parse Error` (or the generation self-consistency diagnostic per `references/preflight.md` section 3.5 when the filename and `generation` merely disagree).
- A file with `schema_version: "0.3"` and `_managed_by: project-context-skill` and a `topology` block (operator hand-edit, or a third-party partial write) matches none of the six steps cleanly. Pre-flight surfaces this as `✗ Parse Error` with an ambiguity diagnostic and asks the operator to resolve.
- A file with `schema_version: "0.3"` but NO `_managed_by` field does not match steps 1 through 4 and DOES match the step 5 regex, but should NOT be silently treated as legacy because it is malformed v0.5.0, not v0.1-era data. Pre-flight surfaces such files as `✗ Parse Error` per `references/preflight.md`.

**Step 6 — Unknown.** If the file's `schema_version` does not match any of steps 1 through 5, pre-flight halts and asks the operator to identify the file. Verdict: `✗ Mismatch: unknown schema`.

Pseudocode for clarity:

```
def classify_for_migration(file, inventory):
    sv = file.frontmatter.get('schema_version')
    mb = file.frontmatter.get('_managed_by')
    gen = file.frontmatter.get('generation')
    has_topology = 'topology' in file.frontmatter
    is_pc_named = matches(file.filename, r'^pc-\d{4}-(context|entities|archive)\.md$')
    is_canonical = file.filename in {'project-context.md', 'entities.md',
                                     'project-context-archive.md'}
    any_pc_files = inventory.has_any(r'^pc-\d{4}-')

    # Normalize sv (strip surrounding quotes if YAML returned them as part of the string)
    sv_normalized = sv.strip('"') if sv else sv

    # Step 1 — current schema (v0.7.0): pc-NNNN name AND marker AND schema "0.5" AND generation AND topology
    if is_pc_named and mb == 'project-context-skill' and sv_normalized == '0.5' \
            and gen is not None and has_topology:
        return CURRENT                     # ✓ Compatible

    # Step 2 — generation/naming upgrade available (v0.6.0 → v0.7.0, Scenario G)
    if is_canonical and mb == 'project-context-skill' and sv_normalized == '0.4' \
            and has_topology and not any_pc_files:
        return UPGRADE_AVAILABLE_GENERATION  # ⚠ Upgrade Available (v0.6.0 to v0.7.0)

    # Step 3 — topology upgrade available (v0.5.0 → v0.6.0, Scenario F)
    if mb == 'project-context-skill' and sv_normalized == '0.3' and not has_topology:
        return UPGRADE_AVAILABLE_TOPOLOGY  # ⚠ Upgrade Available (v0.5.0 to v0.6.0)

    # Step 4 — upgrade available (v0.4.0 → v0.5.0, Scenario E)
    if is_canonical and sv_normalized == '0.2' and mb is None:
        return UPGRADE_AVAILABLE           # ⚠ Upgrade Available

    # Special case — schema "0.5" but missing generation or wrong name (malformed v0.7.0)
    if sv_normalized == '0.5' and (gen is None or not is_pc_named):
        return PARSE_ERROR                 # ✗ Parse Error — surface to operator

    # Special case — schema "0.4" with missing topology (malformed v0.6.0)
    if sv_normalized == '0.4' and not has_topology:
        return PARSE_ERROR                 # ✗ Parse Error — surface to operator

    # Special case — v0.5.0-shaped schema_version but missing/wrong marker (parse error)
    if sv_normalized == '0.3' and mb != 'project-context-skill':
        return PARSE_ERROR                 # ✗ Parse Error — surface to operator

    # Step 5 — legacy regex (v0.1-era)
    if re.match(r'^"?v?0\.(1|2|3)(\.\d+)?"?$', sv):
        return LEGACY                      # ⚠ Legacy — candidate for full migration

    # Step 6 — unknown
    return UNKNOWN                         # ✗ Mismatch: unknown schema
```

## 2. Migration trigger (legacy)

Legacy migration runs whenever one or more legacy files are detected, **regardless of whether canonical project-context files coexist**. The project states pre-flight may observe (full verdict list in `references/preflight.md`):

| Project state | Verdict | Trigger |
|---|---|---|
| **Pure-current (v0.7.0)** — `pc-NNNN-*` files at schema 0.5 with `_managed_by`, `generation`, and topology block; no old-named, legacy, schema-0.2, or schema-0.3-without-topology files | `✓ Compatible` | No-op for migration. Pre-flight continues into the requested operation; applies topology validation, generation self-consistency, and (for spoke roles) stale-spoke detection. |
| **Pure-generation-upgrade (v0.6.0 → v0.7.0, Scenario G)** — old canonical files at schema 0.4 with `_managed_by` and topology block; no `pc-NNNN-*` files | `⚠ Upgrade Available (v0.6.0 to v0.7.0)` | Route to generation/naming upgrade migration (section 11). Destructive; gates on model setup. Token: `confirm v0.7.0 upgrade`. |
| **Pure-topology-upgrade (v0.5.0 → v0.6.0, Scenario F)** — canonical files at schema 0.3 with `_managed_by` but no topology block; no other state present | `⚠ Upgrade Available (v0.5.0 to v0.6.0)` | Route to topology upgrade migration (section 10). Token: `confirm v0.6.0 upgrade`. After section 10, re-invoke for Scenario G. |
| **Pure-upgrade (v0.4.0 → v0.5.0)** — canonical filenames at schema 0.2 with no `_managed_by`; no v0.1-era legacy files | `⚠ Upgrade Available` | Route to upgrade migration (section 9). Token: `confirm upgrade`. After section 9, re-invoke for Scenario F, then G. |
| **Pure-legacy (v0.1-era)** — one or more legacy files; no current or old canonical files | `⚠ Legacy` | Route to legacy migration (sections 3 to 8). Token: `confirm migration`. Operator declares topology role as part of migration interview; migration produces schema-0.4 files directly; then re-invoke for Scenario G. |
| **Coexistence (legacy + canonical project-context)** — one or more legacy files AND one or more canonical project-context files | `⚠ Legacy` (with completion guidance) | Route to legacy migration. The migration merges legacy content into the existing canonical files (using the same classifier and scoring as a normal session). The operator's safety net is the brief's `download → verify → delete old → upload new` ordering: nothing is deleted from the Project until the operator has reviewed the merged output. |
| **Partial canonical state** — some canonical files present, others missing | `⚠ Partial State` | Surface to operator with two options (rebuild missing from active records OR treat as fresh). No auto-resolution. |

Pre-flight does NOT ask a separate coexistence question. The unified ordering of the operator brief (section 4 below) is the review gate; an additional prompt would duplicate that gate without adding safety.

Migration is one-time per legacy file. After the operator follows the brief's required ordering (verifying the merged output and deleting the named legacy files), re-running pre-flight in the same project finds no legacy files. The resulting schema-0.4 set (old canonical names, topology present, no `pc-NNNN-*` files) then routes to Scenario G (`⚠ Upgrade Available (v0.6.0 to v0.7.0)`) to reach schema 0.5 and `pc-NNNN-*` naming. The terminal pure-current state is a `pc-NNNN-*` set at schema 0.5.

## 3. Legacy migration algorithm

For each legacy file found, in chronological order by file `created` (oldest first):

1. **Parse** the legacy frontmatter and body. Recognize both:
   - The v0.1 body structure (7 sections: Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot).
   - The inline-bracketed per-record format (`[tier: ...] [categories: ...] [sensitivity: ...]`).

2. **Map sections to new file/section:**

   | Legacy section | New file | New section |
   |---|---|---|
   | Decisions | `project-context.md` | Decisions |
   | Constraints | `project-context.md` | Constraints |
   | Entities | `entities.md` | (sub-section inferred from content: People / Places / Things / Organizations / Datasets) |
   | Terminology | `project-context.md` | Terminology |
   | External references | `project-context.md` | External References |
   | Open items | `project-context.md` | Open Items |
   | State snapshot | `project-context.md` | Current State |

3. **Stamp every migrated record** with:

   ```yaml
   first_seen_update: 0
   last_seen_update: 0
   first_seen_at: <legacy file's created field>
   last_seen_at: <legacy file's created field>
   times_seen: 1
   status: active
   audit:
     approval_mode: manual
     approved_by: null
     approved_at: <legacy file's created field>
     warning_response: n/a
     importance_source: llm-auto
   ```

   The `update_count` value `0` is intentional: migration is the bootstrap state before any update has occurred. The first post-migration session increments `update_count` to `1`.

4. **Infer `importance` from legacy tier:**

   | Legacy tier | Inferred `importance` |
   |---|---|
   | `full` (or section default for full-tier sections) | `8` |
   | `summary` (or section default for summary-tier sections) | `5` |
   | `transient` | record is DROPPED, not migrated (transient meant "should not survive consolidation") |

   The user can adjust importance via the diff-and-approve flow on the first post-migration session if needed.

5. **Translate inline category tags** to `links` and `source_quote` where they map; otherwise drop them. The skill does not have an open-category system. Where a legacy category clearly identified a related entity (e.g., `[categories: customer]` against a record naming Acme Corp), add a `link` to the entity record after entities are imported.

6. **Source quote:** if the legacy record was a single sentence, use it verbatim as `source_quote`. If it was longer, capture the first sentence as `source_quote` and store the full content in `content`.

7. **Source ref:** use the legacy filename as `source_ref`. `source_kind: chat`.

8. **Apply update-based scoring** to determine which migrated records go where:
   - `weight >= demotion_threshold` → `project-context.md`.
   - `weight < demotion_threshold` → `project-context-archive.md` with `status: archived`, `demoted_at_update: 0`.

   With `first_seen_update = last_seen_update = 0` and `current_update` starting at `1` post-migration, the recency boost is meaningful only for records with high `importance` and `times_seen > 1` (reinforcement during migration when the same record appears in multiple legacy files).

9. **Deduplicate across legacy files.** When the same record appears in multiple legacy files (recognized by semantic similarity), merge into one record with `times_seen` set to the count of appearances. `first_seen_at` is the earliest legacy file's `created`; `last_seen_at` is the most recent.

10. **Initialize the archive `checkpoints` array** with one entry summarizing the migration:

    ```yaml
    checkpoints:
      - update: 0
        timestamp: <migration timestamp>
        summary: "Migrated from N legacy v0.1 file(s). M records imported, K dropped (transient tier)."
        approver: null
    ```

11. **Solicit the topology role declaration** as part of the migration interview, before any file write. Emit LOCKED TEXT 1 (per `references/preflight.md` section 13.1) verbatim. Wait for the operator's reply.

    - If the operator declares `role: hub`: capture the declaration. No additional fields are needed; the topology block's relationship fields (`hub_reference`, `hub_version`, `last_hub_sync`, `parent`) will be null.
    - If the operator declares `role: spoke-dev` or `role: spoke-solution`: if the reply does not already include hub_reference and hub_version, emit LOCKED TEXT 2 (per `references/preflight.md` section 13.2) verbatim and wait for both values.
    - If the operator declares `role: standalone`: capture the declaration. The topology block's relationship fields will be null.
    - If the operator declines or does not respond within the migration session: fall back to `role: "unclassified"` with `declared_by: "skill-default"`. The skill will re-prompt on next invocation (per `references/preflight.md` section 13). The migration still proceeds; the topology block is written with the unclassified default.

    The skill never writes a partial spoke topology. If hub_reference or hub_version is missing for a declared spoke role, LOCKED TEXT 2 fires until both are provided. The skill does not declare a role on the operator's behalf when the operator engages.

12. **Write the three v0.6.0 files** with `update_count: 0`, `record_count` set to actual counts, `schema_version: "0.4"`, `_managed_by: project-context-skill`, and a `topology` block populated from the operator's declaration in step 11. v0.6.0 retargets legacy migration to produce schema "0.4" directly — operators with v0.1-era projects skip schemas "0.2" and "0.3" entirely. The topology block shape per `references/topology.md` section 1:

    ```yaml
    topology:
      role: <operator-declared role, or "unclassified" if operator did not engage>
      hub_reference: <operator-provided hub project name | null for hub/standalone/unclassified>
      hub_version: <operator-provided hub version | null for hub/standalone/unclassified>
      last_hub_sync: <migration timestamp for spoke-* | null otherwise>
      parent: <operator-provided parent spoke for hybrid topology | null otherwise>
      declared_by: <"operator" if the operator engaged in step 11 | "skill-default" if they declined>
      declared_at: <migration timestamp>
    ```

    If the operator declared `role: hub`, also create an empty `## Spoke Inventory` section in the body of `project-context.md` immediately after frontmatter (per `references/topology.md` section 3). The operator populates the inventory manually as spokes are added.

## 4. The operator brief (legacy migration)

Legacy migration is surfaced via the operator brief as a distinct flow. The skill **does not** delete legacy files automatically (Claude Project APIs do not expose file deletion in May 2026). The brief instructs the operator with the required order of operations.

The topology role declaration (step 11 of the algorithm) fires during the interview before the brief is emitted, so by the time the brief appears the three new files already carry the operator-declared role in their `topology` block. The brief reminds the operator of the declared role for confirmation.

Brief format:

```
Migration complete.

Topology role declared during migration: <declared role>
  - For hub: an empty Spoke Inventory section was created in
    project-context.md. Populate it as you add spokes.
  - For spoke-dev or spoke-solution: hub_reference and hub_version
    are stamped on each new file's topology block.
  - For standalone or unclassified: no Hub relationship; topology
    relationship fields are null.

Order matters: (a) download new, (b) verify, (c) delete old, (d) upload new.
Doing this out of order risks losing the source if the migration was wrong.

(a) Download these three new files from this chat:
   - project-context.md       (N records imported, schema 0.4, role: <declared role>)
   - entities.md              (M records imported, schema 0.4)
   - project-context-archive.md  (K records, including L dropped under DEMOTE, schema 0.4)

(b) Verify the new files look correct.
   Open each one and confirm the records match what you expected.
   Confirm the topology block in project-context.md shows the role you
   declared.
   The migration is reversible until you delete the old files in step (c).

(c) Delete the following old dated files from your Project AFTER verification:
   - 2026-04-15-project-context.md
   - 2026-04-22-project-context-segmentation.md
   - 2026-05-03-project-context-revenue-baseline.md
   - [...exact filename list, one per detected legacy file...]

(d) Upload the three new files to your Project.
   In Claude.ai: Project > Knowledge > Upload file (for each one).

If anything looks off, do NOT delete the legacy files. Tell me what's
wrong and I can re-run migration from the archived versions.
```

The skill always lists each legacy file by its **exact filename**, not generic guidance like "the old files." This is a workshop-locked decision (design spec §5.3 revision 2026-05-18). The schema-0.4 output target and the topology-declaration interview step are v0.6.0 changes per design spec §7.3.

## 5. What legacy migration deliberately does NOT do

- It does not delete legacy files from the Project. Only the operator can do that.
- It does not preserve legacy inline-bracket metadata exactly. Tier and categories are mapped to their schema equivalents (`importance`, structural sections, links) — they are lossy translations by design.
- It does not preserve legacy file-level `audience` or governance fields not defined by the current schema. These were only used by org-config and the migration does not attempt to re-derive them.
- It does not migrate `consolidation_summary` blocks. Those were per-file artifacts of the v0.1 consolidate mode; the skill captures equivalent information in the archive `checkpoints` array.
- It does not migrate records whose legacy tier was `transient` — those were explicitly opt-out of consolidation in the legacy model.

## 6. Idempotency (legacy migration)

Pre-flight behavior on a project that may have been partially or fully migrated:

1. **Post-legacy state** (schema "0.4" files with `_managed_by`, topology block, and old canonical names; no legacy files). Legacy migration finds no legacy files and does not fire. Under v0.7.0 this is NOT pure-current: pre-flight classifies the schema-0.4 set as `⚠ Upgrade Available (v0.6.0 to v0.7.0)` (Scenario G), and the operator confirms `confirm v0.7.0 upgrade` to reach schema 0.5 and `pc-NNNN-*` naming. A `pc-NNNN-*` set at schema 0.5 is the pure-current state that skips all migration.
2. **Coexistence state** (the operator downloaded the new files and uploaded them but has not yet deleted the legacy files). Per section 2, legacy migration runs again — but this time it finds the legacy content already present in the v0.6.0 files and most candidates classify as NOOP (reinforcement) or are dropped as duplicates. The brief reminds the operator to delete the named legacy files. This is safe re-entry, not a separate prompt. The topology role declaration step (step 11 of the algorithm) is skipped on re-entry because the topology block is already present and populated; the migration carries forward the existing role.
3. **Pure-legacy state** (operator skipped the upload step or is running migration for the first time). Migration produces the three new v0.6.0 files at schema "0.4" with topology block populated from the operator's role declaration; the brief lists the legacy files for deletion.

## 7. Edge cases (legacy migration)

| Edge case | Behavior |
|---|---|
| Legacy file with no `schema_version` field | Treated as legacy if the filename matches the legacy pattern. Fail loudly if no detected schema_version and no matching filename. |
| Mixed-version legacy files (some v0.1, some v0.3.2) | Migrated together. All legacy files share the same v0.1 schema regardless of skill-version string in `schema_version` — see `references/schema-changelog.md`. |
| Legacy `consolidated` file | Migrated like any other legacy file. The `consolidation_summary` block is dropped; an archive checkpoint records the migration. |
| Legacy file whose body does not conform to schema "0.1" | Pre-flight warns the operator and asks whether to attempt best-effort migration or skip the file. |
| Two legacy records with identical content but different governance | Merge into one record. The most-restrictive governance value wins. |
| Legacy `related_session_recap` field | Preserved on the new `project-context.md` if present on any legacy file. If multiple legacy files reference different session-recaps, the most-recent reference wins. |

## 8. Cross-references (legacy migration)

- Schema "0.1" field set: `references/schema-changelog.md`.
- Schema "0.4" target: `references/schema.md`.
- Topology block schema (target output for v0.6.0 legacy migration): `references/topology.md`.
- Role-declaration prompts (LOCKED TEXT 1 and 2 emitted in step 11): `references/preflight.md` section 13.
- Scoring driving the active/archive split: `references/scoring.md`.
- Pre-flight invoking migration: `references/preflight.md`.

---

## 9. Upgrade migration (v0.4.0 → v0.5.0)

The upgrade migration is the new path introduced in v0.5.0. It handles projects that already have a v0.4.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at schema "0.2") and need to be brought to schema "0.3" so the pre-flight `_managed_by` detection works.

### 9.1 Detection criteria

Per section 1 step 4: pre-flight identifies upgrade-available files by all three signals:

- Canonical v0.5.0 filename (`project-context.md`, `entities.md`, or `project-context-archive.md`).
- `schema_version: "0.2"` in frontmatter (the v0.4.0 literal).
- No `_managed_by` field in frontmatter.

When all three canonical files match these signals, pre-flight emits verdict `⚠ Upgrade Available` and proposes upgrade migration. If only some of the three canonical files match (e.g., `project-context.md` and `entities.md` at 0.2 but `project-context-archive.md` missing), pre-flight emits `⚠ Partial State` instead and surfaces the partial state to the operator per `references/preflight.md`.

### 9.2 Operator confirmation

Token: `confirm upgrade`. Matching is case-insensitive and whitespace-tolerant per `references/preflight.md`. No fuzzy matching. The pre-flight report block surfaces the token to the operator before any write occurs.

### 9.3 Write algorithm

For each of the three canonical files (`project-context.md`, `entities.md`, `project-context-archive.md`):

1. **Read** the file from project knowledge.
2. **Parse** the YAML frontmatter and the body.
3. **Modify the frontmatter only:**
   - Change `schema_version: "0.2"` → `schema_version: "0.3"`.
   - Add `_managed_by: project-context-skill` near the other top-level frontmatter fields (place adjacent to `schema_version` for legibility).
4. **Preserve all other frontmatter fields and all body content unchanged.** No record-level fields are modified, no records are added or removed, no `update_count` increment, no `last_merged` update — the upgrade is metadata-only. `generated_by.version` is explicitly preserved unchanged; the field records the skill version that originally produced the records, not the upgrade.
5. **Emit the modified file** as a proposed write.

### 9.4 Post-flight summary

Per `references/preflight.md` section on post-flight, the post-flight summary for upgrade migration takes this shape:

```
## Post-flight Summary ✓ Upgrade Complete

**Files upgraded to schema 0.3:**
- project-context.md (added _managed_by marker, bumped schema_version)
- entities.md (added _managed_by marker, bumped schema_version)
- project-context-archive.md (added _managed_by marker, bumped schema_version)

**Skill version:** 0.7.0
**Records:** preserved unchanged (no content modifications, only schema upgrade)
**Operation performed:** in-place schema upgrade
```

### 9.5 Operator brief (upgrade migration)

Unlike legacy migration, the upgrade rewrites the three canonical files in place with the same filenames. There is no legacy-file-deletion step. The brief uses the simpler download-and-replace pattern:

```
✅ Upgrade complete.

The three files were rewritten in place with the new schema "0.3" marker.
All records, all timestamps, all audit metadata, and all body content are
unchanged. Only the frontmatter was touched.

📥 Download these three files from this chat:
   • project-context.md
   • entities.md
   • project-context-archive.md

📂 Upload them to your Project, replacing the existing schema-0.2 versions.
   In Claude.ai: Project → Knowledge → Upload file → confirm replace.

🔔 No legacy files to delete — the upgrade kept the same canonical filenames.

After the replace completes, future skill invocations will detect the
_managed_by marker and run pre-flight reliably.
```

### 9.6 What upgrade migration deliberately does NOT do

- It does NOT modify any record content. Every record's `content`, `source_quote`, `audit`, `links`, `importance`, lifecycle fields are preserved verbatim.
- It does NOT increment `update_count`. Pre-flight may treat upgrade as a non-update event; the next normal session will increment.
- It does NOT add a checkpoint to the archive's `checkpoints` array. The schema upgrade is structural, not a content event.
- It does NOT change the `last_merged` timestamp. The schema-version bump itself is the audit marker for the upgrade event. `generated_by.version` is preserved unchanged — it records the skill version that originally produced the records, not the upgrade.
- It does NOT alter the `created` timestamp.

### 9.7 Idempotency (upgrade migration)

Scenario E is a two-stage migration path by design in v0.6.0: the first invocation completes Scenario E (0.2 → 0.3), and the second invocation completes Scenario F (0.3 → 0.4 with topology) per `references/preflight.md` section 13. Re-invocation behavior reflects that staging.

If pre-flight is invoked again on a project that has just completed Scenario E (schema "0.3" with `_managed_by` present on all three files, no `topology` block), step 1 of the detection (per section 1's six-branch classification) does NOT route the project to `✓ Compatible`; instead, step 3 matches (`_managed_by` present + `schema_version: "0.3"` + no topology block) and the project routes to `⚠ Upgrade Available (v0.5.0 to v0.6.0)` (Scenario F). The Scenario E output is ready for Scenario F on next invocation, not "compatible/current" in the v0.6.0 sense. Operator confirmation token for the second stage: `confirm v0.6.0 upgrade`. See section 10.

Re-running Scenario E itself against an already-Scenario-E-upgraded project (i.e., the operator attempts to re-trigger Scenario E by typing `confirm upgrade` when pre-flight has already emitted `⚠ Upgrade Available (v0.5.0 to v0.6.0)`) is a token mismatch: the expected token for the project's current state is `confirm v0.6.0 upgrade`, not `confirm upgrade`. Pre-flight surfaces the token-mismatch error per `references/preflight.md` section 6.1.

If the operator partially completed Scenario E (e.g., uploaded the new `project-context.md` at schema "0.3" with `_managed_by` but kept the old `entities.md` at schema "0.2"), pre-flight will see mixed states: one file matches step 3 (UPGRADE_AVAILABLE_TOPOLOGY: ready for Scenario F), one matches step 4 (UPGRADE_AVAILABLE: still needs Scenario E), and one may be missing. Resolution: re-run Scenario E to bring the remaining schema-0.2 file to schema "0.3"; step 3 then routes all three through Scenario F to reach schema "0.4", then Scenario G to reach the current schema "0.5". The detection's six-branch classification handles each file independently per `references/preflight.md` section 3.2.

A project that has completed both Scenario E and Scenario F is at schema "0.4" with `_managed_by` and a topology block on all three files. Under v0.7.0 that is not the terminal state: pre-flight classifies the schema-0.4 set as `⚠ Upgrade Available (v0.6.0 to v0.7.0)` (Scenario G), and the operator re-invokes with `confirm v0.7.0 upgrade` to reach schema 0.5. The terminal pure-current state is a `pc-NNNN-*` set at schema 0.5, where topology validation and (for `role: spoke-*`) stale-spoke detection apply per `references/preflight.md` sections 10 and 11.

### 9.8 Edge cases (upgrade migration)

| Edge case | Behavior |
|---|---|
| Canonical filename at schema "0.2" but with a stray `_managed_by` field (operator hand-edit?) | Pre-flight surfaces ambiguity. Treat the file as malformed; halt and ask the operator. |
| Canonical filename at schema "0.2" but `_managed_by` set to something other than `project-context-skill` (a different skill claiming management?) | Pre-flight halts and asks the operator to identify the rightful manager. Do not silently overwrite a marker belonging to another skill. |
| Three canonical filenames present but mixed schema_versions (e.g., one at 0.2, one at 0.3, one missing) | `⚠ Partial State`. Surface to operator with rebuild-or-fresh choice. |
| Upgrade fails mid-write (e.g., second of three files cannot be written) | Post-flight emits `✗ Failed` verdict with diagnostic. Operator instructions for partial-state recovery: re-run upgrade migration; idempotency (9.7) handles already-upgraded files. |

---

## 10. Topology upgrade migration (v0.5.0 → v0.6.0, Scenario F)

The topology upgrade migration is the new path introduced in v0.6.0. It handles projects that already have a v0.5.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at schema "0.3" with `_managed_by`) and need to be brought to schema "0.4" so the v0.6.0 topology block, audit trigger, and stale-spoke detection work.

The migration adds the topology block (with `role: "unclassified"` default and all relationship fields null) and bumps the schema_version literal. All other frontmatter and body content is preserved verbatim. The operator declares the topology role in a follow-up exchange after the upgrade completes; the skill prompts using LOCKED TEXT 1 (per `references/preflight.md` section 13).

### 10.1 Detection criteria

Per section 1 step 3: pre-flight identifies Scenario F files by all three signals:

- `_managed_by: project-context-skill` in frontmatter.
- `schema_version: "0.3"` in frontmatter.
- No `topology` block in frontmatter.

When all three canonical files match these signals, pre-flight emits verdict `⚠ Upgrade Available (v0.5.0 to v0.6.0)` and proposes Scenario F migration. If only some of the three canonical files match (e.g., `project-context.md` and `entities.md` at 0.3 without topology but `project-context-archive.md` missing), pre-flight emits `⚠ Partial State` instead and surfaces the partial state to the operator per `references/preflight.md`.

### 10.2 Operator confirmation

Token: `confirm v0.6.0 upgrade`. Matching is case-insensitive and whitespace-tolerant per `references/preflight.md`. No fuzzy matching. The pre-flight report block surfaces the token to the operator before any write occurs.

### 10.3 Write algorithm

For each of the three canonical files (`project-context.md`, `entities.md`, `project-context-archive.md`), in this order:

1. **Read** the file from project knowledge.
2. **Parse** the YAML frontmatter and the body.
3. **Add** a `topology` block to the frontmatter with skill-default values:

   ```yaml
   topology:
     role: "unclassified"
     hub_reference: null
     hub_version: null
     last_hub_sync: null
     parent: null
     declared_by: "skill-default"
     declared_at: <current ISO 8601 timestamp>
   ```

   Place the topology block adjacent to `_managed_by` and `schema_version` for legibility (top of frontmatter, after `name`/`file_role` if present).

4. **Change** `schema_version: "0.3"` → `schema_version: "0.4"`.
5. **Preserve all other frontmatter fields and all body content unchanged.** No record-level fields are modified, no records are added or removed, no `update_count` increment, no `last_merged` update — the upgrade is metadata-only. `generated_by.version` is explicitly preserved unchanged; the field records the skill version that originally produced the records, not the upgrade.
6. **Emit** the modified file as a proposed write.
7. **After all three files write successfully:** emit LOCKED TEXT 1 (per `references/preflight.md` section 13.1) as a follow-up prompt to solicit the operator's topology role declaration. The skill does not infer a role; it waits for the operator's reply.

### 10.4 Post-flight summary

Per `references/preflight.md` section 9.3, the post-flight summary for Scenario F migration takes this shape:

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
  The skill will prompt with the role-declaration prompt (preflight.md
  section 13).
```

### 10.5 Operator brief (topology upgrade)

Unlike legacy migration, the topology upgrade rewrites the three canonical files in place with the same filenames. There is no legacy-file-deletion step. The brief uses the simpler download-and-replace pattern:

```
Upgrade complete (v0.5.0 to v0.6.0).

The three files were rewritten in place with the new schema "0.4"
marker and a topology metadata block (role: unclassified by default).
All records, all timestamps, all audit metadata, and all body content
are unchanged. Only the frontmatter was touched.

Download these three files from this chat:
   - project-context.md
   - entities.md
   - project-context-archive.md

Upload them to your Project, replacing the existing schema-0.3 versions.
   In Claude.ai: Project > Knowledge > Upload file > confirm replace.

No legacy files to delete — the upgrade kept the same canonical filenames.

Next step: declare the topology role for this project. The skill will
prompt with the role-declaration prompt. Reply with one of: hub,
spoke-dev, spoke-solution, or standalone.
```

### 10.6 Role declaration follow-up

After the file writes complete and the operator confirms the upload, the skill emits LOCKED TEXT 1 (per `references/preflight.md` section 13.1) to solicit a role declaration. The operator replies with a role name. The skill then writes the declared role to `topology.role` in `project-context.md`:

- **role: hub** — Write `role: hub`, set `declared_by: "operator"` and `declared_at: <current timestamp>`. Create an empty `## Spoke Inventory` section in the body of `project-context.md` immediately after frontmatter (per `references/topology.md` section 3).
- **role: spoke-dev** or **role: spoke-solution** — If the operator's reply includes `hub_reference` and `hub_version`, write those values plus `last_hub_sync: <current timestamp>`, `declared_by: "operator"`, `declared_at: <current timestamp>`. If hub_reference or hub_version is missing, emit LOCKED TEXT 2 (per `references/preflight.md` section 13.2) and wait for both.
- **role: standalone** — Write `role: standalone` with all relationship fields remaining null, `declared_by: "operator"`, `declared_at: <current timestamp>`.

The skill never writes a partial spoke topology. If the operator declines or does not respond, the topology stays `unclassified`; the skill prompts again on next invocation.

### 10.7 What topology upgrade migration deliberately does NOT do

- It does NOT modify any record content. Every record's `content`, `source_quote`, `audit`, `links`, `importance`, lifecycle fields are preserved verbatim.
- It does NOT declare a role on the operator's behalf. The default is `unclassified` and the skill always asks.
- It does NOT increment `update_count`. The schema upgrade is structural, not a content event.
- It does NOT add a checkpoint to the archive's `checkpoints` array.
- It does NOT change the `last_merged` timestamp. The schema-version bump is the audit marker for the upgrade event. `generated_by.version` is preserved unchanged — it records the skill version that originally produced the records, not the upgrade.
- It does NOT alter the `created` timestamp.
- It does NOT populate the spoke inventory (Hub case) or hub_reference/hub_version (spoke case) without an explicit operator declaration.

### 10.8 Idempotency (topology upgrade migration)

If pre-flight is invoked again on a project that has completed Scenario F (schema "0.4" with `_managed_by` and topology block present on all three files), it is not yet current under v0.7.0: step 2 of the detection classifies the schema-0.4 set as `⚠ Upgrade Available (v0.6.0 to v0.7.0)` (Scenario G), and the operator re-invokes with `confirm v0.7.0 upgrade` to reach schema 0.5. Re-running Scenario F against a schema-0.4 set is a no-op by classification (Scenario F targets schema 0.3 with no topology block); the schema-0.4 set routes to Scenario G instead.

If the operator partially upgraded (e.g., uploaded the new schema-0.4 `project-context.md` but kept the old schema-0.3 `entities.md`), pre-flight will see mixed states: the upgraded schema-0.4 file matches step 2 (Scenario G eligible; it is not current, since current requires `pc-NNNN-*` at schema 0.5), and the schema-0.3 files match step 3 (UPGRADE_AVAILABLE_TOPOLOGY, Scenario F). This is a partial state. Resolution: re-run Scenario F to bring the remaining schema-0.3 files to schema 0.4 (Scenario F's step-3 predicate does not match the already-upgraded schema-0.4 file, so it is left untouched), then run Scenario G to carry the whole schema-0.4 set to schema 0.5.

If the operator did not respond to the role-declaration prompt after a previous Scenario F upgrade, the topology stays `unclassified`. The skill re-prompts on next invocation. This is a transitional state, not a corruption.

### 10.9 Edge cases (topology upgrade migration)

| Edge case | Behavior |
|---|---|
| Operator does not respond to role-declaration prompt | Topology remains `unclassified`. Skill prompts again on next invocation. No data corruption; skill operates normally with unclassified topology. |
| Operator declares `role: spoke-*` but does not provide hub_reference or hub_version | Skill emits LOCKED TEXT 2 (per `references/preflight.md` section 13.2) and waits for both. Skill will not write a partial spoke topology. |
| Operator declares `role: hub` after upgrade | Skill creates empty `## Spoke Inventory` section in body of `project-context.md`. Operator populates manually. |
| Operator declares `role: spoke-solution` and later wants to add child Dev spokes | Standard spoke inventory management on the parent Solution; child spokes declare `parent: <solution-name>` in their own topology. |
| Schema 0.3 file with `_managed_by` but with a stray `topology` block (operator hand-edit, or third-party tool partial upgrade) | Pre-flight surfaces ambiguity. Treat the file as malformed; halt and ask the operator (per section 1 disambiguation notes). |
| Three canonical filenames present but mixed schemas (e.g., one at 0.4-with-topology, one at 0.3-without-topology, one missing) | `⚠ Partial State`. Surface to operator with rebuild-or-fresh choice. |
| Upgrade fails mid-write (e.g., second of three files cannot be written) | Post-flight emits `✗ Failed` verdict with diagnostic. Operator instructions for partial-state recovery: re-run Scenario F upgrade; idempotency (10.8) handles already-upgraded files. |
| Operator declares `role: spoke-dev` with `parent` (hybrid topology, child of a Solution) | Skill writes `parent: <solution-name>` to the topology block alongside hub_reference and hub_version. Validates that `parent` is not null only for `spoke-dev`. |

## 11. Generation/naming upgrade migration (v0.6.0 → v0.7.0, Scenario G)

The generation/naming upgrade migration is the new path introduced in v0.7.0. It handles projects that already have a v0.6.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at schema "0.4" with `_managed_by` and a topology block) and brings them to schema "0.5": versioned `pc-NNNN-*` naming, the new `generation` field, and the config treatment.

The migration renames the three files to `pc-0001-*`, adds `generation: 1`, bumps the schema_version literal, and applies the config treatment. **It preserves all record content, `update_count`, every per-record counter, and the topology block verbatim.** The only changes are the filename, the addition of `generation`, the `schema_version` literal, and the config-file header/relocation. This is a destructive operation (it rewrites the canonical file set) and gates on model setup per `references/preflight.md` section 4.6.

### 11.1 Detection criteria

Per section 1 step 2: pre-flight identifies Scenario G files by all of:

- Old canonical filename (`project-context.md`, `entities.md`, or `project-context-archive.md`).
- `_managed_by: project-context-skill` in frontmatter.
- `schema_version: "0.4"` in frontmatter.
- A `topology` block present in frontmatter.
- No `pc-NNNN-*` files present in the inventory.

When all three canonical files match these signals, pre-flight emits verdict `⚠ Upgrade Available (v0.6.0 to v0.7.0)` and proposes Scenario G migration. If only some of the three match (e.g., `project-context.md` and `entities.md` at 0.4 but `project-context-archive.md` missing), pre-flight emits `⚠ Partial State` instead.

Detection is enumeration-dependent (it requires reading the inventory to confirm no `pc-NNNN-*` files exist). On a non-enumerating surface, the migration is operator-invoked rather than auto-detected; in practice the operator runs it on web where the old files are visible. This is documented, not silently skipped.

### 11.2 Operator confirmation and model-setup gate

Token: `confirm v0.7.0 upgrade`. Matching is case-insensitive and whitespace-tolerant per `references/preflight.md` section 6. No fuzzy matching.

Scenario G is destructive-tier (section 4.6 of `references/preflight.md`). The pre-flight report names the model-setup recommendation (run on the strongest thinking-capable model with extended thinking). The single token `confirm v0.7.0 upgrade` both confirms model setup and authorizes the migration; no separate `confirm model setup` step is required.

### 11.3 Write algorithm

For each of the three context files, in this order (`project-context.md` → `pc-0001-context.md`, `entities.md` → `pc-0001-entities.md`, `project-context-archive.md` → `pc-0001-archive.md`):

1. **Read** the file from project knowledge.
2. **Parse** the YAML frontmatter and the body.
3. **Write under the new name** `pc-0001-<role>.md`. Counter seed resets to 1. The new name's `NNNN` is `0001`.
4. **Add** `generation: 1` to the frontmatter (adjacent to `_managed_by`/`schema_version` for legibility).
5. **Change** `schema_version: "0.4"` → `schema_version: "0.5"`.
6. **Preserve everything else verbatim.** `update_count` is preserved unchanged (it is the scoring counter and is NOT reset). Every per-record counter (`first_seen_update`, `last_seen_update`, `times_seen`, `first_seen_at`, `last_seen_at`), the audit blocks, `record_count`, `generated_by.*`, the archive `checkpoints` array, and the entire `topology` block are carried verbatim. No record content changes. No provenance line is added. No carry-forward from `update_count` into `generation`.
7. **Emit** the renamed file as a proposed write.

### 11.4 Config treatment (folded into Scenario G)

Apply to the three config files (`user-config.md`, `org-config.md`, `platform-specific-parameters.md`) wherever they exist in the project:

1. Add the schema 0.5 config header: `config_editable: true` and `configure_with: references/configure.md`.
2. Bump `schema_version` to `"0.5"`.
3. On filesystem platforms, relocate them into `config/`. On flat web, they remain readable by base name; relocation is a no-op at the read layer and only the header and schema bump apply.

The config bodies are otherwise unchanged. If a config file is absent, there is nothing to treat for it.

### 11.5 Post-flight summary and operator brief

Per `references/preflight.md` section 9.3 (Scenario G example), the post-flight summary lists the new `pc-0001-*` files, renders the set-integrity directive (section 9.6), and instructs the operator to delete the old-named files. Brief:

```
Upgrade complete (v0.6.0 to v0.7.0).

The three files were rewritten under versioned names at schema "0.5":
   project-context.md          ->  pc-0001-context.md
   entities.md                 ->  pc-0001-entities.md
   project-context-archive.md  ->  pc-0001-archive.md

What changed: filenames; added generation: 1; bumped schema_version 0.4
to 0.5; config files received the config_editable/configure_with header
and a schema bump (relocated to config/ on filesystem platforms). All
records, update_count, every per-record counter, the audit metadata, and
the topology block are unchanged.

Order matters: (a) download new, (b) verify, (c) upload new, (d) delete old.

(a) Download the three new files from this chat:
   - pc-0001-context.md
   - pc-0001-entities.md
   - pc-0001-archive.md

(b) Verify they look correct (records intact, topology block present,
   update_count preserved).

(c) Upload the pc-0001-* set to your Project.

(d) After verifying, delete the old-named files now superseded:
   - project-context.md
   - entities.md
   - project-context-archive.md

Set integrity: Replace, do not duplicate. The current canonical set is
pc-0001-context.md, pc-0001-entities.md, and pc-0001-archive.md at
generation 1. After you upload this set, delete any prior pc-MMMM-* set
with a lower counter. Do not upload the same generation twice; a same-name
duplicate can fail the next pre-flight.
```

### 11.6 What Scenario G deliberately does NOT do

- It does NOT modify any record content, `update_count`, or any per-record counter. Only the filename, `generation` (new), `schema_version` literal, and config header/location change.
- It does NOT reset `update_count` or rebase any `*_update` field. Scoring continuity is preserved (the F1 ruling: `generation` is identity-only, `update_count` is the scoring counter).
- It does NOT carry the old `update_count` value forward into `generation`. `generation` seeds at 1 independently.
- It does NOT add a provenance line or a checkpoint for the migration event. The schema bump and rename are the trace.
- It does NOT change the `topology` block. It is carried verbatim.
- It does NOT delete the old-named files. Only the operator can; the brief instructs the order.
- It does NOT re-declare or re-prompt for the topology role. The role is already declared and carried verbatim.

### 11.7 Idempotency (Scenario G)

If pre-flight is invoked again after a completed Scenario G (the project holds `pc-0001-*` files at schema 0.5 with `generation` and topology), step 1 routes to `✓ Compatible` and no migration runs. Re-running Scenario G against an already-upgraded project is a no-op by classification.

If the operator left the old-named files in place after uploading the `pc-0001-*` set (coexistence), the distinct names mean no same-name collision. Pre-flight matches the `pc-0001-*` set as CURRENT (step 1), and the old-named schema-0.4 files no longer satisfy step 2 because `pc-NNNN-*` files are now present (the `not any_pc_files` predicate fails). The old-named files are stale clutter, not a Parse Error; pre-flight notes them for deletion. This is safe re-entry.

If the operator partially uploaded (e.g., uploaded `pc-0001-context.md` but kept the other two old-named), pre-flight sees mixed state and emits `⚠ Partial State` with the rebuild-or-fresh choice.

### 11.8 Edge cases (Scenario G)

| Edge case | Behavior |
|---|---|
| Operator declines the model-setup gate (does not send `confirm v0.7.0 upgrade`) | Migration does not proceed; files unchanged; the verdict and gate render again on the next attempt. |
| Operator leaves old-named files after migration | Distinct names mean no collision; pre-flight matches `pc-0001-*` as current and notes the old-named files for deletion (section 11.7). |
| Non-enumerating surface, Scenario G not auto-detected | Operator invokes the upgrade explicitly, or runs it on web where old files are visible. Documented, not silently skipped. |
| A `generation` field already present on a schema-0.4 file (hand-edit) | Malformed: schema 0.4 does not define `generation`. Pre-flight surfaces `✗ Parse Error` with an ambiguity diagnostic. |
| Old-named files at schema 0.4 with NO topology block | Not Scenario G (missing topology). `✗ Parse Error` per section 1 disambiguation notes. |
| Upgrade fails mid-write (second of three files cannot be written) | Post-flight emits `✗ Failed` with diagnostic. Recovery: re-run Scenario G; idempotency (11.7) leaves already-renamed files untouched and completes the rest. |

## 12. Cross-references (all migrations)

- Schema definition and validation checklist (schema 0.5, generation, naming contract): `references/schema.md`.
- Schema-changelog and Supported Schemas matrix: `references/schema-changelog.md`.
- Pre-flight algorithm, counter assignment (section 3.4), generation self-consistency (section 3.5), advisory and two-tier gate (section 4.6), report block, token catalog, post-flight summary and set-integrity directive (section 9.6): `references/preflight.md`.
- Topology metadata schema, role definitions, spoke inventory format, audit trigger semantics, validation rules: `references/topology.md`.
- Role-declaration prompts (LOCKED TEXT 1 and 2): `references/preflight.md` section 13.
- Config treatment, interview mechanics, and the config/references separation: `references/configure.md`; `config/user-config.md.template`, `config/org-config.md.template`, `config/platform-specific-parameters.md.template`.
- Scoring algorithm driving the legacy migration's active/archive split (keyed off the retained `update_count`): `references/scoring.md`.
