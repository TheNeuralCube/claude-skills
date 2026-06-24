---
file_role: skill-operation
operation: rebuild
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operation: rebuild

## Pre-flight prerequisite

The operations in this document apply only after pre-flight (`references/preflight.md`) has completed and operator confirmation (where required by the verdict) has been received. Operations described here assume a valid, classified project state. Do not execute these operations without pre-flight completion.

`rebuild` reconstructs `pc-NNNN-context.md` from the archive (`pc-NNNN-archive.md`) using the current scoring algorithm. It is a recovery operation, not a routine one.

Invocation phrases routing to this operation: "rebuild", "rebuild from archive", "reset from archive", "reset project context", "regenerate project context". Routing is handled by `SKILL.md`.

Use cases:

- The active file was accidentally edited or corrupted; rebuild restores a coherent version from the archive's history.
- The user has tuned scoring coefficients in `user-config.md` and wants the active/archive split recomputed under the new settings.
- The user wants to apply a new schema or scoring version retroactively.

**`rebuild` is the only operation where review-before-commit is mandatory regardless of `merge_policy`.** Auto-mode does not bypass this gate. The reason: `rebuild` is destructive to the active file — getting it wrong replaces good data with stale archive records, and the operator must confirm.

## 1. Pre-flight prologue

Identical to `operations/default.md` section 1, with one addition:

- Require `pc-NNNN-archive.md` to exist with at least one record. If it does not exist or has zero records, halt with: "Nothing to rebuild from — the archive is empty. Use the default operation to start producing records."

## 2. Read and score the archive

Load every archive record. For each, compute `weight` using the **current** scoring algorithm (formula + coefficients from `references/scoring.md`, with any `user-config.md` / `org-config.md` overrides):

```
weight = alpha   * log(1 + times_seen)
       + beta    * importance
       + gamma   * exp(-lambda * (current_update - last_seen_update))
       - delta   * exp(-lambda * (current_update - first_seen_update))
       - epsilon * max(0, wall_clock_years - 3)
```

The archive records' lifecycle fields (`first_seen_update`, `last_seen_update`, etc.) are preserved from when they were originally active. `current_update` is the archive file's `update_count` at rebuild time.

## 3. Partition

For each scored archive record:

- `weight >= demotion_threshold` → candidate for promotion to the new active file.
- `weight < demotion_threshold` → stays archived.

Within the promotion candidates, group by `prior_id`'s section so we know which section each one belongs in. Resolve duplicates: if multiple archived versions of the same `prior_id` qualify for promotion, promote only the most recent (highest `last_seen_update`).

Records whose status was `superseded` and whose `superseded_by` still exists in the archive (because the superseding record was itself archived) are skipped — the supersession is itself stale, and we do not want to resurrect both versions.

## 4. Build the candidate active file

Construct a candidate `pc-NNNN-context.md` (where `N` is the generation counter assigned at pre-flight per `references/preflight.md` section 3.4) containing:

- Frontmatter cloned from the existing `pc-NNNN-context.md` if it exists, otherwise fresh frontmatter per `references/schema.md`. Bump `update_count` by 1 (the scoring counter). Set `generation` to the new `N` (identity counter; distinct from `update_count`). Set `last_merged` to now.
- Body sections per the file's `read_order`, populated with the promoted records.
- For each promoted record:
  - Restore the original ID (the `prior_id` from the archive record). If that ID is now in use by a different record in the existing active file (rare, but possible after manual edits), generate a fresh sequential ID in the section's prefix.
  - Set `status: active`.
  - Preserve lifecycle fields (`first_seen_update`, `last_seen_update`, etc.) as-is.
  - Drop archive-only fields (`prior_id`, `superseded_by`, `superseded_at_update`, `demoted_at_update`, `restore_command`).
  - Preserve the audit block as-is. Rebuild traceability is captured in the archive's `checkpoints` frontmatter array (see step 6 below), not in per-record audit fields. The schema (`references/schema.md`) does not define a per-record rebuild marker.

## 5. Show the rebuilt file BEFORE committing

This is the mandatory content review gate. Even under `merge_policy: auto`, the rebuilt file MUST be shown to the operator before it replaces the existing active file. Separately, `rebuild` is destructive-tier per `references/preflight.md` section 4.6: pre-flight renders the blocking model-setup gate at operation start (confirm the strongest thinking-capable model with extended thinking) before the rebuild runs. The two gates are complementary: the model-setup gate fires at pre-flight; this content review fires before commit.

Brief template:

