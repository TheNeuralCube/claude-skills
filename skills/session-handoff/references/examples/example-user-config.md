# Example: a populated `config/user-config.md` (session-handoff v0.1.0)

The block below is a realistic example of a rendered, populated user-config. It is illustrative only and fictional. Rendered config files are operator work product and do NOT carry an SPDX header. The template is `config/user-config.md.template`; the field guide there documents every field.

This example shows the operator having populated the required fields (`operator.primary_name`, `defaults.preferred_platform`) and kept most defaults. `sanitization_prompt` is left at the public default `on-signal`.

```yaml
---
schema_version: "0.1"
_managed_by: session-handoff-skill
config_type: user
config_editable: true
configure_with: references/configure.md
---
# To configure: load this file and tell your AI "walk me through configuring this."
# It runs the shared interview (references/configure.md), uses the FIELD GUIDE below,
# and writes you a new version of this file for approval before saving.

operator:
  primary_name: "Dana Okafor"
  preferred_aliases: ["Dana", "D.O."]

defaults:
  preferred_platform: "claude-code"

conventions:
  date_format: "YYYY-MM-DD"
  filename_slug_style: "kebab-case"
  em_dashes_allowed: false
  preferred_table_density: "high"
  default_response_register: "strategic-peer"

privacy:
  default_sensitivity: "internal"
  sanitization_prompt: "on-signal"
  pii_flagging_enabled: true

contact:
  feedback_channel: "https://example.invalid/feedback"
```

## How the skill uses this file

- `operator.primary_name` populates `audit.approved_by` on handoffs this operator
  approves. It is self-asserted, not platform-verified.
- `defaults.preferred_platform` (`claude-code` here) drives the destination-aware
  length budget by selecting the platform entry in `config/platform-parameters.md`.
- `privacy.default_sensitivity` stamps `governance.sensitivity` on new handoffs
  unless org-config or a chat-time instruction overrides it.
- `privacy.sanitization_prompt: on-signal` fires the blocking sanitize question
  only when sharing or sensitive content is detected. The locked sanitization
  surfacing line still emits on every invocation regardless.
- `privacy.pii_flagging_enabled: true` keeps assistive PII flagging on (the
  secure-by-default exception).

To change any of these, load this file and say "walk me through configuring this."
The skill runs the shared interview, proposes a new version as a diff, and saves
only on your approval. A change to `default_sensitivity` or `sanitization_prompt`
is flagged as compliance-relevant in the approval summary.
