---
schema_version: "0.5"
_managed_by: project-context-skill
config_type: platform
config_editable: true
configure_with: references/configure.md
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Platform-specific parameters (project-context v0.7.0, schema 0.5)

This is an operator-editable configuration file. It lives in `config/` and the skill reads it by base name (`platform-specific-parameters.md`), never by a hardcoded path. To change it, load it and ask the assistant to walk you through it; the assistant runs the shared interview in `references/configure.md` and uses the FIELD GUIDE below. See `configure_with` in the frontmatter.

It declares, per platform, the capability and limit parameters the skill consults at runtime: the model the operation-start advisory names, whether the active model can be changed from a skill, whether the file inventory is enumerable, where config is read, and how output is bundled. v0.6.0 read this file but did not action it; v0.7.0 actions the model advisory (`references/preflight.md` section 4.6) and references `config_read_location` and `file_inventory_enumerable` for operator reference. The project-creator skill (Workstream 3) remains the primary consumer of the instruction-rendering fields.

Each platform is a self-contained block: all of a platform's fields live together, so a future split into one file per platform is a straight extraction rather than a refactor.

## Schema

```yaml
platforms:
  claude-ai:
    # v0.7.0 fields
    strongest_thinking_model: "Claude Fable 5"
    can_change_active_model_from_skill: false
    file_inventory_enumerable: true
    config_read_location: "project-knowledge-flat-basename"   # pending one-upload verification; see Platform notes
    output_bundling: "none-required"
    # instruction-rendering fields (v0.6.0; consumed by project-creator)
    instructions_field_char_limit: ~100000
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    overflow_strategy: none_required

  codex:
    # v0.7.0 fields
    strongest_thinking_model: "GPT-5.5"
    can_change_active_model_from_skill: false   # configurable via client settings, /model, /status; the skill does not self-reconfigure
    file_inventory_enumerable: "unverified"
    config_read_location: "config-directory"
    output_bundling: "filesystem-direct"
    # instruction-rendering fields
    instructions_field_char_limit: "filesystem (AGENTS.md); no fixed field limit"
    supports_attached_files: true
    supports_skills: true
    project_concept: true
    overflow_strategy: none_required

  chatgpt-enterprise:
    # v0.7.0 fields
    strongest_thinking_model: "GPT-5.5 Pro"
    can_change_active_model_from_skill: false
    file_inventory_enumerable: "unverified"
    config_read_location: "project-knowledge-flat-basename"
    output_bundling: "zip-for-manual-download"
    # instruction-rendering fields
    instructions_field_char_limit: ~1500
    supports_attached_files: true
    supports_skills: false
    project_concept: true
    overflow_strategy: "produce condensed instructions block plus full instructions as attached source file"

  m365-copilot:
    # v0.7.0 fields (conservative defaults; m365-copilot not yet validated)
    strongest_thinking_model: null            # not validated; the advisory uses its generic-wording fallback (references/preflight.md section 4.6)
    can_change_active_model_from_skill: false
    file_inventory_enumerable: false          # conservative: routes counter assignment through the cannot-confirm prompt, never a silent 0001
    config_read_location: "project-knowledge-flat-basename"   # conservative flat default; base-name read
    output_bundling: "zip-for-manual-download"   # conservative flat-platform default (no preview-and-add flow)
    # instruction-rendering fields
    instructions_field_char_limit: tbd
    supports_attached_files: tbd
    supports_skills: false
    project_concept: tbd
    overflow_strategy: tbd
```

## FIELD GUIDE

This guide documents this file's own fields. It does not duplicate interview mechanics (those live in `references/configure.md`).

### v0.7.0 capability fields

| Field | Type | Semantics |
|---|---|---|
| `strongest_thinking_model` | string or `null` | The model name the operation-start advisory names for this platform (`references/preflight.md` section 4.6). `null` means "not determined": the advisory falls back to generic wording ("the strongest thinking-capable model available on your platform") and never names a wrong model. Fill from current platform reality. |
| `can_change_active_model_from_skill` | boolean | Whether a skill can inspect or change the active model on this platform. `false` on every current platform; this is why the destructive-tier gate confirms model setup with the operator (principle P3) rather than asserting it. |
| `file_inventory_enumerable` | boolean or `"unverified"` | Whether the skill can read the project file inventory at invocation. `true` on Claude.ai (the manifest is provided), so web never prompts for the counter. `false` routes counter assignment through the cannot-confirm prompt (`references/preflight.md` section 3.4) rather than a silent `0001`. `"unverified"` means runtime behavior is detect-and-react: the skill tries to read the manifest and prompts if it cannot confirm. This field is documentation for operator reference; it does not gate runtime behavior. |
| `config_read_location` | enum string | Where the skill reads config files. `"config-directory"` on filesystem platforms (reads `config/<name>.md` by base name). `"project-knowledge-flat-basename"` on flat platforms (reads `<name>.md` by base name from project knowledge). The skill always reads by base name; this field documents the location, it is not a path the skill concatenates. |
| `output_bundling` | enum string or `tbd` | How generated files reach the operator. `"none-required"` (Claude.ai preview-and-add flow), `"filesystem-direct"` (Codex writes to the working directory), `"zip-for-manual-download"` (ChatGPT bundles a `.zip`), or `tbd`. |

### Instruction-rendering fields (v0.6.0; consumed by project-creator)

