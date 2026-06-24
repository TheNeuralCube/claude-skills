---
schema_version: "0.4"
_managed_by: project-context-skill
config_type: platform
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Platform-specific parameters (project-context v0.6.0, schema 0.4)

This file is shipped INSIDE the `.skill` archive (not in operator project knowledge). It declares the per-platform capability and limit parameters the skill consults at runtime when rendering instructions, deciding overflow strategies, and selecting which platform-specific behaviors apply.

For v0.6.0, the project-context skill reads this file but does not action it. The schema is finalized here so the project-creator skill in Workstream 3 (week 2+) can build against it from the start. When project-creator ships, it will consume this file to render platform-appropriate skill instructions.

The file ships with three platform entries: `claude-ai` (full values), `chatgpt-enterprise` (basic values), `m365-copilot` (tbd values pending platform validation).

## Schema

```yaml
platforms:
  claude-ai:
    instructions_field_char_limit: ~100000
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    overflow_strategy: none_required

  chatgpt-enterprise:
    instructions_field_char_limit: ~1500
    supports_attached_files: true
    supports_skills: false
    project_concept: true
    overflow_strategy: "produce condensed instructions block plus full instructions as attached source file"

  m365-copilot:
    instructions_field_char_limit: tbd
    supports_attached_files: tbd
    supports_skills: false
    project_concept: tbd
    overflow_strategy: tbd
```

## Field definitions

| Field | Type | Semantics |
|---|---|---|
| `instructions_field_char_limit` | integer or `tbd` | Approximate character limit for the platform's project-level instructions field. `~100000` indicates "roughly N, exact limit may shift slightly across platform updates." `tbd` means the value has not been validated for this platform. |
| `supports_attached_files` | boolean or `tbd` | Whether the platform supports project-attached source files that the skill can read at invocation time. |
| `supports_skills` | boolean | Whether the platform supports the Anthropic skills format natively. Used to decide whether to emit a SKILL.md or a flattened equivalent. |
| `project_concept` | boolean or `tbd` | Whether the platform has a "project" concept (a persistent container the operator returns to across chats, with attached files and instructions). Skills in this repo target project-concept surfaces. |
| `overflow_strategy` | enum string | Strategy applied when generated instructions exceed `instructions_field_char_limit`. `none_required` means the limit is high enough that overflow does not happen in practice. The full string describes the overflow handling for restricted-limit platforms. |

## Platform notes

### claude-ai (Anthropic, Claude Projects)

The reference target for skill development in this repo. The instructions field is generous (~100K chars), attached source files are first-class, and the Anthropic skills format is supported natively. No overflow strategy is needed.

### chatgpt-enterprise (OpenAI ChatGPT Enterprise / Team Projects)

The platform supports project containers with instructions and attached files, but the instructions field is constrained to ~1500 chars in current ChatGPT Project UI. Skills do not load natively (the SKILL.md format is not consumed); the project-creator skill renders a condensed instructions block (fits the 1500 char field) plus the full instructions as an attached source file, and operators paste the condensed block into the field.

Values shown are best current estimate as of the v0.6.0 build. Re-validate when project-creator ships.

### m365-copilot (Microsoft 365 Copilot)

Platform parameters are not yet validated. v0.6.0 ships with `tbd` placeholders. The project-creator skill will not target m365-copilot until these values are populated. Re-validate during a dedicated m365-copilot research pass; build session marks this as out-of-scope for v0.6.0.

## Validation rules

- Every platform entry must include all five fields.
- A `tbd` value is permitted but flags the platform as not-yet-actionable. Skills that read this file should refuse to render for a platform with any `tbd` field and emit "Platform `<name>` parameters not yet validated; cannot render."
- The set of platform keys (claude-ai, chatgpt-enterprise, m365-copilot) is the v0.6.0 baseline. Additional platforms may be added in future releases; the schema is forward-compatible (skills tolerate unknown platform keys gracefully by ignoring them).

## How the skill loads this file

For v0.6.0 (project-context):

1. Pre-flight reads this file if present in the skill's runtime context.
2. No action taken; the file is loaded but not consulted by project-context operations.

For project-creator (Workstream 3, week 2+):

1. On invocation, the skill resolves the target platform from `user-config.md`'s `defaults.preferred_platform`.
2. The skill loads the matching platform entry from this file.
3. The skill applies the platform's `overflow_strategy` if the rendered instructions exceed `instructions_field_char_limit`.
4. The skill emits a `tbd` refusal (per validation rules above) if the matched platform entry has any `tbd` field.

## Cross-references

| Document | Relationship |
|---|---|
| `references/user-config.md.template` | `defaults.preferred_platform` selects which platform entry here is loaded at runtime |
| `references/topology.md` | Topology is platform-agnostic; this file is platform-specific. They are orthogonal. |
| project-creator skill (Workstream 3, future) | Primary consumer of this file once that skill ships |
