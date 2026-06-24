---
file_role: skill-operation
operation: compact
schema_version_documented: "0.4"
skill_version: "0.6.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operation: compact

## Pre-flight prerequisite

The operations in this document apply only after pre-flight (`references/preflight.md`) has completed and operator confirmation (where required by the verdict) has been received. Operations described here assume a valid, classified project state. Do not execute these operations without pre-flight completion.

`compact` is an operator-invoked operation that explicitly demotes weak records from the active file (`project-context.md`) to the archive. It scores every active record and proposes DEMOTE for everything below `demotion_threshold`. It does NOT parse the current conversation.

Invocation phrases routing to this operation: "compact", "compact this", "compact the project context", "trim the project context", "consolidate". Routing is handled by `SKILL.md`.

The use case: the operator notices the active file is between `target` and `soft_warning` (default 30K-50K tokens) and wants to clean up before the file gets bloated, or the operator wants more aggressive cleanup than the default operation's automatic DEMOTE pass tends to produce.

## 1. Pre-flight prologue

Identical to `operations/default.md` section 1 (surface guard → project detection → file discovery → schema verification → migration trigger if needed → configuration resolution).

Additionally for `compact`:

- Require `project-context.md` to exist with at least one record. If it does not exist or has zero active records, halt with: "Nothing to compact — the active file has no records."

## 2. Score every active record

Read `project-context.md` and compute weight for every record using the formula from `references/scoring.md`:

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

- Remove the record from `project-context.md`.
- Append it to `project-context-archive.md` with:
  - Fresh `arc-` ID.
  - `prior_id` = the original ID.
  - `status: archived`.
  - `demoted_at_update = current_update`.
  - All lifecycle fields and audit block preserved.

After applying:

1. Increment `update_count` on `project-context.md` and `project-context-archive.md`.
2. Update `last_merged` on both.
3. Recompute `record_count` on both.
4. Append a checkpoint to the archive's `checkpoints` array: `summary: "Compact: N records demoted."`.
5. Run the validation checklist from `references/schema.md` section 6 on both files.

`entities.md` is not touched by `compact`. Entity decay is not part of v0.6.0; see `ROADMAP.md`.

## 7. Operator brief

```
✅ **Compact complete.**

📥 **Download** these updated files:
   • project-context.md  (12 records removed; new size: ~28K tokens, down from ~46K)
   • project-context-archive.md  (12 records added; now 47 archived total)

📂 **Upload** to your Project, replacing the prior versions.

🔔 If a demoted record turns out to still be needed, it lives in the
   archive with `restore_command: "restore arc-NNN"`. Invoking that
   command in a future session brings it back to active.
```

Append `downstream_chaining` instructions from `org-config.md` if any apply (`after_compact`, `after_any`).

## 8. Failure handling

| Failure | Handling |
|---|---|
| `project-context.md` does not exist | Halt: "Nothing to compact." |
| Zero records below threshold | Emit a one-line brief: "Nothing to compact — every active record is above the demotion threshold." Do not write files. |
| Operator cancels mid-flow | Stop. Do not write. |
| Validation fails on the rewritten files | Halt; report the validation error; do not surface files to operator. |

## 9. Cross-references

- Default operation: `operations/default.md`.
- Scoring formula: `references/scoring.md`.
- Common operation logic: `references/operations.md`.
- Schema, defaults, configuration: see `operations/default.md` section 11.
