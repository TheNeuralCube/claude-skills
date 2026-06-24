---
file_role: skill-reference
topic: schema
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Schema (project-context v0.7.0, schema_version "0.5")

This file is the authoritative restatement of the data schema for every file the project-context skill writes. Operations reference this file. The build session's drift-detection guard compares this file against the prior tag (`project-context-v0.6.0` for the v0.7.0 build) and refuses to commit if the schema differs from the prior release without a corresponding bump and `schema-changelog.md` entry.

Schema "0.5" extends schema "0.4" with one new REQUIRED frontmatter field (`generation`) on the three context files and a versioned, prefix-unified naming contract for those files (`pc-NNNN-{context,entities,archive}.md`). The legacy `update_count` field is RETAINED: it remains the scoring lifecycle counter (see `references/scoring.md`). `generation` is a separate, identity-only counter that matches the filename's `NNNN` and is distinct from `update_count`. The topology block carries forward from "0.4" verbatim. All other schema "0.4" mechanics carry forward unchanged.

**Two counters, two jobs.** `generation` (new in 0.5) is the shared-set identity counter: all three files of a generation share the same `NNNN`, it matches the filename, and it never feeds scoring. `update_count` (retained from 0.2) is the per-file scoring lifecycle counter that drives update-based decay. They move independently, not in lockstep: `generation` advances on every operation (the whole set is re-stamped to the new `NNNN`, including a file whose content did not change), while `update_count` increments only on files whose content changed. On Scenario G, `generation` resets to 1 while `update_count` is preserved verbatim. Do not conflate them.

This retention of `update_count` intentionally diverges from design spec lines 103, 280, and 306 (which call to retire it) per Hub ruling F1: one counter cannot serve both identity and scoring once Scenario G resets the identity counter. Do not re-apply the removal instruction.

### Naming contract (schema 0.5)

| `file_role` | Filename (schema 0.5) | Prior name (schema 0.4 and earlier) |
|---|---|---|
| `project-context` | `pc-NNNN-context.md` | `project-context.md` |
| `entities` | `pc-NNNN-entities.md` | `entities.md` |
| `archive` | `pc-NNNN-archive.md` | `project-context-archive.md` |

`NNNN` is a zero-padded four-digit shared-set counter equal to the file's `generation`. The first generation is `pc-0001-*`. The skill recognizes its managed context set by the `pc-NNNN-*` name pattern AND the `_managed_by` marker together (the recognition contract; see section 6 and `references/preflight.md`). Counter assignment at pre-flight and the confirmed-empty rule are specified in `references/preflight.md`. Old canonical names (`project-context.md`, `entities.md`, `project-context-archive.md`) are retained only as the detection signal and source filenames for migration Scenarios D, E, F, and G in `references/migration.md`.

## 1. The three files

| Filename | `file_role` | Purpose | Token budget |
|---|---|---|---|
| `pc-NNNN-context.md` | `project-context` | Active grounding file: decisions, constraints, current state, open items, terminology, external references. | Target 30K, soft warning 50K, hard ceiling 80K. |
| `pc-NNNN-entities.md` | `entities` | Stable reference data: people, places, things, organizations, datasets. Looked up by name; no automatic decay. | No fixed ceiling; loaded selectively. |
| `pc-NNNN-archive.md` | `archive` | Append-only history of superseded and demoted records, plus per-session checkpoints in frontmatter. | No fixed ceiling; loaded selectively (on rebuild, restore, historical lookup). |

`NNNN` is the shared-set generation counter (see the naming contract above). All three files of one generation carry the same `NNNN`.

`user-config.md`, `org-config.md`, and `platform-specific-parameters.md` are configuration files, not data files. They are operator-editable and live in `config/` (see `references/configure.md`); the skill reads them by base name. Their templates ship as `config/user-config.md.template`, `config/org-config.md.template`, and `config/platform-specific-parameters.md.template`. Config-file frontmatter is defined in section 2.1 below.

