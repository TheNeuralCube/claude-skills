---
schema_version: "0.1"
_managed_by: session-handoff-skill
config_type: platform
config_editable: true
configure_with: references/configure.md
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# To configure: most operators never edit this file. It ships with the skill as
# reference data the skill reads at pre-flight. An organization on a constrained
# surface may tune overflow_strategy via the shared interview (references/configure.md),
# which writes a new version for approval before saving.
#
# This is the SHIPPED platform parameters file. The parameter SCHEMA and the rules
# for reading these values live in references/platform-specific-parameters.md.

# Platform parameters (session-handoff v0.1.0, schema 0.1)

This file declares the per-platform values the skill consults at runtime: the effective context budget (which makes the update length budget destination-aware), feature support, the overflow strategy, the config-instantiation layout, and the model-identity provenance of each surface. It is shipped inside the `.skill` archive. The schema these values conform to, and the rules for reading them, are owned by `references/platform-specific-parameters.md`.

## Shipped values

```yaml
platforms:
  claude-code:
    context_window_tokens: ~200000
    instructions_field_char_limit: none_required
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    filesystem_config: true
    config_instantiation: "directory"
    overflow_strategy: none_required
    model_identity_provenance: "high"

  cowork:
    context_window_tokens: ~200000
    instructions_field_char_limit: none_required
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    filesystem_config: true
    config_instantiation: "directory"
    overflow_strategy: none_required
    model_identity_provenance: "high"

  claude-ai:
    context_window_tokens: ~200000
    instructions_field_char_limit: ~100000
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    filesystem_config: false
    config_instantiation: "flat-prefix"     # PROVISIONAL / UNVERIFIED: assumed per design spec section 8.4 (hosted Projects present knowledge as a flat list), NOT confirmed on a live Project. Live verification is a separate deferred task. Treated as the safe degrade until verified.
    overflow_strategy: none_required
    model_identity_provenance: "operator-stated"

  chatgpt-enterprise:
    context_window_tokens: tbd
    instructions_field_char_limit: ~1500
    supports_attached_files: true
    supports_skills: false
    project_concept: true
    filesystem_config: false
    config_instantiation: "flat-prefix"
    overflow_strategy: "produce condensed block plus full handoff as an attached file"
    model_identity_provenance: "operator-stated"

  m365-copilot:
    context_window_tokens: tbd
    instructions_field_char_limit: tbd
    supports_attached_files: tbd
    supports_skills: false
    project_concept: tbd
    filesystem_config: tbd
    config_instantiation: tbd
    overflow_strategy: tbd
    model_identity_provenance: tbd
```

## FIELD GUIDE (local to this file)

| Field | Semantics |
|---|---|
| `context_window_tokens` | Effective context budget. When smaller than `length_contract.per_version_soft_target` (12000), the update length projection tightens to this value. `tbd` means no destination tightening. |
| `instructions_field_char_limit` | Approximate char limit for the platform's instructions field. `none_required` where it is not a constraint. |
| `supports_attached_files` | Whether project-attached files are readable at invocation. |
| `supports_skills` | Whether the Anthropic skills format loads natively. |
| `project_concept` | Whether the platform has a persistent project container. |
| `filesystem_config` | Whether a real filesystem hosts the `config/` directory. |
| `config_instantiation` | `directory` (real `config/` folder) or `flat-prefix` (`config-` name prefix on a flat knowledge list). The safe degrade on any non-filesystem or `tbd` surface is `flat-prefix`. |
| `overflow_strategy` | What to do when generated content exceeds a field limit. |
| `model_identity_provenance` | `high` where the skill reads its execution environment (Claude Code, Cowork); `operator-stated` on hosted chat surfaces. Feeds `generated_by.model_source`. |

## Notes

- **claude-code, cowork:** filesystem surfaces. `config/` is a real directory; model identity is high-provenance (`model_source: system-reported`).
- **claude-ai:** the `config_instantiation: flat-prefix` value is **provisional and unverified**. It is assumed per design spec section 8.4 (hosted Projects present knowledge as a flat list, so `config/` degrades to the `config-` prefix), not confirmed against a live Project. Live verification is a separate deferred task tracked in `ROADMAP.md`; do not treat this pin as verified. The assumption is the safe degrade, so behavior is correct even if the surface differs.
- **chatgpt-enterprise:** project containers with a constrained instructions field; best current estimate, re-validate.
- **m365-copilot:** not yet validated; all `tbd`. The skill treats `tbd` `config_instantiation` as the `flat-prefix` safe degrade and `tbd` `context_window_tokens` as no destination tightening.

The set of platform keys is the v0.1.0 baseline. The schema is forward-compatible: unknown platform keys are ignored gracefully. See `references/platform-specific-parameters.md`.
