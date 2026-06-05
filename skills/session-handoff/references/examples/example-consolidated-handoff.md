# Example: a `consolidate` handoff (session-handoff v0.1.0)

The block below is a consolidation of three prior handoffs into one new artifact. It is illustrative only and fictional. Generated handoffs do NOT carry an SPDX header.

It demonstrates the consolidation identity rules: a **fresh `handoff_id`** (never inherited from a source), `generation_mode: consolidated`, `supersedes: null`, a `prior_handoffs` ledger of the immediate sources, and `consolidation_depth: 1`. It demonstrates **most-restrictive governance propagation**: one source is confidential and one carries the SOX framework, so the consolidation is confidential and carries SOX. The ledger uses the enterprise enriched-object shape (`{ id, kind, sensitivity }`); the public default would be plain id strings. One source reconciled a competitor-pricing CSV, so the **Source Ingestion Context** section activates by the data-processing content signal even though `thread_type` is `strategic`.

```markdown
---
schema_version: "0.1"
_managed_by: session-handoff-skill
handoff_id: HND-pricing-model-20260602-s01
handoff_version: 1
skill_version: "session-handoff-skill-v0-1-0"
mode: "consolidate"
handoff_date: 2026-06-02
state_captured_at: 2026-06-02T15:40:00-05:00
topic: "Tier-2 pricing model: consolidated working state"
topic_slug: pricing-model
stage: 4
status: "active"
thread_type: "strategic"
supersedes: null
prior_handoffs:
  - id: "HND-pricing-20260520-s01#v1"
    kind: source
    sensitivity: confidential
  - id: "HND-pricing-20260524-s01#v1"
    kind: source
    sensitivity: internal
  - id: "HND-pricing-20260528-s02#v1"
    kind: source
    sensitivity: internal
consolidation_depth: 1
derivative_of: null
governance:
  sensitivity: "confidential"
  retention: "review_by 2026-09-01"
  governance_frameworks: ["SOX"]
  custom_governance: null
generated_by:
  model: claude-opus-4-8
  provider: anthropic
  surface: claude-code
  generation_mode: consolidated
  model_source: system-reported
audit:
  approved_by: "Dana Okafor"
  approval_mode: self-asserted
  approved_at: 2026-06-02T15:40:00-05:00
  redaction_manifest: null
review_by: 2026-06-16
agent_actionable: "yes"

# --- Tier-2 resumption payload ---
project:
  purpose: "Define a tier-2 pricing model with a SOX-compliant approval path for list-price changes."
  owner: "Dana Okafor, revenue"
  current_stage: "Structure drafted; one finance review complete; SOX control mapping not yet signed off."
  success_criteria: "Approved tier-2 structure, finance sign-off, SOX control mapping confirmed."
  constraints: ["SOX change-control for list-price changes", "no cannibalization of existing enterprise deals"]
  key_entities: ["tier-2 bands: standard, plus, enterprise-lite", "SOX change-control process", "regional discount authority"]
artifacts:
  deliverables:
    - filename: "pricing/tier2_model_v4.xlsx"
      type: spreadsheet
      version: "v4"
      description: "The consolidated tier-2 pricing model workbook merged from the three source drafts."
      current_state: "Three-band structure drafted; one finance review pass complete."
      state_markers:
        - "3 bands: standard, plus, enterprise-lite"
        - "regional discount authority capped at 15%"
      modifications_this_session: ["merged the three source drafts into one model"]
      safe_edit_rules:
        - "List-price cells route through SOX change-control; do not edit them outside that process."
  references:
    - filename: "competitor_prices_2026Q2.csv"
      type: csv
      description: "Q2 competitor list prices, reconciled to map competitor tiers onto our three bands."
      ingestion_status: completed
      items_extracted: 84
      items_excluded: ["12 rows for discontinued SKUs"]
      judgment_calls: ["mapped 9 competitor tiers onto our 3 bands"]
schemas: []
state_snapshot:
  as_of: "2026-06-02T15:40:00-05:00"
  metrics:
    - label: "Tier-2 bands defined"
      value: "3"
      location: "pricing/tier2_model_v4.xlsx"
    - label: "Regional discount authority cap"
      value: "15%"
      location: "pricing/tier2_model_v4.xlsx"
  row_counts: []
  formula_verification: null
decisions:
  - decision: "Three-band tier-2 structure (standard, plus, enterprise-lite)."
    rationale: "Clearer upsell paths than a two-band structure."
    reversibility: difficult
    affects: ["pricing/tier2_model_v4.xlsx"]
  - decision: "List-price changes route through the existing SOX change-control process."
    rationale: "List-price changes are SOX-relevant; this is why the consolidation carries the SOX framework."
    reversibility: irreversible
    affects: ["approval path", "governance_frameworks"]
  - decision: "Regional leads may approve discounts up to 15%; above that escalates."
    rationale: "Settled across the sources; detail in the 2026-05-24 source."
    reversibility: moderate
    affects: ["discount authority"]
known_issues: []
open_items:
  - item: "Finance sign-off on the SOX control mapping for list-price changes."
    context: "Mapping identified but not signed off."
    current_state: "Pending finance review."
    owner: user
    priority: high
    recommended_next: "Route the mapping to finance for sign-off."
  - item: "Confirm enterprise-lite does not cannibalize existing enterprise deals."
    context: "Risk that enterprise-lite pulls down existing enterprise accounts."
    current_state: "Not yet modeled."
    owner: agent
    priority: medium
    recommended_next: "Model overlap against the current enterprise book."
continuation:
  first_step: "Drive the finance sign-off on the SOX control mapping for list-price changes."
  expected_inputs: ["finance review outcome"]
  load_order: ["pricing/tier2_model_v4.xlsx", "competitor_prices_2026Q2.csv"]
  diff_before_acting: true
  safe_edit_boundaries:
    - "Do not edit list-price cells outside the SOX change-control process."
  validation_checklist:
    - "SOX control mapping signed off by finance before any list-price change."
  output_naming: "pricing/tier2_model_v5.xlsx for the next revision"
  toolchain:
    required: ["the pricing model workbook"]
    preferred: []
    forbidden: ["any list-price change path that bypasses SOX change-control"]
source_ingestion:
  - source: "competitor_prices_2026Q2.csv"
    what_was_found: "Q2 competitor list prices across 9 tiers, 84 usable rows."
    matched: ["our standard and plus bands align with 6 competitor tiers"]
    new: ["enterprise-lite has no direct competitor analog"]
    excluded: ["12 rows for discontinued SKUs"]
    judgment_calls: ["mapped 9 competitor tiers onto our 3 bands"]
    ambiguities_remaining: ["two competitor tiers could map to either plus or enterprise-lite"]
changelog:
  from_version: null
  to_version: "HND-pricing-model-20260602-s01#v1"
  structural_changes: ["merged three source drafts into pricing/tier2_model_v4.xlsx"]
  data_changes: ["consolidated decisions and open items across three sources"]
  formula_changes: []
  manual_edits_preserved: []
people_involved:
  - name: "Dana Okafor"
    role: "revenue owner"
  - name: "Pat Lindqvist"
    role: "finance reviewer"
tags: [pricing, tier-2, sox, consolidation]
guardrails_summary: ["any list-price change path that bypasses SOX change-control"]
---

## Project Background

Three working sessions on the tier-2 pricing model are consolidated into one resumable
state. The work covers the pricing structure, the approval path, and the SOX-relevant
controls around list-price changes. See the project block.

## Session Summary

This consolidation merged three source handoffs into pricing/tier2_model_v4.xlsx, reconciled
a competitor-pricing CSV, and carried forward the three live decisions and two open items.
Governance was derived most-restrictively from the sources. See the prior_handoffs ledger
and the changelog block.

## Current State

The three-band structure is drafted and has had one finance review. The SOX control mapping
for list-price changes is identified but not signed off. See the state_snapshot block.

## Source Ingestion Context

competitor_prices_2026Q2.csv was reconciled this consolidation. It contained Q2 competitor
list prices across nine tiers, of which 84 rows were usable and 12 were excluded as
discontinued SKUs. Six competitor tiers aligned with our standard and plus bands. The
enterprise-lite band has no direct competitor analog, which is a positioning signal worth
watching. Two competitor tiers were ambiguous and could map to either plus or enterprise-lite;
that ambiguity is unresolved. See the source_ingestion and artifacts.references blocks.

## Strategic Context

The three-band structure was chosen over two bands for clearer upsell paths. The SOX
change-control routing for list-price changes is a hard constraint and the reason this
consolidation carries the SOX framework. Regional discount authority is capped at 15% with
escalation above that.

## Decisions and Rationale

See the decisions block. The list-price SOX routing is irreversible by design and the most
load-bearing decision; the three-band structure is difficult to reverse once published.

## Open Items in Context

See the open_items block. Finance sign-off on the SOX control mapping is the gating item.
The enterprise-lite cannibalization risk is the second, and is not yet modeled.

## Receiving-agent handling block

Sensitivity is confidential. Limited audience; do not redistribute; confirm the recipient is
authorized before acting on or forwarding. SOX framework applies.

## Continuation Briefing

Drive the finance sign-off on the SOX control mapping for list-price changes, then model the
enterprise-lite overlap against the current enterprise book. Treat this handoff as
confidential and SOX-scoped. Do not edit list-price cells outside the SOX change-control
process. See the continuation block.

## Staleness Warning

This handoff reflects artifact state as of 2026-06-02T15:40:00-05:00. The three source
handoffs are retained; their full detail is reachable via the prior_handoffs ledger. Diff the
actual workbook against this handoff before making changes.
```

## What consolidation did

- **New identity:** `HND-pricing-model-20260602-s01`, not inherited from any source.
- **Ledger:** the three immediate sources, with `kind` and `sensitivity` per source (enterprise enriched-object shape).
- **Most-restrictive governance:** `sensitivity` is `confidential` (the maximum of the three sources), `retention` is the strictest source value, and `governance_frameworks` is the union (`["SOX"]`). Sensitivity was never downgraded.
- **Depth:** `consolidation_depth: 1` (one greater than the maximum source depth of 0).
- **Source retention:** the three sources are retained by default. Deleting the confidential or SOX-bearing source would require `confirm delete protected sources`; the flattened lineage is captured into the post-flight audit record at consolidation time, so provenance survives even if a light source is later deleted.
- **Source Ingestion Context:** activated by the data-processing content signal (a competitor CSV was reconciled), not by `thread_type`, which is `strategic` here.
