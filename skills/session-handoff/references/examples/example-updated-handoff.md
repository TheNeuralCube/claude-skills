# Example: an `update` handoff (session-handoff v0.1.0)

The block below is the `update` of the fresh handoff in `example-handoff.md`. It is illustrative only and fictional. Generated handoffs do NOT carry an SPDX header.

Identity rules: the `handoff_id` is preserved, `handoff_version` increments to 2, `supersedes` points to `HND-search-reindex-20260530-s01#v1`. Curation across both zones (`modes/update.md` section 5): live items carry at full fidelity in the structured blocks; the cutover-criterion question that was an `open_items` entry in v1 is now a settled `decisions` entry, and the resolution is recorded in the `changelog` block, which `update` always populates because it always supersedes. The retained v1 holds the dropped detail.

```markdown
---
schema_version: "0.1"
_managed_by: session-handoff-skill
handoff_id: HND-search-reindex-20260530-s01
handoff_version: 2
skill_version: "session-handoff-skill-v0-1-0"
mode: "update"
handoff_date: 2026-06-02
state_captured_at: 2026-06-02T11:05:00-05:00
topic: "Search reindex pipeline migration to the new analyzer"
topic_slug: search-reindex
stage: 3
status: "active"
thread_type: "build"
supersedes: "HND-search-reindex-20260530-s01#v1"
prior_handoffs: []
consolidation_depth: 0
derivative_of: null
governance:
  sensitivity: "internal"
  retention: null
  governance_frameworks: []
  custom_governance: null
generated_by:
  model: claude-opus-4-8
  provider: anthropic
  surface: claude-code
  generation_mode: live
  model_source: system-reported
audit:
  approved_by: "Dana Okafor"
  approval_mode: self-asserted
  approved_at: 2026-06-02T11:05:00-05:00
  redaction_manifest: null
review_by: 2026-06-09
agent_actionable: "yes"

# --- Tier-2 resumption payload ---
project:
  purpose: "Migrate product search to a custom stemming-plus-synonym analyzer without downtime or a query-latency regression."
  owner: "Dana Okafor, search platform"
  current_stage: "Backfill complete; first relevance check run; not yet serving traffic."
  success_criteria: "Relevance lift on head queries, no tail regression, zero downtime, p99 not worse than legacy."
  constraints: ["zero downtime", "no p99 latency increase", "explainable first step"]
  key_entities: ["products_v2 index", "text_en_v2 analyzer", "search.dual_write_v2 flag", "golden_set_v3"]
artifacts:
  deliverables:
    - filename: "jobs/reindex_v2.py"
      type: code
      version: null
      description: "The reindex backfill job that builds documents and writes them to the products_v2 index."
      current_state: "Backfill complete: 3.4M of 3.4M documents written."
      state_markers:
        - "entrypoint run_backfill(batch_size, cursor)"
        - "cursor at 3,400,000 of 3,400,000 (complete)"
      modifications_this_session: ["backfill run to completion"]
      safe_edit_rules:
        - "Do not reset the cursor; the backfill is complete."
    - filename: "search/eval/golden_set_v3.jsonl"
      type: config
      version: "v3"
      description: "The relevance golden set: labeled head and tail queries used to gate cutover."
      current_state: "240 head queries, 600 tail queries; one evaluation run recorded."
      state_markers:
        - "240 head queries, 600 tail queries"
        - "run 1: head lift 4.1%, tail regression 1.8%"
      modifications_this_session: ["created", "first evaluation run"]
      safe_edit_rules:
        - "Do not edit golden queries to make a run pass; that invalidates the criterion."
  references: []
schemas: []
state_snapshot:
  as_of: "2026-06-02T11:05:00-05:00"
  metrics:
    - label: "Documents backfilled"
      value: "3,400,000 of 3,400,000 (complete)"
      location: "reindex_v2 job cursor"
    - label: "Golden-set head lift (run 1)"
      value: "+4.1%"
      location: "golden_set_v3 run 1"
    - label: "Golden-set tail regression (run 1)"
      value: "-1.8%"
      location: "golden_set_v3 run 1"
    - label: "Production dual-write"
      value: "off"
      location: "search.dual_write_v2 flag"
  row_counts: []
  formula_verification: null
decisions:
  - decision: "Cutover criterion: golden-set nDCG within 1% of legacy on tail AND a 3%+ lift on head."
    rationale: "Settled this session; replaces the v1 open item. See v1 for the options weighed."
    reversibility: moderate
    affects: ["cutover gate", "golden_set_v3"]
  - decision: "Keep production dual-write off until the golden-set check passes at the settled criterion."
    rationale: "Run 1 (head +4.1%, tail -1.8%) is just outside the criterion; not yet safe to dual-write."
    reversibility: easy
    affects: ["search.dual_write_v2 flag"]
  - decision: "Use text_en_v2 over a learned ranker for an explainable first step."
    rationale: "Carried from v1; still live."
    reversibility: moderate
    affects: ["products_v2 index"]
known_issues:
  - issue: "Tail-query regression of 1.8% on golden-set run 1, just outside the cutover criterion."
    severity: important
    location: "golden_set_v3 tail queries"
    discovered: "golden-set run 1, this session"
    recommended_action: "Investigate synonym over-expansion on ambiguous brand terms; re-run."
open_items:
  - item: "Investigate the 1.8% tail regression."
    context: "Leading hypothesis: synonym over-expansion on ambiguous brand terms like 'apple'."
    current_state: "Hypothesis only; not yet confirmed."
    owner: agent
    priority: high
    recommended_next: "Narrow the synonym graph or add a tail-query allowlist, then re-run golden set."
  - item: "Run the p99 latency load test on products_v2 at production QPS."
    context: "A latency regression blocks cutover regardless of relevance."
    current_state: "Scheduled, not run."
    owner: user
    priority: high
    recommended_next: "Run in parallel with the regression investigation."
continuation:
  first_step: "Investigate the 1.8% tail regression; test the synonym-over-expansion hypothesis on ambiguous brand terms."
  expected_inputs: ["operator decision: narrow the synonym graph vs a tail-query allowlist"]
  load_order: ["search/eval/golden_set_v3.jsonl", "search/synonyms/en.txt", "search/analyzers/text_en_v2.json"]
  diff_before_acting: true
  safe_edit_boundaries:
    - "Do not flip search.dual_write_v2 on in production before the criterion passes."
    - "Do not edit golden queries to force a pass."
  validation_checklist:
    - "Golden-set re-run meets the settled criterion (tail within 1%, head 3%+)."
    - "p99 latency load test recorded at production QPS."
  output_naming: null
  toolchain:
    required: ["the golden-set evaluation harness", "the reindex pipeline"]
    preferred: []
    forbidden: ["production dual-write before the criterion passes", "editing golden queries to force a pass"]
source_ingestion: []
changelog:
  from_version: "HND-search-reindex-20260530-s01#v1"
  to_version: "HND-search-reindex-20260530-s01#v2"
  structural_changes: ["added golden_set_v3 deliverable"]
  data_changes: ["backfill completed 1.2M to 3.4M", "recorded golden-set run 1 metrics"]
  formula_changes: []
  manual_edits_preserved: []
  resolved_since_prior:
    - "Cutover criterion ratified (was open item opn in v1; now a decision). Detail and options in v1."
people_involved:
  - name: "Dana Okafor"
    role: "search platform owner"
tags: [search, reindex, analyzer, migration, relevance]
guardrails_summary: ["production dual-write before criterion passes", "editing golden queries to force a pass"]
---

## Project Background

Zero-downtime migration of product search from the legacy standard analyzer to a custom
text_en_v2 analyzer (stemming plus synonym graph), writing to products_v2. The legacy index
serves traffic until the new index is verified. See the project block.

## Session Summary

This session completed the backfill (3.4M of 3.4M), created search/eval/golden_set_v3.jsonl,
and ran the first golden-set evaluation: head lift 4.1%, tail regression 1.8%. The cutover
criterion was ratified (it was an open item in v1) and is now recorded in the decisions block.
See the changelog block for the version delta.

## Current State

The backfill is complete. Golden-set run 1 shows a 4.1% head lift and a 1.8% tail
regression, just outside the ratified criterion. Production dual-write is off. See the
state_snapshot block for the exact metrics.

## Technical Context

The synonym graph loads at index creation, so any change requires a reindex. The tail
regression on run 1 is the open technical question: the leading hypothesis is synonym
over-expansion on ambiguous brand terms (for example 'apple' the brand versus the fruit).
The choice is between narrowing the synonym graph and adding a tail-query allowlist.

## Decisions and Rationale

See the decisions block. The cutover criterion is now settled (tail within 1% of legacy,
head 3%+ lift); v1 holds the options that were weighed. Production dual-write stays off
because run 1 is just outside that criterion.

## Open Items in Context

See the open_items block. The tail regression is the gating item; until it is resolved and
the golden set re-run passes the criterion, cutover cannot proceed. The p99 load test
remains outstanding and can block cutover independently.

## Guardrails and Watchpoints

Do not flip production dual-write before the criterion passes. Do not edit the golden
queries to force a passing run; that invalidates the criterion. Treat synonym expansions on
ambiguous brand terms as suspect until the tail regression is explained.

## Receiving-agent handling block

Sensitivity is internal. Keep within the organization; do not forward outside without
operator direction.

## Continuation Briefing

Investigate the 1.8% tail regression. Test the synonym-over-expansion hypothesis on
ambiguous brand terms, then decide between narrowing the synonym graph and a tail-query
allowlist, and re-run the golden set against the settled criterion. Run the p99 load test in
parallel. Do not flip production dual-write until the criterion passes. See the continuation
block for load order and the validation checklist.

## Staleness Warning

This handoff reflects artifact state as of 2026-06-02T11:05:00-05:00. The operator modifies
deliverables between sessions. Diff the actual files and the golden-set run output against
this handoff, and against the state_snapshot metrics, before making changes. Detail for the
ratified cutover-criterion decision lives in HND-search-reindex-20260530-s01#v1.
```

## What the update curated

- **Carried at full fidelity (live):** the active `open_items` (tail regression, p99 load test), the live `decisions`, the current `state_snapshot` metrics, the `artifacts` with their `state_markers`, and the `continuation` playbook.
- **Compressed (resolved since v1):** the cutover-criterion question, an `open_items` entry in v1, is now a settled `decisions` entry, and its resolution is recorded in `changelog.resolved_since_prior` pointing to v1 for the options weighed.
- **Retained:** v1 is not deleted; it is the durable archive reachable via the `supersedes` pointer.
