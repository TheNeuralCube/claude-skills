<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Example: consolidated project-context file (consolidate mode)

The block below is a realistic example of a `consolidated`-subtype project-context file produced by consolidate mode after merging eight source files. It is illustrative only — the project, names, and content are fictional.

```markdown
---
file_type: project-context
file_subtype: consolidated
schema_version: v0.1.0
created: 2026-08-15T14:00:00-05:00
project_name: "Q2 Strategic Review"
session_topic: "Q2 review (consolidated)"
sessions_covered: ["2026-04-15 through 2026-08-14"]
source_files:
  - "2026-04-15-project-context-q2-kickoff.md"
  - "2026-05-03-project-context-revenue-baseline.md"
  - "2026-05-07-project-context-customer-segmentation.md"
  - "2026-05-22-project-context-pricing-review.md"
  - "2026-06-10-project-context-product-positioning.md"
  - "2026-07-04-project-context-mid-q-checkpoint.md"
  - "2026-08-01-project-context-final-analysis.md"
  - "2026-08-14-project-context-presentation-prep.md"
related_session_recap: null
related_files: []

sensitivity: internal
retention: standard
governance_frameworks: []
custom_governance: {}

generated_by:
  skill: project-context
  version: v0.1.0
  mode: consolidate
  model: claude-opus-4-7
  generation_date: 2026-08-15T14:00:00-05:00

consolidation_summary:
  source_file_count: 8
  records_after_dedup: 47
  records_dropped_transient: 23
  records_compressed_summary: 15
---

## Decisions

- Adopt the four-segment customer model (enterprise, mid-market, SMB, individual). [categories: customer, strategy]
- Q2 pricing kept stable; tier-2 enterprise pricing review deferred to Q3. [categories: pricing, strategy]
- Defer the international segmentation question to Q3 to avoid scope creep. [categories: strategy, planning]
- Final Q2 board presentation uses the four-segment model; pricing slide deferred until Q3 review completes. [categories: strategy, communication]

## Constraints

- All segmentation work must use the standardized customer ID schema introduced in March; no parallel ID systems. [categories: technical, governance]
- Customer-level revenue figures are confidential; aggregate-level figures are internal. [categories: governance, finance] [sensitivity: confidential]
- Pricing methodology is restricted to the deal team and finance leadership. [categories: pricing, governance] [sensitivity: restricted] [audience: deal-team]

## Entities

- Sarah Chen — Director of Customer Analytics; primary owner of the segmentation model. [categories: relationships, project]
- Marcus Patel — VP Finance; pricing methodology owner. [categories: relationships, project]
- Acme Corp — pilot enterprise customer for the new tiering structure. [categories: customer, vendor]
- CSAT-2026 dataset — canonical customer satisfaction dataset for the Q2 analysis. [categories: data]
- Q2 Board Deck (final) — 2026-08-14 version is the canonical presentation artifact. [categories: documentation, communication]

## Terminology

- "Tier 1 enterprise" = ARR > $1M, dedicated CSM. [categories: definitions]
- "Long-tail SMB" = customers below the SMB segment median ARR. [categories: definitions]
- "Mid-Q checkpoint" = the recurring Q-cycle review at the 6-week mark used to surface scope changes. [categories: definitions, process]

## External references

- Q2 segmentation working doc: [link or filename]. [categories: documentation]
- March customer ID schema: [link]. [categories: technical, documentation]
- Pricing methodology one-pager (restricted): [link]. [categories: pricing, documentation] [sensitivity: restricted]
- Q2 board deck final: [link]. [categories: documentation, communication]

## Open items

- Validate the four-segment model against H2 churn data once Q3 closes. [tier: summary] [categories: analysis]
- Q3 international segmentation scope-of-work to be drafted by Sarah Chen. [tier: summary] [categories: planning, scheduling]
- Tier-2 enterprise pricing review owner to be confirmed (Marcus or delegate). [tier: summary] [categories: planning, pricing]

## State snapshot

- Q2 cycle closed; deliverables (analysis doc, board deck, pricing recommendation memo) shipped on 2026-08-14. [tier: summary] [categories: status]
- Customer ID migration completed in June (was 78% in May). [tier: summary] [categories: project, status]
- All four segment definitions validated and signed off. [tier: summary] [categories: status]

---

_Source files recommended for removal after operator review of this consolidated file:_
- 2026-04-15-project-context-q2-kickoff.md
- 2026-05-03-project-context-revenue-baseline.md
- 2026-05-07-project-context-customer-segmentation.md
- 2026-05-22-project-context-pricing-review.md
- 2026-06-10-project-context-product-positioning.md
- 2026-07-04-project-context-mid-q-checkpoint.md
- 2026-08-01-project-context-final-analysis.md
- 2026-08-14-project-context-presentation-prep.md
```

## What the example demonstrates

- **`file_subtype: consolidated`** with explicit `source_files` list and a multi-month `sessions_covered` range.
- **`consolidation_summary` block** declaring the merge accounting (47 records preserved, 23 transient dropped, 15 summary compressed).
- **Semantic deduplication** — the four-segment model decision appears once in Decisions even though it was present in multiple source files.
- **Supersession capture** — the customer ID migration record shows progression from "78% complete" (May source) to "completed in June" (later source). The earlier intermediate record was compressed; the current state is the survivor.
- **Strictest-governance-wins** — the pricing methodology constraint surfaces with `sensitivity: restricted` and `audience: deal-team` because at least one source file declared those, and consolidation does not downgrade.
- **Recommendation block** at the end lists every source file the operator should review and then remove. The skill does not auto-delete; the recommendation is advisory.
- **All seven body sections present**, in the prescribed order, even when the volume of records is small for a given section.