## 2. File-level YAML frontmatter

Every file the skill writes begins with this frontmatter. Fields marked OPTIONAL may be absent or null.

```yaml
---
# Schema identification
schema_version: "0.5"                            # REQUIRED, string. Decoupled from skill version. Bumps only when schema fields change. See references/schema-changelog.md.
_managed_by: project-context-skill               # REQUIRED in schema 0.3+. String literal. Registry marker used by pre-flight detection — see references/preflight.md. The leading underscore signals internal metadata, not user-facing data.
generation: <integer>                            # REQUIRED in schema 0.5+. Identity counter. Matches the filename NNNN (pc-NNNN-*). All three files of a set share it. Distinct from update_count; never feeds scoring. See the naming contract and section 6.
file_role: project-context | entities | archive  # REQUIRED

# Topology (v0.6.0, schema 0.4+) — full schema, role definitions, and validation rules in references/topology.md
topology:                                        # REQUIRED block in schema 0.4+. Universal across all roles.
  role: "hub" | "spoke-dev" | "spoke-solution" | "standalone" | "unclassified"   # REQUIRED, one of five enum values
  hub_reference: <string|null>                   # REQUIRED, populated for spoke-* roles; null otherwise
  hub_version: <string|null>                     # REQUIRED, populated for spoke-* roles; null otherwise
  last_hub_sync: <ISO-8601|null>                 # REQUIRED, populated for spoke-* roles; null otherwise
  parent: <string|null>                          # REQUIRED, populated for child spokes in hybrid topology; null otherwise
  declared_by: "operator" | "skill-default"      # REQUIRED
  declared_at: <ISO-8601>                        # REQUIRED

# Project identification
project: <human-readable project name>           # REQUIRED, string
project_id: <slug>                               # REQUIRED, string, kebab-case

# Lifecycle
created: <ISO-8601 timestamp>                    # REQUIRED
last_merged: <ISO-8601 timestamp>                # REQUIRED
update_count: <integer>                          # REQUIRED, monotonic. RETAINED in schema 0.5. The scoring lifecycle counter (drives update-based decay in references/scoring.md). Distinct from generation. Preserved verbatim across Scenario G; never reset by migration.
record_count: <integer>                          # REQUIRED, count of records in this file

# Display and parsing aids
read_order: [<section names>]                    # REQUIRED, list (per file_role; see section 4)
how_to_read: |                                   # REQUIRED, multi-line plain-text instruction for AI readers
  <one to three sentences>
id_prefix_legend:                                # REQUIRED, map of all ID prefixes used by the skill
  dec: "Decision (in project-context.md)"
  con: "Constraint (in project-context.md)"
  csn: "Current State (in project-context.md)"
  opn: "Open Item (in project-context.md)"
  trm: "Terminology (in project-context.md)"
  ref: "External Reference (in project-context.md)"
  ent: "Entity (in entities.md)"
  arc: "Archived Record (in project-context-archive.md)"

# Cross-references
authors: [<list of user identifiers>]            # REQUIRED, list, may be [] (nullable in v0.5.0 pending platform identity API)
related_session_recap: <optional path>           # OPTIONAL, may be null
related_files: [<list of paths>]                 # OPTIONAL, may be []

# Governance (inherited from v0.1.0 governance framework)
sensitivity: open | internal | confidential | restricted   # REQUIRED
retention: standard | extended | indefinite                # REQUIRED
governance_frameworks: []                                   # REQUIRED, may be []
custom_governance: {}                                       # REQUIRED, may be {}

# Archive-only fields (present only when file_role == "archive")
checkpoints:                                     # REQUIRED on archive files; omitted on others
  - update: <integer>
    timestamp: <ISO-8601>
    summary: <string>
    approver: <user identifier or null>

# Generation metadata
generated_by:
  skill: project-context
  version: <semver>                              # the skill version, e.g. "0.5.0"
  model: <model identifier>
  generation_date: <ISO-8601 timestamp>
---
```

