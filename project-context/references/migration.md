---
file_role: skill-reference
topic: migration
schema_version_documented: "0.3"
skill_version: "0.5.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Migration (project-context v0.5.0)

This file documents the two migration paths v0.5.0 supports:

1. **Legacy migration** (schema "0.1" → "0.3"): one-time, per-project, from the v0.1-era schema used by skill versions v0.1.0 through v0.3.2 to the current schema "0.3". Operators with v0.1-era projects skip schema "0.2" entirely. See sections 1–8.
2. **Upgrade migration** (schema "0.2" → "0.3"): one-time, per-project, in-place upgrade from the v0.4.0 schema "0.2" to the current schema "0.3". Adds the new REQUIRED `_managed_by` field; preserves all other content unchanged. See section 9.

Pre-flight (per `references/preflight.md`) classifies the project's state and routes to the right migration path. This file is the algorithm pre-flight cites for the write phase.

For the history of what was actually written under "0.1", including the unquoted-skill-version-as-schema_version accident, see `references/schema-changelog.md`. For the cross-version compatibility matrix (what v0.5.0 reads, writes, migrates from, refuses), see the "Supported Schemas" section of `references/schema-changelog.md`.

## 1. Detection

Pre-flight scans the project for files matching either:

- The canonical v0.5.0 filenames: `project-context.md`, `entities.md`, `project-context-archive.md`.
- The legacy filename pattern: `*-project-context*.md` (dated, optionally topic-suffixed, including `-consolidated[-N]` variants).
- A `file_type: project-context` value in the YAML frontmatter.

For every match, parse the frontmatter and run the **four-branch classification** below, in this exact order. The branch ordering is significant: the `_managed_by` requirement in step 1 is the explicit disambiguator that distinguishes the v0.5.0 current marker from any legacy literal the broad regex (step 3) would otherwise match.

**Step 1 — Current-schema (v0.5.0).** If the file has BOTH `_managed_by: project-context-skill` AND `schema_version: "0.3"`, the file is a v0.5.0 current-schema file. Skip migration; pre-flight classifies as `✓ Compatible` and proceeds with normal operation per `references/preflight.md`. Do NOT evaluate later steps.

**Step 2 — Upgrade-available (v0.4.0 → v0.5.0).** If the file has a canonical v0.5.0 filename AND `schema_version: "0.2"` (the v0.4.0 literal) AND no `_managed_by` field, the file is a v0.4.0 schema-0.2 file eligible for in-place upgrade. Pre-flight classifies as `⚠ Upgrade Available` and routes to the upgrade migration in section 9. Operator confirmation token: `confirm upgrade`. Do NOT evaluate later steps for this file.

**Step 3 — Legacy regex (v0.1-era).** If neither step 1 nor step 2 matched, test `schema_version` against the legacy regex `^"?v?0\.(1|2|3)(\.\d+)?"?$`. The regex matches the following forms:

```
v0.1, v0.1.0, v0.1.x, 0.1, 0.1.0, "0.1", "v0.1.0",
v0.2, v0.2.0, v0.2.x, 0.2, 0.2.0, "0.2.0",   # NOTE: SHORT "0.2" is handled by step 2 above (canonical-filename + no _managed_by); only NON-canonical or v0.2.0-shaped legacy literals reach this step
v0.3, v0.3.0, v0.3.x, v0.3.1, v0.3.2, 0.3, 0.3.0, 0.3.1, 0.3.2
```

The regex is intentionally permissive about quoting and the leading `v` because v0.1.0-v0.3.2 serialized this field in multiple shapes (see `references/schema-changelog.md`). A match routes to the full legacy migration in section 3. Operator confirmation token: `confirm migration`.

**Disambiguation note (v0.5.0).** A file with `schema_version: "0.3"` but NO `_managed_by` field does not match step 1 (no marker), does not match step 2 (wrong schema_version), and DOES match the step 3 regex — but should NOT be silently treated as legacy because it is malformed v0.5.0, not v0.1-era data. Pre-flight surfaces such files as `✗ Parse Error` per `references/preflight.md` rather than auto-classifying as legacy.

**Step 4 — Unknown.** If the file's `schema_version` does not match any of steps 1, 2, or 3, pre-flight halts and asks the operator to identify the file. Verdict: `✗ Mismatch: unknown schema`.

Pseudocode for clarity:

