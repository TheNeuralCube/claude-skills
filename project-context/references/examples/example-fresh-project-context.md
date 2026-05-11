# Example: fresh project-context file (generate mode)

The block below is a realistic example of a `fresh`-subtype project-context file produced by generate mode. It is illustrative only — the project, names, and content are fictional.

```markdown
---
file_type: project-context
file_subtype: fresh
schema_version: v0.1.0
created: 2026-05-07T18:30:00-05:00
project_name: "Q2 Strategic Review"
session_topic: "Customer segmentation analysis"
sessions_covered: ["2026-05-07 customer segmentation chat"]
source_files: []
related_session_recap: null
related_files: ["2026-05-03-project-context-revenue-baseline.md"]

sensitivity: internal
retention: standard
governance_frameworks: []
custom_governance: {}

generated_by:
  skill: project-context
  version: v0.1.0
  mode: generate
  model: claude-opus-4-7
  generation_date: 2026-05-07T18:30:00-05:00
---

## Decisions

- Adopt the four-segment customer model (enterprise, mid-market, SMB, individual) for Q2 analysis. [categories: customer, strategy]
- Defer the international segmentation question to Q3 to avoid scope creep. [categories: strategy, planning]

## Constraints

- All segmentation work must use the standardized customer ID schema introduced in March; no parallel ID systems. [categories: technical, governance]
- Customer-level revenue figures are confidential; aggregate-level figures are internal. [categories: governance, finance] [sensitivity: confidential]

## Entities

- Sarah Chen — Director of Customer Analytics; primary owner of the segmentation model. [categories: relationships, project]
- Acme Corp — pilot enterprise customer for the new tiering structure. [categories: customer, vendor]
- CSAT-2026 dataset — the canonical customer satisfaction dataset for this analysis. [categories: data]

## Terminology

- "Tier 1 enterprise" = ARR > $1M, dedicated CSM. [categories: definitions]
- "Long-tail SMB" = customers below the SMB segment median ARR. [categories: definitions]

## External references

- Q2 segmentation working doc: [link or filename]. [categories: documentation]
- March customer ID schema: [link]. [categories: technical, documentation]

## Open items

- Validate the four-segment model against historical churn data; analysis pending. [tier: summary] [categories: analysis]
- Schedule review with Sarah Chen for next Tuesday. [tier: summary] [categories: scheduling]

## State snapshot

- Customer ID migration is 78% complete as of this session. [tier: summary] [categories: project, status]
- Three of four segment definitions have been validated; tier-2 mid-market still pending. [tier: summary] [categories: status]
```

## What the example demonstrates

- **All seven sections present**, in the prescribed order, populated with realistic records.
- **Section tier defaults applied.** Decisions, Constraints, Entities, Terminology, and External references inherit `full` (no `[tier: ...]` bracket). Open items and State snapshot inherit `summary` and explicitly state it (consistent with section default — the explicit declaration is acceptable but optional).
- **Per-record sensitivity override** on the second Constraints record: file-level default is `internal`, but the record raises to `confidential` inline.
- **Multi-category tagging** throughout: most records carry two categories.
- **Cross-skill awareness** via the empty `related_session_recap: null` field, indicating session-recap was not run on this conversation.
- **Related files reference** to a prior project-context file from the same project, building a chain.
- **Empty governance lists** (`governance_frameworks: []`, `custom_governance: {}`) demonstrate that the skill produces valid output without populating optional fields.
