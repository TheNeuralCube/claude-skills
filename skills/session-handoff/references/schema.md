---
file_role: skill-reference
topic: schema
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Schema (session-handoff v0.1.0, schema_version "0.1")

This file is the authoritative restatement of the metadata contract on every handoff the session-handoff skill writes. Modes reference this file. The schema version (`schema_version` in every file's frontmatter) is decoupled from the skill version (`skill_version`): the schema version bumps only when the shape of the contract changes, the skill version bumps on every release. The coincidence of both starting near 0.1 is not coupling. See `references/schema-changelog.md`.

The frontmatter is two-tiered:

1. A tight, versioned **metadata contract** owned by this file (section 1). It is what retrofit upgrades and what pre-flight drift-detection inspects.
2. A **resumption payload** whose field-by-field shape is mode-coupled and defined in the mode files (`modes/generate.md`, `modes/update.md`, `modes/consolidate.md`). Section 2 here describes its blocks; it does not own their schema.

Keeping the contract compact is deliberate: it keeps retrofit and drift detection clean while the payload, the part that makes a handoff useful to a resuming agent, evolves more freely.

## 1. The metadata contract

Every handoff begins with this frontmatter. All fields listed here are REQUIRED unless the inline note says otherwise. "Required" means present with a confident value, an explicit placeholder, or `null` with a stated reason. An empty required field is a Parse Error (section 5).

```yaml
---
# --- Identity and schema (required) ---
schema_version: "0.1"
_managed_by: session-handoff-skill
handoff_id: HND-<topic_slug>-<YYYYMMDD>-s<NN>     # self-derivable; no external mnemonic table
handoff_version: 1                                # increments on update; mirrors filename suffix
skill_version: "session-handoff-skill-v0-1-0"
mode: "generate" | "update" | "consolidate" | "retrofit" | "share-sanitize"
handoff_date: <YYYY-MM-DD>
state_captured_at: <ISO 8601>

# --- Topic and status (required) ---
topic: <string>
topic_slug: <kebab-case>
stage: <integer>
status: "active" | "paused" | "complete"
thread_type: "strategic" | "build" | "research" | "mixed"

# --- Lineage (required; semantics in references/lineage.md) ---
supersedes: "<handoff_id>#v<N>" | null            # update only; null otherwise
prior_handoffs: []                                # consolidate ledger; preserved verbatim on a sanitized derivative of a consolidation (lineage.md)
consolidation_depth: 0                            # increments on consolidate; preserved verbatim on a sanitized derivative; audit only
derivative_of: "<handoff_id>#v<N>" | null         # share-sanitize output only

# --- Governance (required; semantics in references/governance.md) ---
governance:
  sensitivity: "open" | "internal" | "confidential" | "restricted"
  retention: <string|null>                        # e.g. "review_by 2026-08-31"; null permitted
  governance_frameworks: []                        # ["SOX","ITAR",...]; empty in public default
  custom_governance: <string|null>

# --- Provenance: how it was made (system-inferred, reliable) ---
generated_by:
  model: <string>
  provider: <string>
  surface: <string>
  generation_mode: "live" | "retrofit" | "consolidated" | "sanitized"
  model_source: <string>

# --- Audit: who vouched for it (self-asserted, NOT platform-verified) ---
audit:
  approved_by: <string|null>                       # from user-config identity
  approval_mode: "self-asserted" | "unverified" | "none"
  approved_at: <ISO 8601|null>
  redaction_manifest: <path|null>                  # set only when share-sanitize ran

# --- Continuation pointers (required) ---
review_by: <YYYY-MM-DD|null>
agent_actionable: "yes" | "no"
---
```

### 1.1 Field-by-field reference

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | The contract version. v0.1.0 writes `"0.1"`. Bumps only when the contract changes; see `references/schema-changelog.md`. |
| `_managed_by` | yes | String literal `session-handoff-skill`. Registry marker; makes pre-flight detection reliable. The leading underscore signals internal metadata, not user-facing data. Appears on every file the skill writes, including config and manifest files. |
| `handoff_id` | yes | `HND-<topic_slug>-<YYYYMMDD>-s<NN>`. Self-derivable; see section 3. Stable across `update` versions of the same handoff. |
| `handoff_version` | yes | Starts at 1, increments on `update`. Disambiguates versions sharing one `handoff_id`. Mirrors the filename version suffix. |
| `skill_version` | yes | The skill that wrote the file, e.g. `"session-handoff-skill-v0-1-0"`. Distinct from `schema_version`. |
| `mode` | yes | The mode that produced this file. One of the five. |
| `handoff_date` | yes | `YYYY-MM-DD`, the calendar date of the write. Feeds `handoff_id`. |
| `state_captured_at` | yes | ISO 8601 with timezone; when the working state was captured. |
| `topic` | yes | Human-readable topic string. |
| `topic_slug` | yes | kebab-case slug; feeds `handoff_id` and the filename. |
| `stage` | yes | Integer; the operator's stage marker for the work. |
| `status` | yes | One of `active`, `paused`, `complete`. |
| `thread_type` | yes | One of `strategic`, `build`, `research`, `mixed`. |
| `supersedes` | yes | `<handoff_id>#v<N>` on `update`; `null` otherwise. See `references/lineage.md`. |
| `prior_handoffs` | yes | The consolidation ledger; populated for `mode: consolidate`, OR preserved verbatim from the source when a `share-sanitize` derivative is taken of a consolidation; `[]` otherwise. Entry shape calibrated by config. See `references/lineage.md`. |
| `consolidation_depth` | yes | Integer; 0 for non-consolidated handoffs, one greater than the maximum source depth on `consolidate`. On a `share-sanitize` derivative it is preserved verbatim from the source. Audit only; does not feed the consolidate cap. |
| `derivative_of` | yes | `<handoff_id>#v<N>` on `share-sanitize` output; `null` otherwise. A sanitized copy is a leaf derivative, not part of the supersession chain. It preserves the source's lineage (`prior_handoffs`, `consolidation_depth`) verbatim and additionally sets this field. |
| `governance.sensitivity` | yes | One of `open`, `internal`, `confidential`, `restricted`. Public default `internal`. See `references/governance.md`. |
| `governance.retention` | yes | Free-form string or `null`. |
| `governance.governance_frameworks` | yes | List, may be `[]`. Empty in the public default. |
| `governance.custom_governance` | yes | Free-form string or `null`. |
| `generated_by.model` | yes | Model identifier, e.g. `claude-opus-4-8`. |
| `generated_by.provider` | yes | Provider, e.g. `anthropic`. |
| `generated_by.surface` | yes | Surface, e.g. `claude-code`, `claude-ai`, `cowork`. See section 4. |
| `generated_by.generation_mode` | yes | One of `live`, `retrofit`, `consolidated`, `sanitized`. Records how the file was produced. |
| `generated_by.model_source` | yes | How the model identity was determined, e.g. `system-reported` or `operator-stated`. |
| `audit.approved_by` | yes | Self-asserted identity from user-config, or `null`. See section 4.1. |
| `audit.approval_mode` | yes | One of `self-asserted`, `unverified`, `none`. |
| `audit.approved_at` | yes | ISO 8601 or `null`. |
| `audit.redaction_manifest` | yes | Path to the manifest, set only when `share-sanitize` ran; `null` otherwise. |
| `review_by` | yes | `YYYY-MM-DD` or `null`. A staleness checkpoint for the resuming agent. |
| `agent_actionable` | yes | `yes` or `no`. Whether a resuming agent can act on this handoff without further operator input. |

Frontmatter resolution order when the skill writes governance and provenance defaults: `config/user-config.md` > `config/org-config.md` > skill defaults from `references/defaults.md` > field-level inferences from session state. See `references/governance.md`.

## 2. The resumption payload (second tier)

The payload carries the actual resumption content, and it is what made the predecessor skill (v1.5) useful: a machine-parseable record of artifact state, structures, decisions, and the cold-start playbook. The payload is **inherited in shape from v1.5 and remains machine-parseable**. It is owned by the mode files (`modes/generate.md` owns the canonical field-by-field schema; `update`, `consolidate`, and `share-sanitize` reuse it and differ only in what they emphasize).

A handoff has two zones, the same separation v1.5 used:

| Zone | Where | Content |
|---|---|---|
| Zone 1: structured state | YAML frontmatter | the tier-1 metadata contract (section 1) plus the tier-2 payload blocks (below). Everything an agent can programmatically extract or verify. |
| Zone 2: context narrative | markdown body | dense prose that expands on Zone 1: connective context that does not fit cleanly into key-value pairs. Section set and activation rules in `references/section-activation.md`. |

Design principle, carried from v1.5: anything an agent could programmatically extract or verify belongs in Zone 1 YAML. Anything that needs natural-language understanding belongs in Zone 2. When in doubt, put it in YAML. The primary reader is a top-tier thinking model, not a human skimmer.

### 2.1 Tier-2 payload blocks (Zone 1 YAML, after the metadata contract)

These blocks follow the metadata-contract keys in the same frontmatter document. They are mode-owned and evolve more freely than tier-1: retrofit and drift detection inspect only the tier-1 contract (section 1), so the payload can grow without forcing a schema bump. `modes/generate.md` is authoritative for the field-by-field shape; the summary here is the standing set.

| Block | Purpose | Activation |
|---|---|---|
| `project` | purpose, owner, current_stage, success_criteria, constraints, key_entities. Zero-context grounding. | always |
| `artifacts.deliverables` | per deliverable: filename, type, version, `description` (what the file is and why it matters), current_state, `state_markers` (verifiable facts an agent can check), `modifications_this_session`, `safe_edit_rules`. | always (empty list if none) |
| `artifacts.references` | per consumed input: filename, type, `description` (what the file contains and how it was used), ingestion_status, items_extracted, items_excluded, judgment_calls. | always (empty list if none) |
| `schemas` | exact structure of built or modified data: headers, input vs formula columns, key_formulas, `special_rows` (row plus purpose, e.g. a sum row feeding a cross-tab reference), named_ranges, validation_rules, data_row_range, populated_rows. | conditional: structured data built or discussed |
| `state_snapshot` | as_of, metrics (label/value/location), row_counts, formula_verification. Exact values an agent checks to confirm it has the right file. | conditional: deliverables exist |
| `decisions` | per decision: decision, rationale, reversibility, affects. | always (note "none this session" if empty) |
| `known_issues` | per issue: issue, severity, location, discovered, recommended_action. | always (note "none identified" if empty) |
| `open_items` | per item: item, context, current_state, owner, priority, recommended_next. | always |
| `continuation` | the cold-start playbook: first_step, expected_inputs, load_order, diff_before_acting, safe_edit_boundaries, validation_checklist, output_naming, toolchain (required/preferred/forbidden). | always |
| `source_ingestion` | per data source: source, what_was_found, matched, new, excluded, judgment_calls, ambiguities_remaining. The audit trail behind `artifacts.references`. | conditional: `thread_type: research` or any data source processed this session (see `references/section-activation.md`) |
| `changelog` | from_version, to_version, structural_changes, data_changes, formula_changes, manual_edits_preserved, `resolved_since_prior` (update only: items resolved since the prior version, compressed to ledger lines pointing to the prior version). | conditional: this handoff supersedes a prior or modified existing deliverables |
| `people_involved` | name plus role, for people the reader needs to know. | optional |
| `tags` | kebab-case tag list. | optional |
| `guardrails_summary` | top-level array of forbidden operations, lifted from `continuation.toolchain.forbidden`, surfaced so an agent sees the key don'ts without descending into `continuation`. | optional |

Null and empty conventions: `null` means the field does not apply to this session type; `[]` means it applies but no items exist; never use empty strings. Omit a conditional block only when `references/section-activation.md` says to.

### 2.2 Zone 2 narrative (markdown body)

The body is dense narrative prose that expands on Zone 1, addressed to the reading agent. The section set, the conditional activation rules, the section order, and the writing rules (third-person observer voice, no emphasis formatting, no tables in narrative, reference deliverables by exact filename, reference Zone 1 blocks by name, no em dashes) are specified canonically in `references/section-activation.md`. The standing body sections are: Project Background, Session Summary, Current State, Technical Context (conditional), Source Ingestion Context (conditional), Strategic Context (conditional), Decisions and Rationale, Open Items in Context, Guardrails and Watchpoints (conditional), Workflow and Process Notes (conditional), the Receiving-agent handling block (sensitivity-aware, `references/governance.md`), Continuation Briefing, and the Staleness Warning.

## 3. handoff_id derivation

`handoff_id` is `HND-<topic_slug>-<YYYYMMDD>-s<NN>`, derived deterministically:

1. `topic_slug` is the kebab-case slug already on the handoff.
2. `<YYYYMMDD>` is `handoff_date` with separators removed.
3. `s<NN>` is the session sequence: `01` for the first handoff on that topic and date, incrementing for subsequent same-topic same-date handoffs detected in project knowledge.

The `HND` prefix is fixed (it replaces the predecessor's id prefix). There is no external lookup table. `supersedes`, `prior_handoffs`, and `derivative_of` entries use the `<handoff_id>#v<N>` form, where `<N>` is the `handoff_version`.

Collision handling: when a same-topic same-date handoff already exists in project knowledge, the `s<NN>` sequence increments on detection. Pre-flight runs this detection before any write.

## 4. Provenance and audit blocks

`generated_by` and `audit` are separate blocks by design. `generated_by` is **how it was made** (system-inferred, reliable). `audit` is **who vouched for it** (self-asserted, not platform-verified). Conflating them would let a self-asserted approval borrow the credibility of a system-inferred fact.

Surface note: on Claude Code and Cowork the surface and model identity are higher-provenance (the skill can read its execution environment). On hosted chat surfaces the model identity may be operator-stated; `model_source` records which. The skill never declines a surface over this; it records and proceeds. See `references/preflight.md` surface awareness.

### 4.1 The two honesty guardrails

These are stated here and in the README, verbatim where prescribed.

- **PII flagging is assistive, not a guarantee.** The skill flags possible PII for review and never claims to have found or removed all PII. See `references/redaction.md`.
- **`approved_by` is self-asserted, not verified.** Verbatim disclosure:

  > approved_by is self-asserted from user-config identity. It is not platform-verified and must not be treated as authenticated identity until a platform identity API exists.

  Until a platform identity API exists, `approved_by` populates from `config/user-config.md` identity or is `null`, and `approval_mode` records the posture (`self-asserted`, `unverified`, or `none`).

## 5. The no-empty-fields principle

Enforced at write. An empty required field with no placeholder is a Parse Error. Emit, verbatim:

```
Field <X> is empty; expected a confident value, an explicit placeholder, or null with reason.
```

No write proceeds while a required field is empty. The resumption payload (second tier) is owned by the mode files and is not part of this metadata-contract validation gate; mode files run their own payload completeness checks.

## 6. Validation checklist

A handoff conforms to schema "0.1" when:

1. Frontmatter is valid YAML and includes every REQUIRED field in section 1.
2. `schema_version` is exactly `"0.1"`.
3. `_managed_by` is present and equals exactly `session-handoff-skill`.
4. `handoff_id` matches `HND-<topic_slug>-<YYYYMMDD>-s<NN>` and is consistent with `topic_slug` and `handoff_date`.
5. `handoff_version` is a positive integer and matches the filename version suffix.
6. `mode` is one of the five and is consistent with the lineage fields (e.g., `supersedes` non-null implies `mode: update` or a composed retrofit-then-update).
7. The governance block is present with a valid `sensitivity` enum value.
8. `generated_by` and `audit` blocks are present and complete.
9. No required field is empty (section 5).
10. Lineage fields are internally consistent per `references/lineage.md` (e.g., `derivative_of` non-null implies `mode: share-sanitize` and `generation_mode: sanitized`).

Modes reference this checklist in their final validation pass.

## 7. Cross-references

- Tier-2 payload field-by-field schema: `modes/generate.md` (canonical); `references/section-activation.md` (Zone-2 sections, activation, ordering, writing rules).
- Schema-version-versus-skill-version decoupling, Supported Schemas, 0.1 inception: `references/schema-changelog.md`.
- Lineage field semantics (supersession, consolidation, derivative identity, governance propagation): `references/lineage.md`.
- Governance taxonomy, resolution order, receiving-agent handling block: `references/governance.md`.
- Built-in redactor, manifest, the `redaction_provider` seam: `references/redaction.md`.
- Pre-flight algorithm, verdicts, token catalog, routing table, post-flight, sanitization surfacing: `references/preflight.md`.
- Universal public defaults: `references/defaults.md`.
- Worked examples: `references/examples/`.
