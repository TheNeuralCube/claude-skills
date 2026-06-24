---
file_role: skill-operation
operation: compact
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operation: compact

## Pre-flight prerequisite

The operations in this document apply only after pre-flight (`references/preflight.md`) has completed and operator confirmation (where required by the verdict) has been received. Operations described here assume a valid, classified project state. Do not execute these operations without pre-flight completion.

`compact` is an operator-invoked operation that explicitly demotes weak records from the active file (`pc-NNNN-context.md`) to the archive. It scores every active record and proposes DEMOTE for everything below `demotion_threshold`. It does NOT parse the current conversation.

Invocation phrases routing to this operation: "compact", "compact this", "compact the project context", "trim the project context", "consolidate". Routing is handled by `SKILL.md`.

The use case: the operator notices the active file is between `target` and `soft_warning` (default 30K-50K tokens) and wants to clean up before the file gets bloated, or the operator wants more aggressive cleanup than the default operation's automatic DEMOTE pass tends to produce.

## 1. Pre-flight prologue

Identical to `operations/default.md` section 1 (surface guard → project detection → file discovery → schema verification → migration trigger if needed → configuration resolution).

Additionally for `compact`:

- Require `pc-NNNN-context.md` to exist with at least one record. If it does not exist or has zero active records, halt with: "Nothing to compact — the active file has no records."

## 2. Score every active record

Read `pc-NNNN-context.md` and compute weight for every record using the formula from `references/scoring.md`:

```
weight_i = alpha   * log(1 + times_seen_i)
         + beta    * importance_i
         + gamma   * exp(-lambda * (current_update - last_seen_update_i))
         - delta   * exp(-lambda * (current_update - first_seen_update_i))
         - epsilon * max(0, wall_clock_years_i - 3)
```

Use the effective coefficients (after `user-config.md` and `org-config.md` resolution).

## 3. Build the DEMOTE batch

Collect every record with `weight < demotion_threshold` (default 5). For each, prepare a DEMOTE proposal that includes:

- The record ID and content.
- The current weight (rounded to one decimal).
- A one-line rationale: which factors drove the weight down (low `times_seen`, large `last_seen_update` gap, low `importance`, wall-clock age, etc.).

Records with weight `>= demotion_threshold` are NOT proposed. `compact` is conservative: it does not propose UPDATE, SUPERSEDE, or ADD.

## 4. Optional batch-cap raise

The default `proposal_cap_per_session` is 10. For `compact`, that cap may be limiting (a file with many marginal records can produce 20+ DEMOTE candidates). The operator explicitly invoked `compact` to deal with backlog, so raise the cap for this operation:

- Compute the total number of DEMOTE candidates.
- If the count exceeds `proposal_cap_per_session`, raise the effective cap to `min(total_candidates, 25)`. Tell the operator: "Found 18 records below threshold; showing all 18 (default cap was 10)."
- If the count exceeds 25, show the top 25 by lowest weight (most aggressive demotions first) and offer to surface the rest in a follow-up `compact` after the first batch is approved.

**Large-compact gate.** A compact whose batch exceeds `proposal_cap_per_session` is a "large compact" and is destructive-tier per `references/preflight.md` section 4.6: pre-flight renders the blocking model-setup gate before the batch proceeds. A routine compact (batch within the cap) is advisory-only. The threshold for "large" is the same cap the batch raise keys off, so the determination is already computed here.

## 5. Diff-and-approve flow

Show the DEMOTE batch in a single proposal block. Severity marker is 🟡 unless any record being demoted has `times_seen >= 5` or `importance >= 8` — in that case 🔴 (the threshold is unusually pushing a record that has been reinforced or rated highly; the operator should sanity-check).

```
🟡 **Compact proposals.** 12 records below threshold (5.0):

  📦  DEMOTE   #1  arc weight 2.1 — dec-018 ("Use v1 customer ID schema")
                   (last seen update 11; 22 updates ago; importance 4)
  📦  DEMOTE   #2  arc weight 3.4 — csn-005 ("Migration is 40% complete")
                   (superseded conceptually by csn-011; importance 5)
  ...
  📦  DEMOTE   #12 arc weight 4.8 — opn-003 ("Schedule mid-quarter check-in")
                   (completed long ago; not reinforced in 18 updates)

Reply with: "all" to demote, "skip 1 5" to keep those, or
"explain 7" to see the source quote.
```

Accept the same approval grammar as `operations/default.md` section 6.4 (`all`, `skip N M`, `only N M`, `explain N`, `cancel`).

## 6. Apply approved demotions and write files

For each approved DEMOTE:

- Remove the record from `pc-NNNN-context.md`.
- Append it to `pc-NNNN-archive.md` with:
  - Fresh `arc-` ID.
  - `prior_id` = the original ID.
  - `status: archived`.
  - `demoted_at_update = current_update`.
  - All lifecycle fields and audit block preserved.

After applying:

1. Increment `update_count` (the scoring counter) on `pc-NNNN-context.md` and `pc-NNNN-archive.md` (the touched files).
2. Update `last_merged` on the files written.
3. Recompute `record_count` on the touched files.
4. Append a checkpoint to the archive's `checkpoints` array: `summary: "Compact: N records demoted."`.
5. **Stamp `generation = N`** (the counter assigned at pre-flight per `references/preflight.md` section 3.4) on all three files and **write all three under `pc-000N-{context,entities,archive}.md`** so the canonical set advances together. `pc-NNNN-entities.md` is not content-changed by `compact` (its `update_count` does not increment) but is re-stamped to generation `N` and re-written under the new name so the set stays at one counter.
6. Run the validation checklist from `references/schema.md` section 6 on every file written (including the generation self-consistency check).

`compact` makes no content change to `pc-NNNN-entities.md`. Entity decay is not yet part of the skill; see `ROADMAP.md`.

## 7. Operator brief

```
✅ **Compact complete.** (generation 5)

📥 **Download** the current generation's files:
   • pc-0005-context.md  (12 records removed; new size: ~28K tokens, down from ~46K)
   • pc-0005-archive.md  (12 records added; now 47 archived total)
   ℹ pc-0005-entities.md — content unchanged, re-stamped to generation 5;
     download and upload it too so the set stays at one counter.

📂 **Upload** the pc-0005-* set to your Project, then follow the set-integrity
   directive rendered in the post-flight summary above (canonical wording in
   references/preflight.md section 9.6).

🔔 If a demoted record turns out to still be needed, it lives in the
   archive with `restore_command: "restore arc-NNN"`. Invoking that
   command in a future session brings it back to active.
```

The set-integrity directive is owned canonically by `references/preflight.md` section 9.6 and rendered by post-flight; this brief points at it rather than restating the replace wording.

Append `downstream_chaining` instructions from `org-config.md` if any apply (`after_compact`, `after_any`).

## 8. Failure handling

| Failure | Handling |
|---|---|
| `pc-NNNN-context.md` does not exist | Halt: "Nothing to compact." |
| Zero records below threshold | Emit a one-line brief: "Nothing to compact — every active record is above the demotion threshold." Do not write files. |
| Operator cancels mid-flow | Stop. Do not write. |
| Validation fails on the rewritten files | Halt; report the validation error; do not surface files to operator. |

## 9. Cross-references

- Default operation: `operations/default.md`.
- Scoring formula: `references/scoring.md`.
- Common operation logic: `references/operations.md`.
- Schema, defaults, configuration: see `operations/default.md` section 11.
