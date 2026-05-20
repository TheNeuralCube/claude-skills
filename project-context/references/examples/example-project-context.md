# Example: `project-context.md` after a routine v0.5.0 session

The block below is a realistic example of the active grounding file (`project-context.md`) after several sessions. It is illustrative only — the project, names, and content are fictional. Generated-output examples do NOT carry SPDX headers (this file is operator work product, not skill source).

```markdown
---
schema_version: "0.3"
_managed_by: project-context-skill
file_role: project-context
project: "Q3 Strategic Review"
project_id: "q3-strategic-review-2026"
created: 2026-05-13T14:00:00-05:00
last_merged: 2026-05-13T16:42:00-05:00
update_count: 14
record_count: 5
read_order: [decisions, constraints, current_state, open_items, terminology, external_references]
how_to_read: |
  This is the active project context for the Q3 Strategic Review project.
  Read decisions and constraints in full. Treat current state as evolving.
  Open items are pending decisions. Look up terminology and external
  references by need. Entities live in entities.md; historical records
  live in project-context-archive.md.
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

## Decisions

- id: dec-001
  content: "Adopt the four-segment customer model (enterprise, mid-market, SMB, individual)."
  section: decisions
  first_seen_update: 2
  last_seen_update: 13
  first_seen_at: 2026-04-22T10:15:00-05:00
  last_seen_at: 2026-05-13T16:42:00-05:00
  times_seen: 8
  importance: 9
  status: active
  source_quote: "We're going with the four-segment model: enterprise, mid-market, SMB, individual."
  source_kind: chat
  source_ref: 2026-04-22-segmentation-discussion
  links: [con-003, ent-014]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-22T10:30:00-05:00
    warning_response: n/a
    importance_source: llm-auto

- id: dec-024
  content: "[AUTO] Lock the v0.4.0 ship date at end of May."
  section: decisions
  first_seen_update: 14
  last_seen_update: 14
  first_seen_at: 2026-05-13T16:38:00-05:00
  last_seen_at: 2026-05-13T16:38:00-05:00
  times_seen: 1
  importance: 7
  status: active
  source_quote: "We're targeting end of May for v0.4.0 ship."
  source_kind: chat
  source_ref: 2026-05-13-design-workshop
  links: []
  audit:
    approval_mode: auto
    approved_by: null
    approved_at: 2026-05-13T16:38:00-05:00
    warning_response: passive
    importance_source: llm-auto

## Constraints

- id: con-003
  content: "Tier-2 enterprise pricing review must be completed before Q4 OKRs are locked."
  section: constraints
  first_seen_update: 5
  last_seen_update: 11
  first_seen_at: 2026-04-30T11:00:00-05:00
  last_seen_at: 2026-05-09T15:20:00-05:00
  times_seen: 3
  importance: 8
  status: active
  source_quote: "Whatever happens with pricing, it has to be locked before the Q4 OKR cycle starts."
  source_kind: chat
  source_ref: 2026-04-30-pricing-discussion
  links: [dec-001]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-30T11:10:00-05:00
    warning_response: n/a
    importance_source: llm-auto

## Current State

- id: csn-011
  content: "Customer ID migration is 92% complete; tier-2 mid-market is the remaining 8%."
  section: current_state
  first_seen_update: 9
  last_seen_update: 14
  first_seen_at: 2026-05-04T10:00:00-05:00
  last_seen_at: 2026-05-13T16:42:00-05:00
  times_seen: 4
  importance: 6
  status: active
  source_quote: "Migration's at 92 percent — mid-market's the long pole."
  source_kind: chat
  source_ref: 2026-05-13-design-workshop
  links: [ent-014]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-05-04T10:15:00-05:00
    warning_response: n/a
    importance_source: user-override

## Open Items

- id: opn-007
  content: "Schedule the Q4 OKR pre-read with the leadership team by 2026-05-25."
  section: open_items
  first_seen_update: 13
  last_seen_update: 13
  first_seen_at: 2026-05-12T11:00:00-05:00
  last_seen_at: 2026-05-12T11:00:00-05:00
  times_seen: 1
  importance: 6
  status: active
  source_quote: "We need the pre-read out before the 25th."
  source_kind: chat
  source_ref: 2026-05-12-research-review
  links: [con-003]
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-05-12T11:05:00-05:00
    warning_response: n/a
    importance_source: llm-auto

## Terminology

_No records in this section._

## External References

_No records in this section._
```
