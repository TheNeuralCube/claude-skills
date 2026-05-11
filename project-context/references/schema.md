<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context schema (v0.1.0)

This file is the authoritative restatement of the schema for any file the project-context skill produces. Mode files reference this document. The model uses it during generation and during consolidation to validate output.

If org-config.md overrides any default below, the override applies; otherwise the values here apply.

## File-level YAML frontmatter

Every project-context file begins with a YAML frontmatter block delimited by `---` lines:

```yaml
---
file_type: project-context
file_subtype: fresh | consolidated
schema_version: v0.1.0
created: <ISO 8601 timestamp with timezone, e.g. 2026-05-08T14:30:00-05:00>
project_name: <string>
session_topic: <short sentence-case description>
sessions_covered: [list of session references]
source_files: [list of filenames]
related_session_recap: <filename or null>
related_files: [list of filenames]

sensitivity: open | internal | confidential | restricted
audience: <free-form string>
retention: standard | extended | legal_hold | delete_after_<period>
governance_frameworks: [list of strings]
custom_governance: <object>

generated_by:
  skill: project-context
  version: v0.1.0
  mode: generate | consolidate
  model: <model identifier>
  generation_date: <ISO 8601 timestamp>
---
```

### Field-by-field

| Field | Required | Notes |
|---|---|---|
| `file_type` | yes | Always the literal string `project-context`. |
| `file_subtype` | yes | `fresh` for generate-mode output. `consolidated` for consolidate-mode output. |
| `schema_version` | yes | The schema version this file conforms to. v0.1.0 files write `v0.1.0`. |
| `created` | yes | ISO 8601 with timezone. Use the operator's local timezone if known; otherwise UTC. |
| `project_name` | yes | The Claude Project / ChatGPT Project / Copilot M365 Project name. Operator-supplied or inferred from project context. |
| `session_topic` | yes | A short sentence-case description of what the session covered. |
| `sessions_covered` | yes | List of session references. For fresh files, usually one entry. For consolidated files, multiple — typically a date range like `"2026-04-15 through 2026-08-14"`. |
| `source_files` | yes | List of filenames. Empty `[]` for fresh files. For consolidated files, the full filenames of every project-context file merged in. |
| `related_session_recap` | no | Filename of a session-recap file produced for the same session, or `null`. Cross-skill awareness, not dependency. |
| `related_files` | no | Filenames of other project-context files this one builds on (e.g., the prior session in the same project). Empty list `[]` if none. |
| `sensitivity` | no | One of `open`, `internal`, `confidential`, `restricted`. Upstream default: `internal`. |
| `audience` | no | Free-form string. Org-config can constrain to a vocabulary. |
| `retention` | no | One of `standard`, `extended`, `legal_hold`, or `delete_after_<period>`. Upstream default: `standard`. |
| `governance_frameworks` | no | Free-form list (e.g., `[HIPAA, SOX, GDPR, internal-IP]`). Empty by default. |
| `custom_governance` | no | Free-form key-value object for org-specific extensions. Empty `{}` by default. |
| `generated_by.skill` | yes | Always `project-context`. |
| `generated_by.version` | yes | The skill version that produced the file (e.g., `v0.1.0`). |
| `generated_by.mode` | yes | `generate` or `consolidate`. |
| `generated_by.model` | no | Model identifier (e.g., `claude-opus-4-7`). Populate when known; omit if not. |
| `generated_by.generation_date` | yes | ISO 8601 timestamp when the file was produced. Often equal to `created`. |

For consolidated files, an additional optional block summarizes the consolidation:

```yaml
consolidation_summary:
  source_file_count: <integer>
  records_after_dedup: <integer>
  records_dropped_transient: <integer>
  records_compressed_summary: <integer>
```

All governance fields are optional. The skill must produce valid output even when every governance field is absent.

## Body section structure

After the frontmatter, the body uses **exactly seven** section headers, in this order, every time:

```markdown
## Decisions
## Constraints
## Entities
## Terminology
## External references
## Open items
## State snapshot
```

**Sections are always present, even when empty.** An empty section contains exactly one line:

```
_No records in this section._
```

Do not invent additional sections. Do not reorder. Do not merge sections. The predictability is for downstream AI parsing efficiency.

### What goes in each section

- **Decisions.** Choices made during the session that constrain future work. Includes "we will do X", "we will not do Y", "we have agreed on Z".
- **Constraints.** Rules, requirements, limits, or standards the project must respect. Includes "all work must use schema X", "feature Y is out of scope", "data Z is confidential".
- **Entities.** Named people, systems, datasets, organizations, or artifacts that matter to future work in the project. One record per named entity.
- **Terminology.** Definitions, glossary entries, or shared vocabulary the project uses. One record per term.
- **External references.** Pointers to documents, links, datasets, or external artifacts the project depends on. One record per reference.
- **Open items.** Unresolved questions, pending tasks, or in-flight work. One record per open item.
- **State snapshot.** A point-in-time description of the project's current status (progress percentages, milestones reached, blockers active). One record per state fact.

