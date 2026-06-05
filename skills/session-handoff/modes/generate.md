---
file_role: skill-mode
mode: generate
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Mode: generate

## Pre-flight prerequisite

This mode runs only after pre-flight (`references/preflight.md`) has completed and, where the verdict requires it, the operator confirmation token has been received. generate runs on the `✓ Fresh` verdict, which auto-proceeds (no prior handoff to overwrite). Do not execute this mode without pre-flight completion.

generate produces one new handoff file from the current conversation: a high-fidelity, machine-readable forward transfer that any agent on any platform can resume cold. It is a mature core carried forward from the predecessor skill (v1.5) and adapted to the v0.1.0 two-tier schema.

Schema reference: `references/schema.md`. Lineage: `references/lineage.md`. Governance: `references/governance.md`. Defaults: `references/defaults.md`.

## 1. The first principle this mode serves

A handoff is a forward transfer of working state, optimized for a future AI agent as its primary reader. generate writes for a top-tier thinking model picking up the work cold, not for a human skimmer. Self-containment beats brevity: identity, lineage, and governance live inside the document.

## 2. Derive identity

1. Determine `topic` and `topic_slug` (kebab-case) from the conversation. Ask the operator only if the topic is genuinely ambiguous.
2. Set `handoff_date` to today and `state_captured_at` to now (ISO 8601 with timezone).
3. Derive `handoff_id` as `HND-<topic_slug>-<YYYYMMDD>-s<NN>` per `references/schema.md` section 3. Pre-flight has already run collision detection; use the `s<NN>` it resolved.
4. Set `handoff_version: 1`, `mode: generate`, `skill_version: "session-handoff-skill-v0-1-0"`, `schema_version: "0.1"`.
5. Set the clean-lineage fields: `supersedes: null`, `prior_handoffs: []`, `consolidation_depth: 0`, `derivative_of: null` (`references/lineage.md` section 7).

## 3. Populate the metadata contract

Fill every required field in `references/schema.md` section 1.

- `stage`, `status` (`active` / `paused` / `complete`), `thread_type` (`strategic` / `build` / `research` / `mixed`): infer from the conversation; confirm with the operator if unclear.
- `governance`: apply the resolution order (`references/governance.md` section 2). Public default `sensitivity: internal`, `governance_frameworks: []`. Org-config and user-config override.
- `generated_by`: stamp `model`, `provider`, `surface`, `generation_mode: live`, and `model_source`. On Claude Code and Cowork these are high-provenance and `model_source: system-reported`; on hosted chat surfaces `model_source: operator-stated` (`references/preflight.md` section 7).
- `audit`: `approved_by` from `config/user-config.md` identity or `null`; `approval_mode` accordingly (`self-asserted` if an identity is present, else `none`); `approved_at`; `redaction_manifest: null` (no sanitize ran).
- `review_by`, `agent_actionable`: set from the work's state.

No-empty-fields rule: if any required field has no confident value, set an explicit placeholder or `null` with a stated reason. An empty required field is a Parse Error (`references/schema.md` section 5); halt and emit the prescribed message.

## 4. Write the resumption payload (this file owns the field-by-field schema)

A handoff has two zones (`references/schema.md` section 2): Zone 1 is structured machine-parseable YAML, Zone 2 is dense narrative that expands on Zone 1. This mode file is the canonical owner of the tier-2 payload field-by-field schema. The principle, carried from the predecessor skill: anything an agent can programmatically extract or verify goes in Zone 1 YAML; anything that needs natural-language understanding goes in Zone 2.

### 4.1 Zone 1: the tier-2 payload blocks (structured YAML)

Emit these blocks in the handoff frontmatter, after the tier-1 metadata-contract keys, in the same YAML document. Lead with artifact state: the most common failure mode of a recap is describing the conversation well and the work product poorly. This skill inverts that. Use the null and empty conventions (`null` = not applicable, `[]` = applicable but empty, never empty strings).

