---
file_role: skill-reference
topic: platform-specific-parameters
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Platform-specific parameters: schema and instantiation layout (session-handoff v0.1.0)

This file is the authoritative specification for the per-platform parameters the skill consults: limits, feature support, overflow strategy, and the config-instantiation layout (how the `config/` layer is realized on each surface). The **shipped parameter values** live in `config/platform-parameters.md`; this file owns the schema those values conform to and the rules for reading them.

Two parameter consumers in v0.1.0:

1. The update length contract reads a platform's effective context limit to make the per-version budget destination-aware (`references/defaults.md` section 4).
2. The config layer reads the instantiation layout to decide whether `config/` is a real directory or a `config-` name prefix on a flat surface (section 3).

## 1. Parameter schema

Each platform entry in `config/platform-parameters.md` conforms to:

```yaml
platforms:
  <platform-key>:
    context_window_tokens: <integer|tbd>      # effective context budget; tightens the per-version length target when smaller
    instructions_field_char_limit: <integer|~N|tbd>
    supports_attached_files: <boolean|tbd>
    supports_skills: <boolean>
    project_concept: <boolean|tbd>             # persistent container with attached files the operator returns to
    filesystem_config: <boolean|tbd>           # true = real config/ directory; false = flat knowledge list
    config_instantiation: "directory" | "flat-prefix" | tbd
    overflow_strategy: <enum string>
    model_identity_provenance: "high" | "operator-stated" | tbd
```

## 2. Field definitions

| Field | Semantics |
|---|---|
| `context_window_tokens` | Effective context budget on the surface. When smaller than `length_contract.per_version_soft_target`, the update length projection tightens to this value. `tbd` means not validated. |
| `instructions_field_char_limit` | Approximate character limit for the platform's project-level instructions field. `~N` means roughly N. |
| `supports_attached_files` | Whether the platform supports project-attached files the skill can read at invocation. |
| `supports_skills` | Whether the platform consumes the Anthropic skills format natively. |
| `project_concept` | Whether the platform has a persistent project container with attached files and instructions. |
| `filesystem_config` | Whether the surface exposes a real filesystem the `config/` directory can live in. |
| `config_instantiation` | `directory` (real `config/` folder) or `flat-prefix` (`config-` name prefix on a flat knowledge list). See section 3. |
| `overflow_strategy` | What to do when generated content exceeds a field limit. `none_required` when the limit is high enough that overflow does not happen in practice. |
| `model_identity_provenance` | `high` where the skill can read its execution environment (Claude Code, Cowork); `operator-stated` where model identity must be supplied. Feeds `generated_by.model_source` (`references/schema.md` section 4). |

## 3. Config-instantiation layout

The `config/` layer is a real navigable directory on filesystem surfaces (Claude Code, Cowork): `config_instantiation: directory`. On Claude.ai hosted Projects, where project knowledge is assumed to be presented as a flat file list (provisional; see below), `config/` degrades to a `config-` naming convention: `config_instantiation: flat-prefix`, so `config/user-config.md` becomes a flat file named `config-user-config.md`.

The intent (these files are yours to edit) is preserved on every surface. The skill never blind-writes; it auto-creates a config file only when confirmed absent (`references/configure.md` section 5).

**Claude.ai pin is provisional and unverified.** The `claude-ai` `config_instantiation: flat-prefix` value in `config/platform-parameters.md` is assumed per design spec section 8.4, not confirmed on a live Project; the two platform files agree on this provisional status. Live verification is a separate deferred task tracked in `ROADMAP.md`. Until verified for a given surface, the skill defaults to the `flat-prefix` convention on any non-filesystem or `tbd` surface (the safe degrade), naming files with the `config-` prefix and noting the assumption in pre-flight.

## 4. Surface awareness and model-identity provenance

session-handoff is the cross-surface tool and never declines a surface (this inverts the project-context surface guard, which is deliberately not adopted). It keeps awareness that Claude Code and Cowork yield higher model-identity provenance and notes it, but does not refuse on any surface. The `model_identity_provenance` parameter feeds the `generated_by.model_source` stamp and the higher-provenance note in pre-flight.

## 5. Validation rules

- Every platform entry in `config/platform-parameters.md` must include all schema fields (section 1).
- A `tbd` value is permitted but flags that parameter as not-yet-validated. The length contract treats a `tbd` `context_window_tokens` as "no destination tightening"; the config layer treats a `tbd` `config_instantiation` as the safe `flat-prefix` degrade.
- The schema is forward-compatible: unknown platform keys are ignored gracefully.

## 6. Cross-references

- Shipped platform values: `config/platform-parameters.md`.
- Length contract that consumes `context_window_tokens`: `references/defaults.md` section 4, `modes/update.md`.
- Config auto-creation and the instantiation layout: `references/configure.md` section 5.
- Model-identity provenance stamp: `references/schema.md` section 4.
- Surface awareness in pre-flight: `references/preflight.md`.
