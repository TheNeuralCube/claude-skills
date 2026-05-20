<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# user-config.md template (project-context skill)

This file is a **template**. Copy it to `user-config.md` in your project (alongside the three data files), uncomment any settings you want to override, and the skill will pick them up on the next invocation. Resolution order: `user-config.md` (this file) > `org-config.md` > skill defaults in `references/defaults.md`.

If `user-config.md` is absent, the skill falls back to org-config and then to upstream defaults. There is nothing wrong with running without a `user-config.md`; the defaults are designed for top-tier thinking models out of the box.

The file is a Linux-conf-style markdown document: a YAML body with every setting commented out, plus prose comments explaining what each does and the recommended values. Uncomment to activate.

This file is also the canonical example of the **`user-config.md` cross-skill convention** introduced in this skill version. Future skills in the `github.com/TheNeuralCube/claude-skills` monorepo follow the same pattern: per-user override layer, kebab-case YAML keys, every setting commented-out by default, every comment block explaining the trade-off. See repo-root `CONTRIBUTING.md` for the convention overview.

```yaml
# ============================================================
# project-context — user configuration
# ============================================================
# Default values are shown commented out, with rationale.
# Uncomment and edit any line to override.
# Reload by re-uploading this file to your Project.
# ============================================================


# -----------------------------------------------------------
# proposal_cap_per_session
# -----------------------------------------------------------
# How many gated merge proposals the skill shows you per session
# before grouping the rest as "deferred."
#
# Higher = more shows up per session, more decision fatigue.
# Lower  = fewer per session, more total sessions to clear backlog.
#
# Default: 10
# Recommended for power users: 15
# Recommended for "I'm in a hurry": 5
# -----------------------------------------------------------
# proposal_cap_per_session: 10


# -----------------------------------------------------------
# merge_policy
# -----------------------------------------------------------
# Controls which classifier outputs auto-apply vs require approval.
#
# Options:
#   hybrid -- (default) auto-apply ADD and NOOP; gate UPDATE,
#             DEMOTE, SUPERSEDE
#   gate   -- require approval on every change (max safety,
#             max friction)
#   auto   -- auto-approve everything (read the auto-mode
#             warning in operations/default.md before using
#             this; your name will be on every auto record)
# -----------------------------------------------------------
# merge_policy: hybrid


# -----------------------------------------------------------
# active_file_token_target / soft_warning / hard_ceiling
# -----------------------------------------------------------
# Token budgets for the active project-context.md file.
# These trigger consolidation behavior in the operator brief.
#
# Defaults: target 30000, warning 50000, ceiling 80000
# Optimized for: top-tier thinking models (Claude Opus 4.5+,
#                GPT-5 Pro thinking, Gemini Ultra thinking)
# Do not raise on lighter models. Lower if you observe
# grounding degradation in downstream sessions.
# -----------------------------------------------------------
# active_file_token_target: 30000
# active_file_soft_warning: 50000
# active_file_hard_ceiling: 80000


# -----------------------------------------------------------
# Scoring algorithm coefficients
# -----------------------------------------------------------
# These tune the demotion algorithm. Change with care.
# See references/scoring.md for the formula and reasoning.
#
# alpha   -- reinforcement weight (default 1.5)
# beta    -- importance weight (default 1.0)
# gamma   -- recency boost (default 5.0)
# delta   -- age penalty (default 2.0)
# epsilon -- wall-clock floor, per year past 3 (default 0.5)
# lambda  -- decay rate, = ln(2)/20 for 20-update half-life
#            (default 0.0347)
# demotion_threshold -- records below this propose DEMOTE
#                       (default 5)
# -----------------------------------------------------------
# scoring:
#   alpha: 1.5
#   beta: 1.0
#   gamma: 5.0
#   delta: 2.0
#   epsilon: 0.5
#   lambda: 0.0347
#   demotion_threshold: 5


# -----------------------------------------------------------
# Governance defaults (per-user)
# -----------------------------------------------------------
# Override the org or upstream defaults for files you create.
# See references/governance.md for the full field set.
#
# Defaults:
#   sensitivity: internal
#   retention: standard      (archive defaults to indefinite)
#   governance_frameworks: []
#   custom_governance: {}
# -----------------------------------------------------------
# governance:
#   sensitivity: internal
#   retention: standard
#   governance_frameworks: []
#   custom_governance: {}


# -----------------------------------------------------------
# user_identifier
# -----------------------------------------------------------
# How the skill identifies you in the audit trail. Currently
# null because the platform does not yet expose authenticated
# user identity to skills. v0.5.0 will pick this up
# automatically when the platform API supports it.
#
# Until then, you can set a free-form string here and the
# skill will stamp it onto `audit.approved_by` for every
# record you approve. If left null, audit.approved_by stays
# null.
# -----------------------------------------------------------
# user_identifier: null


# -----------------------------------------------------------
# Brief format
# -----------------------------------------------------------
# Controls the operator brief at the end of each session.
#
# brief.include_audit_summary -- show a one-line audit
#   summary per session (default: true). Useful if you use
#   auto-mode and want a daily reminder of which records
#   were auto-approved.
#
# brief.show_token_budget -- show current vs. budget for the
#   active file (default: true).
#
# brief.show_demotion_list -- list which records were
#   demoted, by ID (default: true).
# -----------------------------------------------------------
# brief:
#   include_audit_summary: true
#   show_token_budget: true
#   show_demotion_list: true
```

## How the skill loads this file

1. On invocation, after the surface guard and project detection, the skill scans the project for `user-config.md`.
2. If present, it parses the YAML body (everything inside the fenced block).
3. Any uncommented setting overrides the corresponding org-config or upstream default for the duration of the current invocation.
4. If the file is malformed, the skill warns the operator and falls back to org-config (then upstream defaults), rather than failing.

The skill never writes to `user-config.md`. It is operator-owned.

## What does not belong in `user-config.md`

- Anything specific to a single chat session — use chat-time instructions instead.
- Anything that would change schema validity. You cannot add or remove the file's sections, rename frontmatter fields, or change the ID prefix table; those are part of the `schema_version: "0.3"` contract.
- Secrets or credentials. The skill does not need them, and `user-config.md` may end up in shared infrastructure.

## What if I want to share my user-config?

`user-config.md` is per-user by intent. If multiple users on the same project should share the same settings, put those settings in `org-config.md` instead. `user-config.md` is the layer where one user diverges from their team — e.g., "I work in auto-mode because I trust my own quality judgment; the rest of the team uses hybrid."

## Cross-skill convention

This file's format — Linux-conf-style markdown with a fenced YAML body, kebab-case keys, every setting commented-out with rationale, single-source-of-truth defaults in `references/defaults.md`, resolution order user > org > skill — is the canonical example of the **`user-config.md` cross-skill convention** for the claude-skills monorepo. Future skills in the repo (next minor of session-recap, all new skills) adopt the same convention. The repo-root `CONTRIBUTING.md` points to this file as the example. The forthcoming nc3-meta-skill-forge skill (working name; see `ROADMAP.md`) will absorb the convention as its canonical home once that skill releases.