```yaml
# --- Tier-2 resumption payload (mode-owned; evolves more freely than tier-1) ---
project:
  purpose: "1-2 sentence purpose"
  owner: "name and relevant context, or null"
  current_stage: "where the work stands in its lifecycle"
  success_criteria: "what done looks like"
  constraints: ["active constraints: budget, time, tools"]
  key_entities: ["names, orgs, systems the reader must know"]

artifacts:
  deliverables:                          # [] if none produced this session
    - filename: "exact filename incl. extension"
      type: spreadsheet | document | code | presentation | config | other
      version: "version label, or null"
      description: "what this file is and why it matters"
      current_state: "brief state description"
      state_markers:                     # verifiable facts an agent can check against the file
        - "marker (e.g. 441 formulas, zero errors)"
      modifications_this_session: ["what changed this session"]
      safe_edit_rules: ["e.g. do not overwrite tab X; the operator edits it manually"]
  references:                            # [] if none consumed
    - filename: "exact filename"
      type: csv | pdf | image | document | api_export | other
      description: "what this file contains and how it was used"
      ingestion_status: completed | partial | pending
      items_extracted: <int>
      items_excluded: ["items excluded and why"]
      judgment_calls: ["classification decisions made from this source"]

schemas: []                              # conditional: built/modified structured data
  # - name: "tab/table/section identifier"
  #   purpose: "what this structure does"
  #   headers: ["exact", "column", "names", "in", "order"]
  #   input_columns: [...]
  #   formula_columns: [...]
  #   key_formulas: [{ column, pattern, location }]
  #   special_rows: [{ row, purpose }]   # e.g. a sum row feeding a cross-tab reference
  #   named_ranges: [{ name, definition, used_by }]
  #   validation_rules: [{ column, allowed_values }]
  #   data_row_range: "rows 4-200"
  #   populated_rows: <int>

state_snapshot: null                     # conditional: deliverables exist
  # as_of: "<ISO 8601; matches state_captured_at>"
  # metrics: [{ label, value, location }]
  # row_counts: [{ sheet, populated, blank_critical_fields }]
  # formula_verification: { total_formulas, errors, recalculation_method, spot_checks }

decisions:                               # [] but note "none this session" in narrative if empty
  - decision: "what was decided"
    rationale: "why, full reasoning"
    reversibility: easy | moderate | difficult | irreversible
    affects: ["artifacts, sections, systems affected"]

known_issues:                            # [] but note "none identified" in narrative if empty
  - issue: "description"
    severity: critical | important | minor | informational
    location: "where in the deliverable or project"
    discovered: "how/when found"
    recommended_action: "what the next agent should do"

open_items:
  - item: "what is unresolved"
    context: "why it matters, evidence so far"
    current_state: "exact current state in the deliverable, or null"
    owner: user | agent | both
    priority: high | medium | low
    recommended_next: "suggested resolution path"

continuation:                            # the cold-start playbook
  first_step: "exact first thing the next agent should do"
  expected_inputs: ["files or data the operator will provide"]
  load_order: ["files to load and in what order"]
  diff_before_acting: true | false
  safe_edit_boundaries: ["e.g. preserve operator edits on tab X; tab Y safe to rebuild"]
  validation_checklist: ["checks to perform before saving"]
  output_naming: "convention for the next deliverable version, or null"
  toolchain:
    required: ["tools/libraries required"]
    preferred: ["preferred but not mandatory"]
    forbidden: ["tools that must not be used, and why"]

source_ingestion: []                     # conditional: thread_type research OR data sources processed
  # - source: "exact filename or source name"
  #   what_was_found: "summary"
  #   matched: ["data that matched existing records"]
  #   new: ["new data added"]
  #   excluded: ["excluded items and why"]
  #   judgment_calls: ["classification decisions"]
  #   ambiguities_remaining: ["unresolved ambiguities"]

changelog: null                          # conditional: supersedes a prior or modified deliverables
  # from_version: "..."  to_version: "..."
  # structural_changes: [...]  data_changes: [...]
  # formula_changes: [...]  manual_edits_preserved: [...]
  # resolved_since_prior: [...]          # update only: items resolved since the prior version,
  #                                      # compressed to one-line ledger entries that point to
  #                                      # the prior version for detail. See modes/update.md.

people_involved: []                      # optional: [{ name, role }]
tags: []                                 # optional: kebab-case
guardrails_summary: []                   # optional: forbidden ops lifted from continuation.toolchain.forbidden
```

Activation: `schemas`, `state_snapshot`, `source_ingestion`, and `changelog` are conditional per `references/section-activation.md`. Always-present blocks that are empty use `[]` (and the narrative notes "none this session"). The artifact-state blocks (`artifacts`, `state_snapshot`) carry the verifiable facts that let a resuming agent confirm it has the right files; do not prosify them away.

### 4.2 Zone 2: the narrative body

Write the activated narrative sections per `references/section-activation.md` (section set, conditional activation by `thread_type` and content, the fixed section order, and the writing rules). The narrative expands on Zone 1; it does not duplicate structured data. Reference deliverables by exact filename and reference Zone 1 blocks by name. Include the Receiving-agent handling block (sensitivity-aware, `references/governance.md` section 3.2) and the Staleness Warning. Rewrite content to be self-contained: no pronouns that depend on the originating conversation. Third-person observer voice, no em dashes, no emphasis formatting, no tables in narrative.

## 5. Write the file and validate

1. Filename: `<handoff_id>-v1.md` (the version suffix mirrors `handoff_version`).
2. Run the tier-1 validation checklist (`references/schema.md` section 6). If any check fails, halt and report; do not present the file.
3. Run the payload completeness check: every always-present tier-2 block is present (empty as `[]`/`null` where it applies), every activated conditional block (`references/section-activation.md`) is populated, and every Zone 2 narrative section that should appear given `thread_type` and content is present in the fixed order. The artifact-state blocks (`artifacts`, `state_snapshot`) must carry verifiable `state_markers`/`metrics` rather than prose, since they are the resuming agent's file-identity check.
4. No SPDX header on the generated handoff. The handoff is the operator's work product, not skill source.

## 6. Post-flight

Emit the post-flight summary (`references/preflight.md` section 9): the `handoff_id`, `handoff_version 1`, the filename and schema, `generation_mode: live`, and the standard surface and sanitization notes. Confirm the file is ready to download or move to its destination.

## 7. Failure handling

| Failure | Handling |
|---|---|
| Topic genuinely ambiguous | Ask the operator once; do not guess a slug that will collide. |
| A required field has no confident value | Set an explicit placeholder or `null` with reason; if neither is possible, Parse Error and halt. |
| Validation fails on the written file | Halt; report the failing check; do not present the file. |
| Operator cancels | Stop. Do not write. |

## 8. Cross-references

- Two-zone model and the tier-2 block summary: `references/schema.md` section 2.
- Zone 2 section set, conditional activation, ordering, writing rules: `references/section-activation.md`.
- Schema and the no-empty-fields rule (tier-1): `references/schema.md`.
- Clean-lineage constraints for generate: `references/lineage.md` section 7.
- Governance resolution and the receiving-agent block: `references/governance.md`.
- Pre-flight, surface awareness, post-flight: `references/preflight.md`.
- The update path that supersedes a generate handoff: `modes/update.md`.
- A worked example: `references/examples/example-handoff.md`.