```
def classify_for_migration(file):
    sv = file.frontmatter.get('schema_version')
    mb = file.frontmatter.get('_managed_by')
    is_canonical = file.filename in {'project-context.md', 'entities.md',
                                     'project-context-archive.md'}

    # Step 1 — current schema (v0.5.0)
    if mb == 'project-context-skill' and sv == '"0.3"' or sv == '0.3':
        return CURRENT          # ✓ Compatible

    # Step 2 — upgrade available (v0.4.0 → v0.5.0)
    if is_canonical and (sv == '"0.2"' or sv == '0.2') and mb is None:
        return UPGRADE_AVAILABLE  # ⚠ Upgrade Available

    # Special case — v0.5.0-shaped schema_version but no marker (parse error)
    if (sv == '"0.3"' or sv == '0.3') and mb != 'project-context-skill':
        return PARSE_ERROR      # ✗ Parse Error — surface to operator

    # Step 3 — legacy regex (v0.1-era)
    if re.match(r'^"?v?0\.(1|2|3)(\.\d+)?"?$', sv):
        return LEGACY           # ⚠ Legacy — candidate for full migration

    # Step 4 — unknown
    return UNKNOWN              # ✗ Mismatch: unknown schema
```

## 2. Migration trigger (legacy)

Legacy migration runs whenever one or more legacy files are detected, **regardless of whether v0.5.0 files coexist**. The project states pre-flight may observe (full verdict list in `references/preflight.md`):

| Project state | Verdict | Trigger |
|---|---|---|
| **Pure-current (v0.5.0)** — canonical v0.5.0 files only; no legacy files; no schema-0.2 files | `✓ Compatible` | No-op for migration. Pre-flight continues into the requested operation. |
| **Pure-upgrade (v0.4.0 → v0.5.0)** — canonical filenames at schema 0.2 with no `_managed_by`; no v0.1-era legacy files | `⚠ Upgrade Available` | Route to upgrade migration (section 9). Token: `confirm upgrade`. |
| **Pure-legacy (v0.1-era)** — one or more legacy files; no v0.5.0 canonical files | `⚠ Legacy` | Route to legacy migration (sections 3–8). Token: `confirm migration`. |
| **Coexistence (legacy + v0.5.0)** — one or more legacy files AND one or more canonical v0.5.0 files | `⚠ Legacy` (with completion guidance) | Route to legacy migration. The migration merges legacy content into the existing v0.5.0 files (using the same classifier and scoring as a normal session). The operator's safety net is the brief's `download → verify → delete old → upload new` ordering: nothing is deleted from the Project until the operator has reviewed the merged output. |
| **Partial v0.5.0 state** — some canonical files present, others missing | `⚠ Partial State` | Surface to operator with two options (rebuild missing from active records OR treat as fresh). No auto-resolution. |

Pre-flight does NOT ask a separate coexistence question. The unified ordering of the operator brief (section 4 below) is the review gate; an additional prompt would duplicate that gate without adding safety.

Migration is one-time per legacy file. After the operator follows the brief's required ordering — verifying the merged output and deleting the named legacy files — re-running pre-flight in the same project finds no legacy files and falls into the pure-current state.

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

   The `update_count` value `0` is intentional: migration is the bootstrap state before any v0.5.0 update has occurred. The first post-migration session increments `update_count` to `1`.

4. **Infer `importance` from legacy tier:**

   | Legacy tier | Inferred `importance` |
   |---|---|
   | `full` (or section default for full-tier sections) | `8` |
   | `summary` (or section default for summary-tier sections) | `5` |
   | `transient` | record is DROPPED, not migrated (transient meant "should not survive consolidation") |

   The user can adjust importance via the diff-and-approve flow on the first post-migration session if needed.

5. **Translate inline category tags** to `links` and `source_quote` where they map; otherwise drop them. v0.5.0 does not have an open-category system. Where a legacy category clearly identified a related entity (e.g., `[categories: customer]` against a record naming Acme Corp), add a `link` to the entity record after entities are imported.

6. **Source quote:** if the legacy record was a single sentence, use it verbatim as `source_quote`. If it was longer, capture the first sentence as `source_quote` and store the full content in `content`.

7. **Source ref:** use the legacy filename as `source_ref`. `source_kind: chat`.

