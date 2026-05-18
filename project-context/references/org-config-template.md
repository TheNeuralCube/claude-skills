<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# org-config.md template (project-context v0.4.0)

This file is a **template**. Copy it to `org-config.md` in your Project, populate the values your organization needs, and the skill will load it on every invocation. Resolution order: `user-config.md` > `org-config.md` (this file) > skill defaults in `references/defaults.md`.

The upstream skill does not ship a populated `org-config.md`. If `org-config.md` is absent, the skill uses upstream defaults; this is a perfectly fine deployment for individual users and small teams.

Every field below is **optional**. Comments explain what each does. Delete sections you do not use, or leave them empty — both are fine.

```yaml
---
config_type: project-context-org-config       # Required. Identifies this file to the skill.
config_version: "0.4.0"                       # Required. Match the skill version that consumes this config.
organization: <name>                          # Free-form name of the deploying organization.
---

# ---------------------------------------------------------------------------
# Default governance values
# ---------------------------------------------------------------------------
# Override the upstream defaults in references/defaults.md and
# references/governance.md. Each field below applies to every file the skill
# writes unless user-config.md or the operator overrides at invocation time.
defaults:
  sensitivity: internal                       # open | internal | confidential | restricted
  retention: standard                         # standard | extended | indefinite (archive defaults to indefinite)
  governance_frameworks: []                   # free-form list, e.g. [HIPAA, SOX, GDPR, internal-IP]
  custom_governance: {}                       # free-form key-value object for org-specific dimensions

# ---------------------------------------------------------------------------
# Merge policy (org floor)
# ---------------------------------------------------------------------------
# Sets the merge policy floor for the organization. user-config.md can choose
# a more permissive setting (e.g., user "auto" with org "hybrid") only if the
# allow_user_auto flag below is true.
#
# merge_policy: hybrid | gate | auto
# allow_user_auto: true | false   (default false; setting true lets users opt
#                                  into auto-mode in their own user-config.md)
merge_policy: hybrid
allow_user_auto: false

# ---------------------------------------------------------------------------
# Token budgets (org-level)
# ---------------------------------------------------------------------------
# Override the active-file budgets. See references/defaults.md.
# These are starting points; tune based on observed grounding fidelity in
# downstream sessions.
# active_file_token_target: 30000
# active_file_soft_warning: 50000
# active_file_hard_ceiling: 80000

# ---------------------------------------------------------------------------
# Scoring algorithm coefficients (org-level)
# ---------------------------------------------------------------------------
# Override the defaults in references/scoring.md.
# scoring:
#   alpha: 1.5
#   beta: 1.0
#   gamma: 5.0
#   delta: 2.0
#   epsilon: 0.5
#   lambda: 0.0347
#   demotion_threshold: 5

# ---------------------------------------------------------------------------
# Cross-skill chaining (optional)
# ---------------------------------------------------------------------------
# Lets the org append reminders or instructions to the operator brief at the
# end of each session. Triggers: after_default | after_merge_external |
# after_compact | after_rebuild | after_any.
# example downstream chaining; replace with values appropriate to your deployment
downstream_chaining:
  - trigger: after_any
    instruction: "Reminder: route the updated files through the team's review queue before re-uploading to the Project."
  - trigger: after_rebuild
    instruction: "Reminder: confirm the rebuilt active file matches your expectations before deleting the old version."

# ---------------------------------------------------------------------------
# Custom trigger phrase additions (optional)
# ---------------------------------------------------------------------------
# Org-specific phrases that route to a given operation. Upstream phrases stay
# active; entries here are additive.
# example additional trigger phrases; replace with phrases your team will use
additional_triggers:
  default:
    - "snapshot the project"
    - "context capture"
  compact:
    - "roll up project context"
  rebuild:
    - "reset project context"

# ---------------------------------------------------------------------------
# Custom governance vocabulary (optional)
# ---------------------------------------------------------------------------
# Constrain governance_frameworks to a fixed vocabulary. When set, the skill
# refuses to write a frontmatter governance_frameworks list containing a
# value not in the vocabulary.
governance_frameworks_vocabulary:
  enforce: false                              # true | false
  allowed: []                                 # used only when enforce is true

# ---------------------------------------------------------------------------
# Project identification defaults (optional)
# ---------------------------------------------------------------------------
# Useful for organizations that always work in a single named project context.
# When set, the skill uses these as the default project / project_id in
# frontmatter unless the operator explicitly overrides.
project_default: ""
project_id_default: ""
```

## How the skill loads this file

1. On invocation, after the surface guard and project detection, the skill scans the project for `org-config.md`.
2. If present, it parses the YAML frontmatter and body.
3. Any value here overrides the corresponding upstream default but is itself overridable by `user-config.md`.
4. Trigger phrases under `additional_triggers` are added to the trigger set; upstream phrases are not removed.
5. If `org-config.md` is malformed, the skill warns the operator and falls back to upstream defaults rather than failing.

## What does not belong in `org-config.md`

- Anything specific to a single user's session — use `user-config.md` instead.
- Anything that would change schema validity (cannot add or remove the body sections, cannot rename frontmatter fields, cannot change the ID prefix table; those are part of the `schema_version: "0.2"` contract).
- Secrets or credentials. The skill does not need them and `org-config.md` may be checked into shared infrastructure.

If you want to extend the schema beyond what `org-config.md` allows, that is a v0.5.0+ feature request rather than a config customization.