### Field-by-field reference

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | The data-shape contract. The skill writes `"0.5"`. Bumps only when fields change; see `references/schema-changelog.md`. |
| `_managed_by` | yes (schema 0.3+) | String literal `project-context-skill`. Registry marker. Makes pre-flight detection reliable: `project_knowledge_search` for this distinctive YAML field returns only chunks from files under skill management. See `references/preflight.md`. |
| `generation` | yes (schema 0.5+) | Integer identity counter equal to the filename `NNNN` (`pc-NNNN-*`). Shared across all three files of a set. Distinct from `update_count`; it is filename identity, not a scoring input. The filename counter and `generation` must agree; a mismatch is a pre-flight diagnostic (see `references/preflight.md` and section 6). Counter assignment and the confirmed-empty rule live in `references/preflight.md`. |
| `file_role` | yes | One of `project-context`, `entities`, `archive`. Must match the file's role per the `pc-NNNN-{context,entities,archive}` suffix. |
| `topology` | yes (schema 0.4+) | Block-level frontmatter field carrying the project's topology role and Hub relationship. Universal across all projects; every role has its own required-non-null and required-null field set per `references/topology.md` section 6.1. Validation rules (role enum check, declared_by enum check, ISO 8601 check, no-empty-fields) live in `references/topology.md` section 6 and are applied at pre-flight per `references/preflight.md` section 10. |
| `project` | yes | Human-readable project name. |
| `project_id` | yes | kebab-case slug used for cross-file references. |
| `created` | yes | ISO-8601 with timezone; the date this file was first written. |
| `last_merged` | yes | ISO-8601; updated every successful merge. |
| `update_count` | yes | Monotonic integer; increments by one per successful merge. RETAINED in schema 0.5 as the scoring lifecycle counter (`references/scoring.md`). Distinct from `generation`: `update_count` drives decay, `generation` is filename identity. Preserved verbatim across all migrations including Scenario G; never reset. |
| `record_count` | yes | Count of records currently in this file's body. |
| `read_order` | yes | List of section names in display order. Per `file_role`; see section 4. |
| `how_to_read` | yes | One to three sentences telling an AI reader how to consume this file. |
| `id_prefix_legend` | yes | Map of every ID prefix the skill uses. Present in every file to give cross-file readers a complete legend regardless of which file they loaded. |
| `authors` | yes | List, may be `[]`. Reserved for future platform-identity API. |
| `related_session_recap` | no | Filename of a session-recap file for the same project, or null. |
| `related_files` | no | Other related files; may be `[]`. |
| `sensitivity` | yes | One of `open`, `internal`, `confidential`, `restricted`. Default `internal`. |
| `retention` | yes | One of `standard`, `extended`, `indefinite`. Default `standard`. Archive files default to `indefinite`. |
| `governance_frameworks` | yes | Free-form list, may be `[]`. |
| `custom_governance` | yes | Free-form object, may be `{}`. |
| `checkpoints` | only on archive | Ordered list of per-merge checkpoint objects. See section 5.3. |
| `generated_by.skill` | yes | Always `project-context`. |
| `generated_by.version` | yes | The skill version that originally generated the records in this file (e.g., `"0.6.0"`). Independent of `schema_version`. Preserved unchanged across upgrade migrations — the field records original generation, not subsequent metadata-only rewrites. |
| `generated_by.model` | yes | The model that originally generated the records in this file (e.g., `claude-opus-4-7`). Preserved unchanged across upgrade migrations — the field records original generation, not subsequent metadata-only rewrites. |
| `generated_by.generation_date` | yes | ISO-8601 timestamp marking when the records in this file were originally generated. Preserved unchanged across upgrade migrations — the field records original generation, not subsequent metadata-only rewrites. Upgrade traceability is the `schema_version` bump, not this field. |

