---
file_role: skill-reference
topic: defaults
schema_version_documented: "0.2"
skill_version: "0.4.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Defaults (project-context v0.4.0)

This file is the single source of truth for every default value the skill applies when no `user-config.md` or `org-config.md` overrides it. Resolution order: `user-config.md` > `org-config.md` > this file.

If a value appears here, it can be overridden in user-config or org-config. If a value does not appear here, it is not user-tunable in v0.4.0.

## 1. Merge policy

| Setting | Default | Allowed values |
|---|---|---|
| `merge_policy` | `hybrid` | `hybrid`, `gate`, `auto` |

Semantics:

- `hybrid` (default) — auto-apply ADD (no similar neighbor) and NOOP (duplicate/reinforcement). Gate UPDATE, DEMOTE, SUPERSEDE for operator approval.
- `gate` — require approval on every change. Max safety, max friction.
- `auto` — auto-approve every change. Triggers the auto-mode warning on session entry; all records stamp `audit.approval_mode: auto`.

See `operations/default.md` for the hybrid-brake table.

## 2. Proposal cap

| Setting | Default |
|---|---|
| `proposal_cap_per_session` | `10` |

How many gated merge proposals are shown to the operator per session before the rest are grouped as "deferred." Configurable via user-config or org-config.

`compact` operation may temporarily raise this cap to surface a larger batch of DEMOTE proposals, because the user explicitly asked for batch demotion.

## 3. Active-file token budgets

| Setting | Default |
|---|---|
| `active_file_token_target` | `30000` |
| `active_file_soft_warning` | `50000` |
| `active_file_hard_ceiling` | `80000` |

Optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking).

- Below `target`: routine operation; no consolidation pressure.
- Between `target` and `soft_warning`: no action, but `compact` is a good fit if invoked.
- Between `soft_warning` and `hard_ceiling`: default operation surfaces a consolidation reminder in the operator brief.
- Above `hard_ceiling`: default operation pushes harder on DEMOTE proposals; data integrity may degrade on lighter models.

These budgets apply to `project-context.md`. `entities.md` and `project-context-archive.md` have no enforced ceilings in v0.4.0.

## 4. Scoring coefficients

| Setting | Default | Source |
|---|---|---|
| `scoring.alpha` | `1.5` | reinforcement weight |
| `scoring.beta` | `1.0` | importance weight |
| `scoring.gamma` | `5.0` | recency boost |
| `scoring.delta` | `2.0` | age penalty |
| `scoring.epsilon` | `0.5` | wall-clock floor (per year past 3) |
| `scoring.lambda` | `0.0347` | decay rate (= ln(2)/20, 20-update half-life) |
| `scoring.demotion_threshold` | `5` | records below this are proposed for DEMOTE |

See `references/scoring.md` for the formula and rationale.

## 5. Governance defaults

| Setting | Default |
|---|---|
| `sensitivity` | `internal` |
| `retention` (active, entities) | `standard` |
| `retention` (archive) | `indefinite` |
| `governance_frameworks` | `[]` |
| `custom_governance` | `{}` |

## 6. Pre-flight defaults

| Setting | Default |
|---|---|
| `surface_guard.enabled` | `true` |
| `surface_guard.claude_code_action` | `decline_and_recommend_session_recap` |
| `migration.enabled` | `true` |
| `migration.preserve_legacy_files` | `true` (operator deletes manually; skill never deletes) |

The surface guard cannot be disabled in v0.4.0 (the skill is fundamentally inappropriate for Claude Code surfaces). Migration is opt-in only in the sense that the operator confirms the migration brief; detection is always on.

## 7. Output behavior defaults

| Setting | Default |
|---|---|
| `output.include_audit_trail_in_brief` | `true` (per-record audit metadata available on request) |
| `output.emit_operator_brief` | `true` |
| `output.brief_uses_emojis` | `true` (chat-only — stored files never carry emojis) |

## 8. Auto-mode defaults

| Setting | Default |
|---|---|
| `auto_mode.warning_on_session_entry` | `true` (cannot be disabled) |
| `auto_mode.passive_response_proceeds` | `true` (per design spec section 12.3) |
| `auto_mode.scope` | `per_session` (re-warn each session if still configured) |

## 9. ID prefixes

| Section | Prefix |
|---|---|
| Decisions | `dec-` |
| Constraints | `con-` |
| Current State | `csn-` |
| Open Items | `opn-` |
| Terminology | `trm-` |
| External References | `ref-` |
| Entities (all sub-sections) | `ent-` |
| Archived Records | `arc-` |

ID prefixes are not user-configurable in v0.4.0. They are part of the schema contract (`schema_version: "0.2"`).

## 10. Section order (`read_order`)

| File | `read_order` |
|---|---|
| `project-context.md` | `[decisions, constraints, current_state, open_items, terminology, external_references]` |
| `entities.md` | `[people, places, things, organizations, datasets]` |
| `project-context-archive.md` | `[records]` |

`read_order` is not user-configurable in v0.4.0. It is part of the schema contract.

## 11. What is NOT configurable in v0.4.0

These behaviors are intentionally fixed at the skill level. They are listed here so deployers do not waste time looking for override knobs.

- The surface guard's claude-code detection logic.
- The five-op classifier's decision rules.
- The hybrid brake's auto-apply / gate split (only the overall `merge_policy` is overridable).
- The auto-mode warning text (must match design spec section 12.3 verbatim).
- The migration algorithm.
- The file set (always three files; cannot reduce to one or two).
- The schema (must conform to `schema_version: "0.2"`).
- The `[AUTO]` content prefix for auto-approved records.

If a deployer needs to change one of these, the right answer is a skill fork or a future skill release — not an override.

## 12. Cross-references

- Format and commenting style for overriding these defaults: `references/user-config-template.md`.
- Org-scope overrides: `references/org-config-template.md`.
- Where each default is consumed: see each `operations/*.md` file.
