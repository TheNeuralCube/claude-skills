# Example: `entities.md` after a few sessions

The block below is a realistic example of the entities reference file. It is illustrative only — the project, names, and content are fictional. Generated-output examples do NOT carry SPDX headers.

```markdown
---
schema_version: "0.3"
_managed_by: project-context-skill
file_role: entities
project: "Q3 Strategic Review"
project_id: "q3-strategic-review-2026"
created: 2026-05-13T14:00:00-05:00
last_merged: 2026-05-13T16:42:00-05:00
update_count: 14
record_count: 4
read_order: [people, places, things, organizations, datasets]
how_to_read: |
  Stable reference data for the Q3 Strategic Review project. Look up entries
  by name; this file does not undergo automatic decay. New entries are added
  as entities are mentioned in conversations.
id_prefix_legend:
  dec: "Decision (in project-context.md)"
  con: "Constraint (in project-context.md)"
  csn: "Current State (in project-context.md)"
  opn: "Open Item (in project-context.md)"
  trm: "Terminology (in project-context.md)"
  ref: "External Reference (in project-context.md)"
  ent: "Entity (in entities.md)"
  arc: "Archived Record (in project-context-archive.md)"
authors: []
related_session_recap: null
related_files: []
sensitivity: internal
retention: standard
governance_frameworks: []
custom_governance: {}
generated_by:
  skill: project-context
  version: "0.5.0"
  model: claude-opus-4-7
  generation_date: 2026-05-13T16:42:00-05:00
---

## People

- id: ent-001
  content: "Sarah Chen — Director of Customer Analytics; primary owner of the segmentation model."
  section: people
  first_seen_update: 2
  last_seen_update: 13
  first_seen_at: 2026-04-22T10:15:00-05:00
  last_seen_at: 2026-05-12T11:00:00-05:00
  times_seen: 5
  importance: 8
  status: active
  source_quote: "Sarah owns segmentation."
  source_kind: chat
  source_ref: 2026-04-22-segmentation-discussion
  links: [dec-001]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-22T10:30:00-05:00
    warning_response: n/a
    importance_source: llm-auto

- id: ent-002
  content: "Priya Shah — Finance lead; pricing decision approver."
  section: people
  first_seen_update: 11
  last_seen_update: 13
  first_seen_at: 2026-05-09T15:00:00-05:00
  last_seen_at: 2026-05-12T11:00:00-05:00
  times_seen: 2
  importance: 7
  status: active
  source_quote: "Priya signed off on the new pricing."
  source_kind: chat
  source_ref: 2026-05-09-pricing-discussion
  links: []
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-05-09T15:10:00-05:00
    warning_response: n/a
    importance_source: llm-auto

## Places

_No records in this section._

## Things

_No records in this section._

## Organizations

- id: ent-014
  content: "Acme Corp — pilot enterprise customer for the new tiering structure."
  section: organizations
  first_seen_update: 3
  last_seen_update: 12
  first_seen_at: 2026-04-25T09:00:00-05:00
  last_seen_at: 2026-05-11T14:00:00-05:00
  times_seen: 3
  importance: 6
  status: active
  source_quote: "Acme is the pilot for the new tier-1 structure."
  source_kind: chat
  source_ref: 2026-04-25-checkin
  links: [dec-001, csn-011]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-25T09:10:00-05:00
    warning_response: n/a
    importance_source: llm-auto

## Datasets

- id: ent-018
  content: "CSAT-2026 dataset — canonical customer satisfaction dataset for the Q3 review."
  section: datasets
  first_seen_update: 4
  last_seen_update: 10
  first_seen_at: 2026-04-28T10:00:00-05:00
  last_seen_at: 2026-05-08T14:00:00-05:00
  times_seen: 2
  importance: 6
  status: active
  source_quote: "Use CSAT-2026 as the canonical dataset."
  source_kind: chat
  source_ref: 2026-04-28-data-review
  links: []
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-28T10:10:00-05:00
    warning_response: n/a
    importance_source: llm-auto
```
