---
file_role: skill-reference
topic: migration
schema_version_documented: "0.2"
skill_version: "0.4.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Migration from v0.1 schema (project-context v0.4.0)

This file documents the one-time, per-project migration path from the schema "0.1" used by skill versions v0.1.0 through v0.3.2 to the schema "0.2" used by skill version v0.4.0 and forward. The pre-flight prologue of every operation checks for legacy files; this file is the algorithm those operations cite.

For the history of what was actually written under "0.1", including the unquoted-skill-version-as-schema_version accident, see `references/schema-changelog.md`.

## 1. Detection

Pre-flight scans the project for files matching either:

- The legacy filename pattern: `*-project-context*.md` (dated, optionally topic-suffixed, including `-consolidated[-N]` variants).
- A `file_type: project-context` value in the YAML frontmatter.

For every match, parse the frontmatter `schema_version` field and run the **two-step check** below, in this exact order. The first step exists because the legacy regex (step 2) is broad enough to match the current schema literal `"0.2"`; the current-schema short-circuit prevents that.

**Step 1 — Current-schema short-circuit.** If the file's `schema_version` is exactly the string `"0.2"` (quoted, short, no leading `v`), the file is a v0.4.0+ current-schema file. Skip migration for this file; treat it as a normal v0.4.0 file (pre-flight continues with schema verification per `references/operations.md` section 4). Do NOT evaluate step 2 for this file.

**Step 2 — Legacy regex (only if step 1 did not short-circuit).** Treat the file as legacy if its `schema_version` matches any of these forms (the same data shape, serialized differently across releases):

```
v0.1, v0.1.0, v0.1.x, 0.1, 0.1.0, "0.1", "v0.1.0",
v0.2, v0.2.0, v0.2.x, 0.2, 0.2.0, "0.2.0",   # note: SHORT "0.2" already handled by step 1
v0.3, v0.3.0, v0.3.x, v0.3.1, v0.3.2, 0.3, 0.3.0, 0.3.1, 0.3.2
```

In regex form: `^"?v?0\.(1|2|3)(\.\d+)?"?$` (evaluated only after the step-1 short-circuit). The regex is intentionally permissive about quoting and the leading `v` because v0.1.0-v0.3.2 serialized this field in multiple shapes (see `references/schema-changelog.md`).

**Disambiguation note.** The literal string `"0.2"` (quoted, short, no `v`) is the v0.4.0 schema "0.2" marker — handled by step 1, never reaches step 2. Legacy v0.2.0 wrote `schema_version: v0.2.0` (unquoted, full version, with leading `v`) — does not match step 1, matches step 2 → legacy.

If a file's `schema_version` does not pass step 1 AND does not match the step 2 regex, pre-flight halts and asks the operator to identify the file.

Pseudocode for clarity:

```
def classify_for_migration(schema_version):
    # Step 1 — current-schema short-circuit
    if schema_version == '"0.2"' or schema_version == '0.2':   # quoted or bare short form
        return CURRENT     # skip migration; treat as v0.4.0+ file
    # Step 2 — legacy regex (only reached when step 1 did not return)
    if re.match(r'^"?v?0\.(1|2|3)(\.\d+)?"?$', schema_version):
        return LEGACY      # candidate for migration
    return UNKNOWN         # halt; ask the operator
```

## 2. Migration trigger

Migration runs whenever one or more legacy files are detected, **regardless of whether v0.4.0 files coexist**. The three project states pre-flight may observe:

| Project state | Migration trigger |
|---|---|
| **Pure-legacy** — one or more legacy files; no v0.4.0 files | Migrate. |
| **Coexistence** — one or more legacy files AND one or more v0.4.0 files | Migrate. The migration merges legacy content into the existing v0.4.0 files (using the same classifier and scoring as a normal session). The operator's safety net is the brief's `download → verify → delete old → upload new` ordering: nothing is deleted from the Project until the operator has reviewed the merged output. |
| **Pure-current** — only v0.4.0 files; no legacy files | No-op. Pre-flight continues into the requested operation normally. |

Pre-flight does NOT ask a separate coexistence question. The unified ordering of the operator brief (section 4 below) is the review gate; an additional prompt would duplicate that gate without adding safety.

Migration is one-time per legacy file. After the operator follows the brief's required ordering — verifying the merged output and deleting the named legacy files — re-running pre-flight in the same project finds no legacy files and falls into the pure-current state.

## 3. Migration algorithm

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

   The `update_count` value `0` is intentional: migration is the bootstrap state before any v0.4.0 update has occurred. The first post-migration session increments `update_count` to `1`.

4. **Infer `importance` from legacy tier:**

   | Legacy tier | Inferred `importance` |
   |---|---|
   | `full` (or section default for full-tier sections) | `8` |
   | `summary` (or section default for summary-tier sections) | `5` |
   | `transient` | record is DROPPED, not migrated (transient meant "should not survive consolidation") |

   The user can adjust importance via the diff-and-approve flow on the first post-migration session if needed.