8. **Apply update-based scoring** to determine which migrated records go where:
   - `weight >= demotion_threshold` → `project-context.md`.
   - `weight < demotion_threshold` → `project-context-archive.md` with `status: archived`, `demoted_at_update: 0`.

   With `first_seen_update = last_seen_update = 0` and `current_update` starting at `1` post-migration, the recency boost is meaningful only for records with high `importance` and `times_seen > 1` (reinforcement during migration when the same record appears in multiple legacy files).

9. **Deduplicate across legacy files.** When the same record appears in multiple legacy files (recognized by semantic similarity), merge into one v0.5.0 record with `times_seen` set to the count of appearances. `first_seen_at` is the earliest legacy file's `created`; `last_seen_at` is the most recent.

10. **Initialize the archive `checkpoints` array** with one entry summarizing the migration:

    ```yaml
    checkpoints:
      - update: 0
        timestamp: <migration timestamp>
        summary: "Migrated from N legacy v0.1 file(s). M records imported, K dropped (transient tier)."
        approver: null
    ```

11. **Write the three v0.5.0 files** with `update_count: 0`, `record_count` set to actual counts, `schema_version: "0.3"`, and `_managed_by: project-context-skill` in the frontmatter of every file. v0.5.0 retargets legacy migration to produce schema "0.3" directly — operators with v0.1-era projects skip schema "0.2" entirely.

## 4. The operator brief (legacy migration)

Legacy migration is surfaced via the operator brief as a distinct flow. The skill **does not** delete legacy files automatically (Claude Project APIs do not expose file deletion in May 2026). The brief instructs the operator with the required order of operations:

```
✅ Migration complete.

Order matters: (a) download new, (b) verify, (c) delete old, (d) upload new.
Doing this out of order risks losing the source if the migration was wrong.

📥 (a) Download these three new files from this chat:
   • project-context.md       (N records imported)
   • entities.md              (M records imported)
   • project-context-archive.md  (K records, including L dropped under DEMOTE)

🔍 (b) Verify the new files look correct.
   Open each one and confirm the records match what you expected.
   The migration is reversible until you delete the old files in step (c).

🗑 (c) Delete the following old dated files from your Project AFTER verification:
   • 2026-04-15-project-context.md
   • 2026-04-22-project-context-segmentation.md
   • 2026-05-03-project-context-revenue-baseline.md
   • [...exact filename list, one per detected legacy file...]

📂 (d) Upload the three new files to your Project.
   In Claude.ai: Project → Knowledge → Upload file (for each one).

🔔 If anything looks off, do NOT delete the legacy files. Tell me what's
   wrong and I can re-run migration from the archived versions.
```

The skill always lists each legacy file by its **exact filename**, not generic guidance like "the old files." This is a workshop-locked decision (design spec §5.3 revision 2026-05-18).

## 5. What legacy migration deliberately does NOT do

- It does not delete legacy files from the Project. Only the operator can do that.
- It does not preserve legacy inline-bracket metadata exactly. Tier and categories are mapped to v0.5.0 equivalents (`importance`, structural sections, links) — they are lossy translations by design.
- It does not preserve legacy file-level `audience` or non-v0.5.0 governance fields. These were only used by org-config and the migration does not attempt to re-derive them.
- It does not migrate `consolidation_summary` blocks. Those were per-file artifacts of the v0.1 consolidate mode; v0.5.0 captures equivalent information in the archive `checkpoints` array.
- It does not migrate records whose legacy tier was `transient` — those were explicitly opt-out of consolidation in the legacy model.

## 6. Idempotency (legacy migration)

Pre-flight behavior on a project that may have been partially or fully migrated:

1. **Pure-current state** (only v0.5.0 files with `_managed_by` and `schema_version: "0.3"`; no legacy files). Pre-flight classifies as `✓ Compatible`, finds no legacy files, and skips migration silently. The requested operation proceeds.
2. **Coexistence state** (the operator downloaded the new files and uploaded them but has not yet deleted the legacy files). Per section 2, legacy migration runs again — but this time it finds the legacy content already present in the v0.5.0 files and most candidates classify as NOOP (reinforcement) or are dropped as duplicates. The brief reminds the operator to delete the named legacy files. This is safe re-entry, not a separate prompt.
3. **Pure-legacy state** (operator skipped the upload step or is running migration for the first time). Migration produces the three new v0.5.0 files; the brief lists the legacy files for deletion.

## 7. Edge cases (legacy migration)

