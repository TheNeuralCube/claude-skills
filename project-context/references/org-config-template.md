<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# org-config.md template (project-context skill)

This file is a **template**. Copy it to `org-config.md` (sibling to `SKILL.md`) in your deployment of the project-context skill, populate the values your organization needs, and the skill will load it on every invocation. The upstream skill does not ship a populated `org-config.md` — only this template.

If `org-config.md` is absent, the skill falls back to upstream defaults documented in `references/schema.md` and `references/governance.md`. There is nothing wrong with running the skill without an `org-config.md`; the upstream defaults are designed to be safe-permissive for individual users and small teams.

Below is the full schema. Every field is **optional**. Comments explain what each does. Delete sections you do not use, or leave them empty — both are fine.

```yaml
---
config_type: project-context-org-config       # Required. Identifies this file to the skill.
config_version: v0.3.1                        # Required. Match the skill version that consumes this config.
organization: <name>                          # Free-form name of the deploying organization.
---

# ---------------------------------------------------------------------------
# Default governance values
# ---------------------------------------------------------------------------
# These override the upstream defaults documented in references/governance.md.
# Each field is applied to every generated file's frontmatter unless the
# operator overrides it at invocation time.
defaults:
  sensitivity: internal                       # open | internal | confidential | restricted
  audience: ""                                # free-form string; empty if not used
  retention: standard                         # standard | extended | legal_hold | delete_after_<period>
  governance_frameworks: []                   # free-form list, e.g. [HIPAA, SOX, GDPR, internal-IP]

# ---------------------------------------------------------------------------
# Custom category taxonomy (optional)
# ---------------------------------------------------------------------------
# By default, the model assigns categories freely. To enforce a vocabulary,
# set constrain_to_vocabulary to true and list the allowed categories.
# When constrained, the model picks from the list only and never invents
# a new category.
categories:
  constrain_to_vocabulary: false              # true | false
  vocabulary: []                              # used only when constrain_to_vocabulary is true

# ---------------------------------------------------------------------------
# Custom tier defaults per section (optional)
# ---------------------------------------------------------------------------
# Override the section tier defaults from references/schema.md. Any section
# omitted here keeps its upstream default. Allowed values: full | summary |
# transient.
section_tier_defaults:
  Decisions: full
  Constraints: full
  Entities: full
  Terminology: full
  External_references: full
  Open_items: summary
  State_snapshot: summary

# ---------------------------------------------------------------------------
# Cross-skill chaining (optional)
# ---------------------------------------------------------------------------
# Lets the org append reminders or instructions after the skill produces an
# output. Each entry has a trigger and an instruction string. The skill
# prints the instruction as the final line of its response when the trigger
# fires. Triggers: after_generate | after_consolidate | after_either.
# example downstream chaining instructions; replace with values appropriate to your deployment
downstream_chaining:
  - trigger: after_generate
    instruction: "Reminder: route the generated file through the team's review queue before adding to the project."
  - trigger: after_consolidate
    instruction: "Reminder: review consolidation output before removing source files."

# ---------------------------------------------------------------------------
# Custom trigger phrase additions (optional)
# ---------------------------------------------------------------------------
# Adds organization-specific phrases that should route to a given mode.
# Upstream phrases (listed in SKILL.md) always remain active. Phrases listed
# here are additive.
# example additional trigger phrases; replace with phrases your team will use
additional_triggers:
  generate:
    - "snapshot the project"
    - "context capture"
  consolidate:
    - "roll up project context"

# ---------------------------------------------------------------------------
# Custom retention policies (optional)
# ---------------------------------------------------------------------------
# Translates the abstract retention values from governance.md into concrete
# durations the deploying organization uses. The skill does not enforce
# these; downstream retention systems consume them.
# example retention durations; replace with values appropriate to your organization's retention policy
retention_policies:
  standard: 365_days
  extended: 1825_days
  legal_hold: indefinite
  delete_after_30d: 30_days

# ---------------------------------------------------------------------------
# Project name override (optional)
# ---------------------------------------------------------------------------
# Useful for organizations that always work in a single named project
# context and want every generated file to carry the same project_name.
# When set, the skill uses this as the default project_name in frontmatter
# and skips the operator prompt unless the operator explicitly overrides.
project_name_default: ""

# ---------------------------------------------------------------------------
# Custom file naming overrides (optional)
# ---------------------------------------------------------------------------
filename_topic_required: false                # if true, the skill always prompts for a topic slug at generate time
filename_topic_default: ""                    # if filename_topic_required is false, this is used when the operator declines to provide one
```

## How the skill loads this file

1. On invocation, after pre-flight, the skill checks for `org-config.md` alongside `SKILL.md`.
2. If present, it parses the YAML frontmatter and the rest of the document above.
3. Any value here overrides the corresponding upstream default for the duration of the current invocation.
4. Trigger phrases listed under `additional_triggers` are added to the trigger set; upstream phrases are not removed.
5. If `org-config.md` is malformed, the skill warns the operator and falls back to upstream defaults rather than failing.

## What does not belong in `org-config.md`

- Anything specific to a single chat session (use the file frontmatter instead).
- Anything that would change schema validity (you cannot add or remove the seven body sections; you cannot rename frontmatter fields).
- Secrets or credentials. The skill does not need them and the file may be checked into shared infrastructure.

If you want to extend the schema beyond what `org-config.md` allows, that is a v0.2.0+ feature request rather than a config customization.
