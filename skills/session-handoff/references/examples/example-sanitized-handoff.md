# Example: a `share-sanitize` derivative plus its manifest (session-handoff v0.1.0)

The blocks below are a redacted derivative copy of the confidential consolidated handoff in `example-consolidated-handoff.md`, plus the redaction manifest it emits. Both are illustrative only and fictional. Generated handoffs and manifests do NOT carry an SPDX header.

This example demonstrates the **derivative identity** rules (`handoff_id` preserved, `derivative_of` set, `generation_mode: sanitized`, `supersedes: null`) and that masking applies **across both zones** (`modes/share-sanitize.md` section 5): a person name is masked inside the Zone 1 `people_involved` structured block, not only in prose. Because the source was a consolidation, the derivative **preserves the source lineage verbatim**: `prior_handoffs` (the three sources) and `consolidation_depth: 1` carry through unchanged, and `derivative_of` is added on top (`references/lineage.md` sections 6 and 7). Source sensitivity is `confidential`, so `sensitivity_rules` forces `credentials`, `pii`, and `client_names`. Masking style is `tag`. The tier-1 metadata contract is preserved; `audit.approved_by` stays as the attestation. To keep the example readable, only the frontmatter identity, the masked blocks, and the narrative delta are shown; all other payload blocks carry verbatim from the source.

## The redacted derivative copy (excerpt)

```markdown
---
schema_version: "0.1"
_managed_by: session-handoff-skill
handoff_id: HND-pricing-model-20260602-s01
handoff_version: 1
skill_version: "session-handoff-skill-v0-1-0"
mode: "share-sanitize"
handoff_date: 2026-06-02
state_captured_at: 2026-06-02T15:40:00-05:00
topic: "Tier-2 pricing model: consolidated working state (sanitized for sharing)"
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
derivative_of: "HND-pricing-model-20260602-s01#v1"
governance:
  sensitivity: "confidential"
  retention: "review_by 2026-09-01"
  governance_frameworks: ["SOX"]
  custom_governance: null
generated_by:
  model: claude-opus-4-8
  provider: anthropic
  surface: claude-code
  generation_mode: sanitized
  model_source: system-reported
audit:
  approved_by: "Dana Okafor"
  approval_mode: self-asserted
  approved_at: 2026-06-02T15:55:00-05:00
  redaction_manifest: "HND-pricing-model-20260602-s01-v1-sanitized.manifest.md"
review_by: 2026-06-16
agent_actionable: "yes"

# --- Tier-2 resumption payload (masked; all blocks not shown carry verbatim from the source) ---
people_involved:
  - name: "Dana Okafor"
    role: "revenue owner"
  - name: "[REDACTED:pii]"
    role: "finance reviewer"
tags: [pricing, tier-2, sox, consolidation]
guardrails_summary: ["any list-price change path that bypasses SOX change-control"]
---

## Source Ingestion Context

competitor_prices_2026Q2.csv was reconciled this consolidation. It contained Q2 competitor
list prices across nine tiers, of which 84 rows were usable and 12 were excluded as
discontinued SKUs. Two competitor tiers were ambiguous and could map to either plus or
enterprise-lite; that ambiguity is unresolved.

## Receiving-agent handling block

Sensitivity is confidential. Limited audience; do not redistribute; confirm the recipient is
authorized before acting on or forwarding. SOX framework applies. This copy is a sanitized
derivative; the canonical unredacted handoff exists under the same handoff_id.

## Staleness Warning

This state is as of 2026-06-02T15:40:00-05:00. This is a redacted derivative; review it
before sharing.
```

## The redaction manifest

```yaml
---
schema_version: "0.1"
_managed_by: session-handoff-skill
manifest_type: redaction
source_handoff_id: "HND-pricing-model-20260602-s01#v1"
redacted_at: 2026-06-02T15:55:00-05:00
redaction_provider: built-in
policy_schema_version: "0.1"
---
# Reports categories and counts only. Never reproduces redacted content.
summary:
  total_redactions: 1
  by_category:
    pii: 1
    client_names: 0
    credentials: 0
    financials: 0
    internal_names: 0
  pii_flagged_not_redacted: 1
  masking_style: tag
disclaimer: >
  Redaction is assistive and model-based. It is not guaranteed to find or remove all
  sensitive content. Review the redacted output before sharing.
```

## What share-sanitize did

- **Same `handoff_id`, derivative identity:** `derivative_of` points to the source;
  `generation_mode: sanitized`; `supersedes: null`. The canonical handoff is unchanged.
- **Lineage preserved verbatim:** the source was a consolidation, so the derivative carries
  the source's `prior_handoffs` ledger and `consolidation_depth: 1` unchanged, and adds
  `derivative_of` on top. share-sanitize masks content; it does not rewrite lineage
  (`references/lineage.md` sections 6 and 7).
- **Masking across both zones:** the finance reviewer's name was masked inside the Zone 1
  `people_involved` structured block as `[REDACTED:pii]`. This is the point of the two-zone
  payload: sensitive values in structured blocks are masked, not only prose.
- **Active category set:** `sensitivity_rules[confidential]` forced `credentials`, `pii`,
  and `client_names`. This source carried no credentials and no client account names, so
  those counts are zero. One PII span (a person name) was masked.
- **PII flagging is assistive:** the owner's name (Dana Okafor) was flagged as PII but the
  operator chose to keep it as the attestation, recorded as `pii_flagged_not_redacted: 1`.
  The skill does not claim to have found all PII.
- **Manifest:** categories and counts only, never content, with the mandatory assistive
  disclaimer. `audit.redaction_manifest` on the derivative points to it.