| Edge case | Behavior |
|---|---|
| Legacy file with no `schema_version` field | Treated as legacy if the filename matches the legacy pattern. Fail loudly if no detected schema_version and no matching filename. |
| Mixed-version legacy files (some v0.1, some v0.3.2) | Migrated together. All legacy files share the same v0.1 schema regardless of skill-version string in `schema_version` — see `references/schema-changelog.md`. |
| Legacy `consolidated` file | Migrated like any other legacy file. The `consolidation_summary` block is dropped; an archive checkpoint records the migration. |
| Legacy file whose body does not conform to schema "0.1" | Pre-flight warns the operator and asks whether to attempt best-effort migration or skip the file. |
| Two legacy records with identical content but different governance | Merge into one v0.5.0 record. The most-restrictive governance value wins. |
| Legacy `related_session_recap` field | Preserved on the new `project-context.md` if present on any legacy file. If multiple legacy files reference different session-recaps, the most-recent reference wins. |

## 8. Cross-references (legacy migration)

- Schema "0.1" field set: `references/schema-changelog.md`.
- Schema "0.3" target: `references/schema.md`.
- Scoring driving the active/archive split: `references/scoring.md`.
- Pre-flight invoking migration: `references/preflight.md`.

---

## 9. Upgrade migration (v0.4.0 → v0.5.0)

The upgrade migration is the new path introduced in v0.5.0. It handles projects that already have a v0.4.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at schema "0.2") and need to be brought to schema "0.3" so the pre-flight `_managed_by` detection works.

### 9.1 Detection criteria

Per section 1 step 2: pre-flight identifies upgrade-available files by all three signals:

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
4. **Preserve all other frontmatter fields and all body content unchanged.** No record-level fields are modified, no records are added or removed, no `update_count` increment, no `last_merged` update — the upgrade is metadata-only.
5. **Optional: update `generated_by.version`** to `"0.5.0"` since the file is being rewritten under the v0.5.0 skill. (This is informational; `_managed_by` and `schema_version` are the authoritative version signals.)
6. **Emit the modified file** as a proposed write.

### 9.4 Post-flight summary

Per `references/preflight.md` section on post-flight, the post-flight summary for upgrade migration takes this shape:

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
- It does NOT change the `last_merged` timestamp. (Operators auditing the file history can identify the upgrade event by the version bump in `generated_by.version` if that field was updated; otherwise the schema-version bump itself is the marker.)
- It does NOT alter the `created` timestamp.

### 9.7 Idempotency (upgrade migration)

If pre-flight is invoked again on a project that has already been upgraded (schema "0.3" with `_managed_by` present on all three files), step 1 of the detection routes the project to `✓ Compatible` and no upgrade migration runs. Re-running upgrade against an already-upgraded project is a no-op by classification.

If the operator partially upgraded (e.g., uploaded the new `project-context.md` but kept the old `entities.md`), pre-flight will see mixed schema versions: one file matches step 1 (CURRENT), two match step 2 (UPGRADE_AVAILABLE). This is a partial state. Resolution: re-run upgrade migration, which will leave the already-upgraded file untouched (step 1 routes it to CURRENT, the operation does not re-modify it) and complete the remaining files.

### 9.8 Edge cases (upgrade migration)

| Edge case | Behavior |
|---|---|
| Canonical filename at schema "0.2" but with a stray `_managed_by` field (operator hand-edit?) | Pre-flight surfaces ambiguity. Treat the file as malformed; halt and ask the operator. |
| Canonical filename at schema "0.2" but `_managed_by` set to something other than `project-context-skill` (a different skill claiming management?) | Pre-flight halts and asks the operator to identify the rightful manager. Do not silently overwrite a marker belonging to another skill. |
| Three canonical filenames present but mixed schema_versions (e.g., one at 0.2, one at 0.3, one missing) | `⚠ Partial State`. Surface to operator with rebuild-or-fresh choice. |
| Upgrade fails mid-write (e.g., second of three files cannot be written) | Post-flight emits `✗ Failed` verdict with diagnostic. Operator instructions for partial-state recovery: re-run upgrade migration; idempotency (9.7) handles already-upgraded files. |

## 10. Cross-references (all migrations)

- Schema definition and validation checklist: `references/schema.md`.
- Schema-changelog and Supported Schemas matrix: `references/schema-changelog.md`.
- Pre-flight algorithm, report block, token catalog, post-flight summary: `references/preflight.md`.
- Scoring algorithm driving the legacy migration's active/archive split: `references/scoring.md`.