## Per-item record format

Every record is a markdown bullet at the top level of its section. The format is:

```markdown
- <record content as one or more sentences>. [tier: full | summary | transient] [categories: tag1, tag2, tag3]
```

Each record is a self-contained unit. A reader should be able to extract any single record and understand it without reading the surrounding records. Avoid pronouns whose antecedents live in other records.

### Section tier defaults

Each section has an implicit tier default. Records that match the section default omit the `[tier: ...]` bracket. Records that diverge declare their tier explicitly.

| Section | Default tier | Rationale |
|---|---|---|
| Decisions | `full` | Decisions almost always preserve fully. |
| Constraints | `full` | Constraints preserve fully. |
| Entities | `full` | Named entities preserve fully. |
| Terminology | `full` | Terminology preserves fully. |
| External references | `full` | Pointers to external artifacts preserve fully. |
| Open items | `summary` | Open items often resolve and become stale. |
| State snapshot | `summary` | State changes between sessions. |

Org-config can override these defaults; see `org-config-template.md`.

### Tier semantics

- **`full`** — preserved verbatim through consolidation. Decisions, constraints, owner intent, named entities default here.
- **`summary`** — compressed during consolidation when stale; the gist is preserved, the verbatim form is not. In-flight reasoning, completed workstream details, and state snapshots default here.
- **`transient`** — dropped on consolidation. Used for redundant restatements, conversational scaffolding, or details that have no forward-grounding value.

### Categories

Categories are open multi-tag attributes assigned by the model based on record content. There is no canonical taxonomy at the upstream level. The model assigns one or more categories per record.

Illustrative (not exhaustive) categories: `business`, `technical`, `relationships`, `career`, `governance`, `finance`, `legal`, `vendor`, `customer`, `product`, `infrastructure`, `process`, `strategy`, `planning`, `analysis`, `documentation`, `data`, `definitions`, `scheduling`, `status`.

The model may invent new categories when none of the existing categories fit. Org-config can constrain the model to a fixed vocabulary via `categories.constrain_to_vocabulary: true` plus a `vocabulary` list — see `org-config-template.md`.

### Per-item governance overrides

When a single record has governance values that differ from the file-level frontmatter defaults, the divergence is declared inline as additional bracketed metadata after categories:

```markdown
- <record content>. [tier: full] [categories: vendor, contracts] [sensitivity: confidential]
```

Any of `sensitivity`, `audience`, `retention`, `governance_frameworks`, or arbitrary `custom_governance` keys may appear in inline brackets. Each bracket carries a single field and its value.

### Bracket omission rules

To reduce verbosity:
- **Omit the `[tier: ...]` bracket** when the record's tier matches the section default.
- **Always include the `[categories: ...]` bracket** if any categories apply. (Categories have no section default.)
- **Omit governance brackets** when the record inherits the file-level defaults.

If a record diverges on tier but matches the file-level governance, only the `[tier: ...]` bracket is added.

## Filename format

```
YYYY-MM-DD-project-context.md
YYYY-MM-DD-project-context-{topic-slug}.md
```

- The date prefix is the date the file was produced.
- The topic slug is kebab-case, lowercase, ASCII. Operator-supplied or proposed by the skill and confirmed by the operator.
- Same-day same-topic invocations append to / merge with the existing file rather than creating a duplicate.
- Same-day different-topic invocations produce separate files, discriminated by topic slug.

Consolidated files use:

```
YYYY-MM-DD-project-context-consolidated.md
YYYY-MM-DD-project-context-consolidated-2.md      (if consolidation runs more than once on the same day)
YYYY-MM-DD-project-context-consolidated-3.md
```

## Validation checklist

A file conforms to schema v0.1.0 when:

1. The frontmatter is valid YAML and includes every required field above.
2. `file_type` is `project-context`.
3. `file_subtype` is `fresh` or `consolidated`.
4. `schema_version` is `v0.1.0`.
5. The body contains exactly seven sections, in the prescribed order, with the prescribed headers.
6. Empty sections contain the literal placeholder `_No records in this section._`.
7. Every non-empty record is a top-level bullet whose content is followed by zero or more bracketed metadata fields, each in `[key: value]` form.
8. Tier values are limited to `full`, `summary`, `transient`.
9. The filename matches one of the allowed patterns above.

The mode files reference this checklist when running their final validation pass before producing output.