Frontmatter resolution order when the skill writes a file: `user-config.md` defaults > `org-config.md` defaults > skill defaults from `references/defaults.md` > field-level inferences from project state.

### 2.1 Config-file frontmatter (schema 0.5)

Configuration files (`user-config.md`, `org-config.md`, `platform-specific-parameters.md`) are operator-editable and carry their own minimal frontmatter. They are NOT data files and do NOT carry `generation`, `update_count`, `topology`, `record_count`, or any per-record schema. Their bodies are unchanged from v0.6.0 except for the self-documenting header and local field guide (see `references/configure.md`).

```yaml
---
schema_version: "0.5"                            # REQUIRED, string. Bumped to "0.5" in v0.7.0.
_managed_by: project-context-skill               # REQUIRED. Same registry marker as data files.
config_type: "user" | "org" | "platform"         # REQUIRED. Which configuration layer this file is.
config_editable: true                            # REQUIRED in schema 0.5+. Declares the file operator-editable. Always true for config files.
configure_with: references/configure.md           # REQUIRED in schema 0.5+. Points at the shared interview mechanics that regenerate this file.
---
```

| Field | Required | Notes |
|---|---|---|
| `schema_version` | yes | `"0.5"` for v0.7.0 config files. |
| `_managed_by` | yes | `project-context-skill`. |
| `config_type` | yes | `user`, `org`, or `platform`. Distinguishes the three config files. |
| `config_editable` | yes (schema 0.5+) | Literal `true`. The location (`config/`) and this flag together declare operator ownership (convention P4). |
| `configure_with` | yes (schema 0.5+) | `references/configure.md`. The single owner of interview mechanics; the local field guide in each config file documents that file's own fields. |

