# Example: `pc-0014-context.md` (schema 0.5) after a routine v0.7.0 session

The block below is a realistic example of the active grounding file after several sessions. The file is named `pc-0014-context.md`: `NNNN` is the shared-set `generation` counter (here 14), distinct from `update_count` (the scoring counter, also 14 here because the context file was written in every generation; the two need not coincide). It is illustrative only — the project, names, and content are fictional. Generated-output examples do NOT carry SPDX headers (this file is operator work product, not skill source). In the legend and reader instructions below, `pc-NNNN-*` is shown generically; the actual files in this set are `pc-0014-context.md`, `pc-0014-entities.md`, and `pc-0014-archive.md`.

The example uses `topology.role: standalone` (no Hub relationship); see `references/topology.md` for the full topology schema and the four other role options (hub, spoke-dev, spoke-solution, unclassified). A `role: hub` example would additionally carry a `## Spoke Inventory` section in the body immediately after frontmatter.

```markdown
---
schema_version: "0.5"
_managed_by: project-context-skill
generation: 14
file_role: project-context
topology:
  role: "standalone"
  hub_reference: null
  hub_version: null
  last_hub_sync: null
  parent: null
  declared_by: "operator"
  declared_at: 2026-05-13T14:00:00-05:00
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
  references by need. Entities live in pc-NNNN-entities.md; historical records
  live in pc-NNNN-archive.md.
id_prefix_legend:
  dec: "Decision (in pc-NNNN-context.md)"
  con: "Constraint (in pc-NNNN-context.md)"
  csn: "Current State (in pc-NNNN-context.md)"
  opn: "Open Item (in pc-NNNN-context.md)"
  trm: "Terminology (in pc-NNNN-context.md)"
  ref: "External Reference (in pc-NNNN-context.md)"
  ent: "Entity (in pc-NNNN-entities.md)"
  arc: "Archived Record (in pc-NNNN-archive.md)"
authors: []
related_session_recap: null
related_files: []
sensitivity: internal
retention: standard
governance_frameworks: []
custom_governance: {}
generated_by:
  skill: project-context
  version: "0.7.0"
  model: claude-opus-4-8
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