```
🔁 **Rebuild preview.** I rebuilt pc-NNNN-context.md from the archive.

  Promoted from archive: 18 records
  Stayed archived:        29 records
  Existing active file:   will be REPLACED on your approval

Section breakdown (rebuilt active):
   Decisions:            7 records
   Constraints:          3 records
   Current State:        2 records
   Open Items:           1 record
   Terminology:          4 records
   External References:  1 record

Top promotions (highest weight first):
  1. dec-001 (weight 17.3) "Adopt the four-segment customer model..."
  2. con-003 (weight 12.1) "Tier-2 enterprise pricing review..."
  ...
  18. trm-009 (weight 5.1)  "Tier 1 enterprise = ARR > $1M..."

Reply with: "approve" to commit, "preview" to see the full rebuilt file,
"explain N" to see record details, or "cancel" to abort.
```

The operator MUST type `approve` (or equivalent affirmative) before the commit happens. `auto`, `accept`, `yes`, `go ahead` are accepted. Anything else, including silence or `whatever`, is treated as cancel. This is intentionally stricter than the default operation's auto-mode handling because `rebuild` is destructive.

## 6. Commit the rebuild

On approval, write the new generation `N` (the counter assigned at pre-flight):

1. Write the candidate file as `pc-000N-context.md` (it replaces the prior generation's context file as the canonical active file).
2. Write `pc-000N-archive.md`:
   - The records promoted out of the archive remain in the archive body. Do NOT delete them. The archive is append-only; the source-of-truth invariant is that nothing is ever removed from the archive. The promoted records now appear in BOTH files, with the archive copy carrying its original `arc-` ID and `status: archived`.
   - **The archive record's `audit` block is preserved as-is.** Do not mutate any per-record audit field (including `approval_mode`, `approved_by`, `approved_at`, `warning_response`, `importance_source`) for a rebuild event. The schema (`references/schema.md`) does not define a per-record rebuild marker, and rebuild traceability lives **only** in the file-level `checkpoints` array in YAML frontmatter — never on individual records.
   - Append a checkpoint to the archive's `checkpoints` array: `summary: "Rebuild: <count> records promoted from archive; <count> stayed archived."`. This is the sole rebuild trace.
   - Increment the archive's `update_count` (scoring counter).
3. `pc-000N-entities.md`: entities are not content-changed by `rebuild`, but the file is re-stamped to generation `N` and re-written under the new name so the canonical set stays at one counter. Its `update_count` is unchanged.
4. **Stamp `generation = N` on all three files.** The set advances together; `update_count` moves only on the touched files (context and archive).
5. Run the validation checklist from `references/schema.md` section 6 on every file written (including the generation self-consistency check).

## 7. Operator brief

```
✅ **Rebuild complete.** (generation 6)

📥 **Download** the current generation's files:
   • pc-0006-context.md  (REBUILT — 18 records, ~24K tokens)
   • pc-0006-archive.md  (checkpoint added; archive body unchanged)
   ℹ pc-0006-entities.md — content unchanged, re-stamped to generation 6;
     download and upload it too so the set stays at one counter.

📂 **Upload** the pc-0006-* set to your Project. Then follow the set-integrity
   directive rendered in the post-flight summary above (canonical wording in
   references/preflight.md section 9.6).

🔔 Keep the prior generation's set until you confirm the rebuilt version
   looks correct. If something is wrong, the prior pc-MMMM-* set is still
   intact and you can fall back to it. Once verified, delete the prior set
   per the set-integrity directive.
```

The set-integrity directive is owned canonically by `references/preflight.md` section 9.6 and rendered by post-flight; this brief points at it rather than restating the replace wording.

Append `downstream_chaining` instructions from `org-config.md` if any apply (`after_rebuild`, `after_any`).

## 8. Failure handling

| Failure | Handling |
|---|---|
| Archive does not exist or is empty | Halt: "Nothing to rebuild from." |
| All archive records score below threshold | Halt with explanation: "Every archive record scores below the demotion threshold. The rebuild would produce an empty active file. Lower the threshold in user-config.md or invoke the default operation to add fresh records." |
| Operator does not approve | Stop. Do not write. Do not modify the existing active file. |
| Validation fails on the rebuilt file | Halt; report; do not commit. Existing active file remains untouched. |

## 9. Cross-references

- Default operation: `operations/default.md`.
- Scoring formula: `references/scoring.md`.
- Common operation logic and the rebuild summary: `references/operations.md`.
- Schema (especially the archive `restore_command` field): `references/schema.md`.
- Defaults, configuration, migration: see `operations/default.md` section 11.