Rendered config files (instantiated from the `.template` files into the operator's project) do NOT inherit the SPDX header from the template. The `config_editable` and `configure_with` header lines are present on both the template and the rendered file.

## 3. Per-record schema

Records are written under section headers (e.g., `## Decisions`) as markdown list items with a YAML metadata block beneath each bullet.

```yaml
- id: <prefix>-<NNN>                          # REQUIRED, kebab-case prefix + zero-padded number
  content: <record text>                      # REQUIRED, plain string
  section: <section name>                     # REQUIRED, matches read_order

  # Lifecycle
  first_seen_update: <integer>                # REQUIRED, update_count when first added
  last_seen_update: <integer>                 # REQUIRED, update_count when last reinforced
  first_seen_at: <ISO-8601>                   # REQUIRED, wall-clock at first add (drives the 3-year floor)
  last_seen_at: <ISO-8601>                    # REQUIRED, wall-clock at last reinforcement
  times_seen: <integer>                       # REQUIRED, reinforcement count, default 1

  # Scoring
  importance: <integer 1-10>                  # REQUIRED, LLM-assigned at ingest, user may override

  # Status
  status: active | superseded | archived      # REQUIRED

  # Provenance
  source_quote: <verbatim text>               # REQUIRED, from conversation or external file
  source_kind: chat | external_file           # REQUIRED
  source_ref: <chat session ID or file path>  # REQUIRED

  # Relationships
  links: [<list of record IDs>]               # REQUIRED, may be []

  # Audit
  audit:
    approval_mode: auto | manual | hybrid     # REQUIRED
    approved_by: <user identifier or null>    # REQUIRED, null in v0.5.0 pending platform identity API
    approved_at: <ISO-8601>                   # REQUIRED
    warning_response: acknowledged | passive | dismissed | n/a   # REQUIRED
    importance_source: llm-auto | user-override                   # REQUIRED
```

Auto-approved records carry a visible `[AUTO]` prefix on the `content` field for human-readability:

```yaml
- id: dec-021
  content: "[AUTO] Lock the v0.4.0 ship date at end of May."
  ...
  audit:
    approval_mode: auto
    ...
```

Archive records carry two additional fields:

```yaml
prior_id: <original record ID before archiving>     # REQUIRED on archive records
superseded_by: <ID of the record that replaced this one>  # REQUIRED when status == superseded
superseded_at_update: <integer>                     # REQUIRED when status == superseded
demoted_at_update: <integer>                        # REQUIRED when status == archived
restore_command: <chat command string>              # OPTIONAL, hint shown to users for restoration
```

### ID prefix conventions

| Prefix | File | Section |
|---|---|---|
| `dec-` | `project-context.md` | Decisions |
| `con-` | `project-context.md` | Constraints |
| `csn-` | `project-context.md` | Current State |
| `opn-` | `project-context.md` | Open Items |
| `trm-` | `project-context.md` | Terminology |
| `ref-` | `project-context.md` | External References |
| `ent-` | `entities.md` | All entity records (across sub-sections) |
| `arc-` | `project-context-archive.md` | All archived records |

IDs are unique within the project. The prefix encodes the file, so cross-file links use just the ID: `links: [dec-012, ent-007]`.

## 4. Body sections by file_role

### 4.1 `pc-NNNN-context.md` (`read_order`)

1. **Decisions** (prefix `dec-`) — choices made and committed.
2. **Constraints** (prefix `con-`) — non-negotiable boundaries, limits, rules.
3. **Current State** (prefix `csn-`) — facts about the present, expected to evolve.
4. **Open Items** (prefix `opn-`) — questions, blockers, pending decisions.
5. **Terminology** (prefix `trm-`) — definitions, glossary, agreed vocabulary.
6. **External References** (prefix `ref-`) — links to documents, papers, conversations, files outside this project.

Empty sections contain the literal line `_No records in this section._`

### 4.2 `pc-NNNN-entities.md` (`read_order`)

1. **People** — named individuals.
2. **Places** — locations, regions, venues.
3. **Things** — products, tools, artifacts, datasets.
4. **Organizations** — companies, teams, groups.
5. **Datasets** — named data sources referenced repeatedly.

All entity records use prefix `ent-`. Empty sub-sections use the same placeholder.

### 4.3 `pc-NNNN-archive.md` (`read_order`)

One body section, `## Records`. Flat list of all archived entries discriminated by the `status` field:

- `status: superseded` — record contradicted by a newer record and replaced. The replacement's ID is in `superseded_by`.
- `status: archived` — record aged out via DEMOTE but remains true. No replacement.

This is a deliberate v0.4.0 design choice. Machine ingestion (rebuild, scoring, audit) reads by `status`, not by section header. A flat list with status discrimination is the cleaner schema for the primary consumer. Human readers will filter via AI assistance, which treats the file as data regardless of section structure.

Session checkpoints — per-merge summaries — are not body records. They live in the frontmatter `checkpoints` array (see 5.3). This separates two different shapes of entry: records (the things being archived) and checkpoints (the meta-log of when activity happened).

## 5. Special schema cases

### 5.1 First-run placeholder block

On first invocation, each file is created eagerly with frontmatter and a placeholder block wrapped in HTML comments:

```markdown
<!-- PROJECT_CONTEXT_PLACEHOLDER_START -->
This file is empty.
... (one-paragraph explanation) ...
If you are an AI agent reading this file, treat it as currently containing
zero records. Do not interpret this placeholder text as data.
<!-- PROJECT_CONTEXT_PLACEHOLDER_END -->

## <first section header>

_No records yet._
```

The skill removes the entire placeholder block (delimiters and content) on the first successful ADD. See `operations/default.md`.

### 5.2 Auto-mode `[AUTO]` prefix

Records added under `audit.approval_mode: auto` carry a literal `[AUTO]` prefix on `content`. The prefix is a plain string token, not a YAML tag — readability for both AI and human readers. Combined with `audit.approval_mode`, this gives two signals (visible in content, structured in audit) for auto-approval.

### 5.3 Archive `checkpoints` array

Frontmatter-only. Ordered list of per-merge checkpoint objects:

```yaml
checkpoints:
  - update: <integer>          # the update_count value at this checkpoint
    timestamp: <ISO-8601>      # wall-clock time of the merge
    summary: <string>          # one-line description of what changed
    approver: <user identifier or null>
```

Reading agents that want "what happened in the last N updates" parse `checkpoints`. Reading agents that want "what records are archived" parse the body. The two queries do not interfere.

## 6. Validation checklist

A file conforms to schema "0.5" when:

1. Frontmatter is valid YAML and includes every REQUIRED field above.
2. `schema_version` is exactly `"0.5"`.
3. `_managed_by` is present and equals exactly the string `project-context-skill`.
4. The filename matches the `pc-NNNN-{context,entities,archive}.md` pattern and `file_role` matches the suffix (`context` → `project-context`, `entities` → `entities`, `archive` → `archive`).
5. `generation` is present, is a non-negative integer, and equals the `NNNN` in the filename. A mismatch is a pre-flight diagnostic (see `references/preflight.md`).
6. `update_count` is present (RETAINED in schema 0.5) and is a monotonic integer. It is distinct from `generation` and is the scoring lifecycle counter.
7. `topology` block is present in frontmatter and conforms to the topology schema and validation rules in `references/topology.md` (role is one of the five enum values; required-by-role fields per section 6.1; no empty fields; `declared_by` is `operator` or `skill-default`; `declared_at` parses as ISO 8601).
8. `id_prefix_legend` is present and includes all eight prefixes.
9. The body uses the `read_order` defined for the file's `file_role`.
10. Empty sections contain exactly `_No records in this section._`
11. Every record carries the REQUIRED record-level fields (lifecycle, scoring, status, provenance, links, audit).
12. Every record's ID prefix matches the section/file per the prefix table.
13. `status` is one of `active`, `superseded`, `archived`.
14. Archive files include a `checkpoints` frontmatter array (may be `[]` on a freshly initialized archive).
15. Auto-approved records have `[AUTO]` prefix on `content` AND `audit.approval_mode: auto`.
16. For `pc-NNNN-context.md` files with `topology.role: hub`, the body includes a `## Spoke Inventory` section immediately after frontmatter, formatted per `references/topology.md` section 3 (Name | Role | Artifact Type | Source Hub Version | Status | Parent). Empty spoke inventory renders as the heading plus column header row only.
17. The recognition contract holds: the file is identified as a managed context file by BOTH the `pc-NNNN-*` filename pattern AND the `_managed_by: project-context-skill` marker (see `references/preflight.md`).

Operations reference this checklist in their final validation pass.

## 7. Cross-references

- Skill-version vs schema-version decoupling, schema-changelog, Supported Schemas matrix: `references/schema-changelog.md`.
- Pre-flight algorithm, report block, token catalog, post-flight summary, topology validation, stale-spoke detection, audit trigger handler, role-declaration prompts: `references/preflight.md`.
- Topology block schema, role definitions, spoke inventory format, audit trigger semantics, hybrid topology rules, validation rules: `references/topology.md`.
- Scoring inputs (`times_seen`, `importance`, etc.): `references/scoring.md`.
- Migration from schema "0.1" (v0.1-era, Scenario D), "0.2" (v0.4.0 upgrade, Scenario E), "0.3" (v0.5.0 topology upgrade, Scenario F), and "0.4" (v0.6.0 to v0.7.0 generation/naming upgrade, Scenario G): `references/migration.md`.
- Counter assignment, confirmed-empty rule, generation self-consistency check, naming contract enforcement: `references/preflight.md`.
- Default values for every overridable field: `references/defaults.md`.
- Configuration interview mechanics and the config/references separation: `references/configure.md`.
- Configuration overrides (operator-editable, read by base name): `config/user-config.md.template`, `config/org-config.md.template`, `config/platform-specific-parameters.md.template`.
- Worked examples: `references/examples/`.