| Field | Type | Semantics |
|---|---|---|
| `instructions_field_char_limit` | integer, string, or `tbd` | Approximate character limit for the platform's project-level instructions field. `~N` indicates "roughly N." `tbd` means unvalidated. |
| `supports_attached_files` | boolean or `tbd` | Whether the platform supports project-attached source files the skill can read at invocation time. |
| `supports_skills` | boolean | Whether the platform consumes the Anthropic skills format natively. |
| `project_concept` | boolean or `tbd` | Whether the platform has a persistent "project" container. |
| `overflow_strategy` | enum string | Strategy when generated instructions exceed `instructions_field_char_limit`. `none_required` means the limit is high enough that overflow does not happen in practice. |

## Platform notes

### claude-ai (Anthropic, Claude Projects)

The reference target. `strongest_thinking_model` is `Claude Fable 5` (the strongest generally available Claude model as of the build date; it supersedes Claude Opus 4.8, which is now the next-most-capable thinking model). The source-file manifest is provided to the skill at invocation, so `file_inventory_enumerable: true` and web never prompts for the counter (`references/preflight.md` section 3.4). `config_read_location` is `project-knowledge-flat-basename`: project knowledge is a flat file list, so the skill reads `user-config.md`, `org-config.md`, and `platform-specific-parameters.md` by base name. **Verification note:** the flat-project-knowledge assumption should be confirmed with a one-upload test before being relied on in production; until then it is the documented assumption.

### codex (OpenAI Codex)

`strongest_thinking_model` is `GPT-5.5` (the strongest model recommended for Codex at build time; `gpt-5.x-codex` variants are specialized). Model and effort are configurable via client settings, `/model`, and `/status`, but the skill does not self-reconfigure, so `can_change_active_model_from_skill: false` and the destructive gate confirms setup with the operator. Filesystem platform: config is a real `config/` directory and output is written directly to the working directory. `file_inventory_enumerable` is `unverified`; the skill is detect-and-react and prompts for the counter if it cannot confirm the inventory.

### chatgpt-enterprise (OpenAI ChatGPT Enterprise / Team Projects)

`strongest_thinking_model` is `GPT-5.5 Pro` (the highest-capability reasoning tier for Enterprise as of the build date). Instructions field is constrained (~1500 chars); skills do not load natively. Project knowledge is flat, so config is read by base name. Generated files are bundled into a `.zip` for manual download since there is no preview-and-add flow. Re-validate model names when project-creator ships.

### m365-copilot (Microsoft 365 Copilot)

Not yet validated. The v0.7.0 capability fields use conservative defaults rather than bare `tbd` where a bare `tbd` would be undefined behavior: `file_inventory_enumerable: false` routes counter assignment through the cannot-confirm prompt (never a silent `0001`), `config_read_location` defaults to base-name read, `output_bundling` defaults to `zip-for-manual-download` (m365 has no preview-and-add flow), and `strongest_thinking_model: null` triggers the advisory's generic-wording fallback. The instruction-rendering fields remain `tbd` pending a dedicated m365-copilot research pass; project-creator will not target m365-copilot until they are populated.

## Validation rules

- Every platform entry must include all five v0.7.0 capability fields and all five instruction-rendering fields.
- `strongest_thinking_model` may be `null` (advisory falls back to generic wording). A `tbd` on an instruction-rendering field flags the platform as not-yet-actionable for project-creator: that skill refuses to render for a platform with any `tbd` instruction-rendering field and emits "Platform `<name>` parameters not yet validated; cannot render." The model advisory in project-context does NOT refuse on `null`; it uses the fallback.
- `file_inventory_enumerable: false` or `"unverified"` must never produce a silent `0001`. Counter assignment follows `references/preflight.md` section 3.4.
- The platform key set (claude-ai, codex, chatgpt-enterprise, m365-copilot) is the current baseline. The schema is forward-compatible: skills tolerate unknown platform keys by ignoring them.

## How the skill loads this file

For project-context:

1. Pre-flight reads this file by base name if present (in `config/` on filesystem platforms; in flat project knowledge on web).
2. The operation-start advisory (`references/preflight.md` section 4.6) reads the active platform's `strongest_thinking_model` and names it, or uses generic wording if the value is missing or null.
3. Counter assignment (`references/preflight.md` section 3.4) is detect-and-react; `file_inventory_enumerable` is operator-reference documentation, not a runtime gate.
4. If the file is absent, the advisory uses generic wording and counter assignment proceeds by attempting to read the inventory.

For project-creator (Workstream 3, future): resolves the target platform from `user-config.md`'s `defaults.preferred_platform`, loads the matching entry, applies `overflow_strategy`, and refuses on a `tbd` instruction-rendering field.

## Cross-references

| Document | Relationship |
|---|---|
| `references/preflight.md` | Section 4.6 (advisory and gate) reads `strongest_thinking_model` and `can_change_active_model_from_skill`; section 3.4 (counter assignment) references `file_inventory_enumerable` |
| `references/configure.md` | Owns the interview mechanics that regenerate this file |
| `config/user-config.md.template` | `defaults.preferred_platform` selects which platform entry is loaded at runtime |
| `references/topology.md` | Topology is platform-agnostic; this file is platform-specific. Orthogonal. |
| project-creator skill (Workstream 3, future) | Primary consumer of the instruction-rendering fields |