5. **Translate inline category tags** to `links` and `source_quote` where they map; otherwise drop them. v0.4.0 does not have an open-category system. Where a legacy category clearly identified a related entity (e.g., `[categories: customer]` against a record naming Acme Corp), add a `link` to the entity record after entities are imported.

6. **Source quote:** if the legacy record was a single sentence, use it verbatim as `source_quote`. If it was longer, capture the first sentence as `source_quote` and store the full content in `content`.

7. **Source ref:** use the legacy filename as `source_ref`. `source_kind: chat`.

8. **Apply update-based scoring** to determine which migrated records go where:
   - `weight >= demotion_threshold` → `project-context.md`.
   - `weight < demotion_threshold` → `project-context-archive.md` with `status: archived`, `demoted_at_update: 0`.

   With `first_seen_update = last_seen_update = 0` and `current_update` starting at `1` post-migration, the recency boost is meaningful only for records with high `importance` and `times_seen > 1` (reinforcement during migration when the same record appears in multiple legacy files).

9. **Deduplicate across legacy files.** When the same record appears in multiple legacy files (recognized by semantic similarity), merge into one v0.4.0 record with `times_seen` set to the count of appearances. `first_seen_at` is the earliest legacy file's `created`; `last_seen_at` is the most recent.

10. **Initialize the archive `checkpoints` array** with one entry summarizing the migration:

    ```yaml
    checkpoints:
      - update: 0
        timestamp: <migration timestamp>
        summary: "Migrated from N legacy v0.1 file(s). M records imported, K dropped (transient tier)."
        approver: null
    ```

11. **Write the three v0.4.0 files** with `update_count: 0`, `record_count` set to actual counts, and `schema_version: "0.2"`.

## 4. The operator brief

Migration is surfaced via the operator brief as a distinct flow. The skill **does not** delete legacy files automatically (Claude Project APIs do not expose file deletion in May 2026). The brief instructs the operator with the required order of operations:

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

## 5. What migration deliberately does NOT do

- It does not delete legacy files from the Project. Only the operator can do that.
- It does not preserve legacy inline-bracket metadata exactly. Tier and categories are mapped to v0.4.0 equivalents (`importance`, structural sections, links) — they are lossy translations by design.
- It does not preserve legacy file-level `audience` or non-v0.4.0 governance fields. These were only used by org-config and the migration does not attempt to re-derive them.
- It does not migrate `consolidation_summary` blocks. Those were per-file artifacts of the v0.1 consolidate mode; v0.4.0 captures equivalent information in the archive `checkpoints` array.
- It does not migrate records whose legacy tier was `transient` — those were explicitly opt-out of consolidation in the legacy model.

## 6. Idempotency

Pre-flight behavior on a project that may have been partially or fully migrated:

1. **Pure-current state** (only v0.4.0 files; no legacy files). Pre-flight detects `schema_version: "0.2"` on all files, finds no legacy files, and skips migration silently. The requested operation proceeds.
2. **Coexistence state** (the operator downloaded the new files and uploaded them but has not yet deleted the legacy files). Per section 2, migration runs again — but this time it finds the legacy content already present in the v0.4.0 files and most candidates classify as NOOP (reinforcement) or are dropped as duplicates. The brief reminds the operator to delete the named legacy files. This is safe re-entry, not a separate prompt.
3. **Pure-legacy state** (operator skipped the upload step or is running migration for the first time). Migration produces the three new files; the brief lists the legacy files for deletion.

## 7. Edge cases

| Edge case | Behavior |
|---|---|
| Legacy file with no `schema_version` field | Treated as legacy if the filename matches the legacy pattern. Fail loudly if no detected schema_version and no matching filename. |
| Mixed-version legacy files (some v0.1, some v0.3.2) | Migrated together. All legacy files share the same v0.1 schema regardless of skill-version string in `schema_version` — see `references/schema-changelog.md`. |
| Legacy `consolidated` file | Migrated like any other legacy file. The `consolidation_summary` block is dropped; an archive checkpoint records the migration. |
| Legacy file whose body does not conform to schema "0.1" | Pre-flight warns the operator and asks whether to attempt best-effort migration or skip the file. |
| Two legacy records with identical content but different governance | Merge into one v0.4.0 record. The most-restrictive governance value wins. |
| Legacy `related_session_recap` field | Preserved on the new `project-context.md` if present on any legacy file. If multiple legacy files reference different session-recaps, the most-recent reference wins. |

## 8. Cross-references

- Schema "0.1" field set: `references/schema-changelog.md`.
- Schema "0.2" target: `references/schema.md`.
- Scoring driving the active/archive split: `references/scoring.md`.
- Pre-flight invoking migration: `operations/default.md`.
