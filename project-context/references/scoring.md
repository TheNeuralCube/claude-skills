---
file_role: skill-reference
topic: scoring
schema_version_documented: "0.2"
skill_version: "0.4.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Scoring algorithm (project-context v0.4.0)

This file is the authoritative restatement of the scoring algorithm used by the project-context skill to decide which records stay in the active file (`project-context.md`) and which are proposed for demotion to the archive (`project-context-archive.md`).

Operations reference this file. The user can tune the algorithm in `user-config.md` (see `references/user-config-template.md`). Defaults come from `references/defaults.md`.

## 1. The weight formula

For every active record `i`, compute:

```
weight_i = alpha   * log(1 + times_seen_i)
         + beta    * importance_i
         + gamma   * exp(-lambda * (current_update - last_seen_update_i))
         - delta   * exp(-lambda * (current_update - first_seen_update_i))
         - epsilon * max(0, wall_clock_years_i - 3)
```

Symbols:

| Symbol | Meaning |
|---|---|
| `times_seen_i` | Per-record count of reinforcements (every NOOP/UPDATE/SUPERSEDE that touches the record increments it; ADD initializes to 1). |
| `importance_i` | Per-record integer 1-10 assigned by the model at ingest, optionally overridden by the user. |
| `current_update` | The file's `update_count` at the moment of scoring (post-increment for the current session). |
| `last_seen_update_i` | The `update_count` value when the record was last reinforced. |
| `first_seen_update_i` | The `update_count` value when the record was first added. |
| `wall_clock_years_i` | Wall-clock age of the record in years, computed from `first_seen_at`. |

## 2. Coefficient defaults

| Coefficient | Default | Meaning |
|---|---|---|
| `alpha` | `1.5` | Each doubling of `times_seen` adds approximately one unit of weight. |
| `beta` | `1.0` | One point of importance (on the 1-10 scale) maps to one unit of weight. |
| `gamma` | `5.0` | A record reinforced this session receives up to ~5 units of recency boost. |
| `delta` | `2.0` | A record never reinforced since creation loses up to ~2 units. |
| `epsilon` | `0.5` | A record older than 3 years (wall-clock) loses 0.5 units per year past 3. |
| `lambda` | `0.0347` (= ln(2)/20) | Decay rate. The exponential terms have a 20-update half-life. |
| `demotion_threshold` | `5` | Records with `weight < 5` are proposed for DEMOTE. |

All coefficients are overridable in `user-config.md` and `org-config.md`. Resolution order: user-config > org-config > skill default. See `references/defaults.md` for the single source of truth.

## 3. Demotion threshold

Default: `weight < 5` triggers a DEMOTE proposal. The default operation runs the scoring pass at the end of every session; the explicit `compact` operation runs it on demand against the same threshold.

DEMOTE is a hybrid-brake-gated operation: it requires operator approval before the record moves to the archive. Auto-mode auto-approves DEMOTE per the published auto-mode warning flow (`operations/default.md`, section "Auto-mode").

## 4. Update-based decay rationale

The decay terms (`gamma` and `delta`) are measured in **file updates**, not wall-clock time. Every successful merge increments `update_count` by one. A record's recency is computed against `current_update`, not against today's date.

This has two consequences:

1. A project used daily and a project used monthly age records at different calendar rates but the same activity rate. A project untouched for six months sees zero updates and therefore zero decay during the gap.
2. The skill is robust to bursty usage. A flurry of sessions in one week does not artificially age records that haven't been displaced; only records that were not reinforced during the burst lose ground.

The wall-clock floor (`epsilon`) provides a small absolute-age penalty for records older than 3 years, regardless of activity. This handles the edge case of long-dormant projects with records that should be considered stale even if no activity has displaced them.

## 5. Worked examples

The four profiles below illustrate how the formula behaves at the default coefficients (taken verbatim from design spec section 11.5).

| Record profile | `times_seen` | `importance` | last-seen gap (updates) | first-seen gap (updates) | wall-clock age | weight |
|---|---|---|---|---|---|---|
| Core fact, recently active | 20 | 9 | 0 | 30 | 60 days | ~17.5 |
| Stale, low-importance | 1 | 3 | 25 | 30 | 90 days | ~4.6 |
| New addition | 1 | 5 | 0 | 0 | 0 | ~9.0 |
| Old archived candidate | 8 | 7 | 22 | 80 | 4 years | ~6.8 |

The stale record demotes at threshold 5. The other three stay active. Of these:

- The core fact has both high reinforcement (`times_seen=20`) and recent activity (gap 0) plus high importance — it carries the most weight by a wide margin.
- The new addition starts with a strong recency boost (gap 0) and middling importance.
- The old archived candidate is borderline: it has wall-clock penalty plus a 22-update gap, but its `times_seen=8` and `importance=7` keep it above threshold.

## 6. When the model assigns `importance`

The skill assigns `importance` at ingest based on the candidate record's content and context. Rough guideposts (not strict bands):

| Range | Typical content |
|---|---|
| 1-3 | Conversational scaffolding, recap, low-stakes details. |
| 4-6 | Useful state, in-flight reasoning, intermediate facts. |
| 7-8 | Decisions, named entities, agreed terminology, key constraints. |
| 9-10 | Foundational decisions and constraints the project pivots on. |

The user can override the score on a per-record basis via the diff-and-approve flow ("Set importance: 9"). When the user overrides, the record's `audit.importance_source` is stamped `user-override`; otherwise it is `llm-auto`.

## 7. Anti-patterns

- **Do not** treat `importance` as the only signal. The formula combines five factors deliberately. A high-importance record that is never reinforced will still decay.
- **Do not** lower `demotion_threshold` to keep more records active. The active file's size budgets exist because large files degrade grounding fidelity on the indirect-user (downstream AI) side. Use `compact` and rely on the archive instead.
- **Do not** raise coefficients to keep marginal records active. If a record matters, the user should reinforce it (mention it) or override its importance through the approval flow.

## 8. Cross-references

- Schema for `times_seen`, `importance`, `first_seen_update`, `last_seen_update`, `first_seen_at`: see `references/schema.md`.
- Where the formula is invoked: `operations/default.md` (end-of-session pass), `operations/compact.md` (on-demand batch), `operations/rebuild.md` (rebuild from archive).
- Where defaults can be overridden: `references/user-config-template.md`, `references/org-config-template.md`.
- Single-source-of-truth defaults table: `references/defaults.md`.
