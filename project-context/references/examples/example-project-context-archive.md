# Example: `project-context-archive.md` after a few demotions and one supersession

The block below is a realistic example of the archive file. It is illustrative only — the project, names, and content are fictional. Generated-output examples do NOT carry SPDX headers.

Note the structure: a flat `## Records` body discriminated by the `status` field (`superseded` vs `archived`), with the per-merge `checkpoints` array living in the YAML frontmatter (NOT in the body). This is the v0.3 schema convention.

```markdown
---
schema_version: "0.3"
_managed_by: project-context-skill
file_role: archive
project: "Q3 Strategic Review"
project_id: "q3-strategic-review-2026"
created: 2026-05-13T14:00:00-05:00
last_merged: 2026-05-13T16:42:00-05:00
update_count: 14
record_count: 2
read_order: [records]
how_to_read: |
  This is the archive for the Q3 Strategic Review project. Records here are
  historical: either superseded by newer records (with prior_id pointer) or
  demoted from active because they no longer meet the active threshold.
  Filter by `status` to distinguish: `superseded` for contradicted records,
  `archived` for demoted records. Per-merge checkpoint history lives in the
  `checkpoints` frontmatter array, not in the body. Treat as read-only history.
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
retention: indefinite
governance_frameworks: []
custom_governance: {}
checkpoints:
  - update: 14
    timestamp: 2026-05-13T16:42:00-05:00
    summary: "3 ADDs, 1 UPDATE, 1 DEMOTE. Routine session."
    approver: null
  - update: 13
    timestamp: 2026-05-12T11:00:00-05:00
    summary: "2 ADDs, 1 SUPERSEDE (dec-018 to dec-021). Research review."
    approver: null
  - update: 12
    timestamp: 2026-05-11T15:00:00-05:00
    summary: "1 ADD. Brief session."
    approver: null
generated_by:
  skill: project-context
  version: "0.5.0"
  model: claude-opus-4-7
  generation_date: 2026-05-13T16:42:00-05:00
---

## Records

- id: arc-001
  prior_id: dec-018
  content: "Use Park et al. retrieval scoring for record prioritization."
  section: decisions
  first_seen_update: 8
  last_seen_update: 10
  first_seen_at: 2026-05-09T14:00:00-05:00
  last_seen_at: 2026-05-11T10:00:00-05:00
  times_seen: 2
  importance: 7
  status: superseded
  superseded_by: dec-021
  superseded_at_update: 12
  source_quote: "Let's use the Park scoring formula."
  source_kind: chat
  source_ref: 2026-05-09-research-review
  links: []
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-05-09T14:30:00-05:00
    warning_response: n/a
    importance_source: llm-auto
  restore_command: "restore arc-001"

- id: arc-002
  prior_id: csn-007
  content: "Mid-quarter check-in shows 60% of segments validated."
  section: current_state
  first_seen_update: 3
  last_seen_update: 5
  first_seen_at: 2026-04-25T14:00:00-05:00
  last_seen_at: 2026-04-28T16:00:00-05:00
  times_seen: 1
  importance: 4
  status: archived
  demoted_at_update: 11
  source_quote: "We're at about 60% segment validation at the mid-point."
  source_kind: chat
  source_ref: 2026-04-25-checkin
  links: []
  audit:
    approval_mode: manual
    approved_by: null
    approved_at: 2026-04-25T14:30:00-05:00
    warning_response: n/a
    importance_source: llm-auto
  restore_command: "restore arc-002"
```
