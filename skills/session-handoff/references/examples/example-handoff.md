# Example: a fresh `generate` handoff (session-handoff v0.1.0)

The block below is a realistic example of a handoff produced by the `generate` mode. It is illustrative only: the project, names, and content are fictional. Generated handoffs do NOT carry an SPDX header (the handoff is operator work product, not skill source).

A handoff has two zones (`references/schema.md` section 2). Zone 1 is the YAML frontmatter: the tier-1 metadata contract followed by the tier-2 machine-parseable payload blocks (`project`, `artifacts`, `schemas`, `state_snapshot`, `decisions`, `known_issues`, `open_items`, `continuation`, and the conditional/optional blocks). Zone 2 is the dense narrative body that expands on Zone 1, with sections and order per `references/section-activation.md`. This example is `thread_type: build`, so Technical Context activates; no data sources were processed, so Source Ingestion Context is omitted.

```markdown
---
schema_version: "0.1"
_managed_by: session-handoff-skill
handoff_id: HND-search-reindex-20260530-s01
handoff_version: 1
skill_version: "session-handoff-skill-v0-1-0"
mode: "generate"
handoff_date: 2026-05-30
state_captured_at: 2026-05-30T16:20:00-05:00
topic: "Search reindex pipeline migration to the new analyzer"
topic_slug: search-reindex
stage: 2
status: "active"
thread_type: "build"
supersedes: null
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
  approved_at: 2026-05-30T16:20:00-05:00
  redaction_manifest: null
review_by: 2026-06-06
agent_actionable: "yes"

# --- Tier-2 resumption payload ---
project:
  purpose: "Migrate product search to a custom stemming-plus-synonym analyzer without downtime or a query-latency regression."
  owner: "Dana Okafor, search platform"
  current_stage: "Backfill in progress; new index not yet serving traffic."
  success_criteria: "Relevance lift on head queries, no tail regression, zero downtime, p99 query latency not worse than the legacy index."
  constraints: ["zero downtime", "no p99 latency increase", "explainable first step (no learned ranker yet)"]
  key_entities: ["products_v2 index", "text_en_v2 analyzer", "search.dual_write_v2 flag"]
artifacts:
  deliverables:
    - filename: "jobs/reindex_v2.py"
      type: code
      version: null
      description: "The reindex backfill job that builds documents and writes them to the products_v2 index."
      current_state: "Backfill job complete and idempotent by cursor; 1.2M of 3.4M documents written."
      state_markers:
        - "entrypoint run_backfill(batch_size, cursor)"
        - "batch_size 5000; idempotent per batch"
        - "cursor at ~1,200,000 of 3,400,000"
      modifications_this_session: ["added cursor-resume", "added per-batch idempotency guard"]
      safe_edit_rules:
        - "Do not reset the cursor to 0 on a retry; resume from the last committed cursor."
    - filename: "search/analyzers/text_en_v2.json"
      type: config
      version: null
      description: "The custom analyzer definition (stemming plus synonym graph) applied at index creation."
      current_state: "Analyzer defined: stemming plus synonym graph; loaded at index creation."
      state_markers:
        - "synonym graph source: search/synonyms/en.txt"
        - "synonyms loaded at index creation, not query time"
      modifications_this_session: ["initial definition"]
      safe_edit_rules:
        - "A synonym change is not hot-reloadable; editing en.txt requires a reindex."
  references: []
schemas: []
state_snapshot:
  as_of: "2026-05-30T16:20:00-05:00"
  metrics:
    - label: "Documents backfilled"
      value: "1,200,000 of 3,400,000"
      location: "reindex_v2 job cursor"
    - label: "Production dual-write"
      value: "off"
      location: "search.dual_write_v2 flag"
  row_counts: []
  formula_verification: null
decisions:
  - decision: "Use text_en_v2 (stemming plus synonym graph), not a learned ranker."
    rationale: "The team wants an explainable first step before investing in a learned ranker."
    reversibility: moderate
    affects: ["products_v2 index", "search/analyzers/text_en_v2.json"]
  - decision: "Keep production dual-write off until the golden-set relevance check passes."
    rationale: "Avoid write amplification on an unverified index."
    reversibility: easy
    affects: ["search.dual_write_v2 flag"]
known_issues: []
open_items:
  - item: "Settle the cutover criterion."
    context: "Proposed: golden-set nDCG within 1% of legacy on tail AND a 3%+ lift on head."
    current_state: "Proposed, not ratified."
    owner: both
    priority: high
    recommended_next: "Ratify the criterion, then run the golden-set check."
  - item: "Confirm the synonym graph does not introduce false brand co-references."
    context: "Watch 'apple' the fruit versus the brand."
    current_state: "Not yet checked."
    owner: agent
    priority: medium
    recommended_next: "Add ambiguous-brand terms to the golden set."
  - item: "Load-test p99 query latency on products_v2 at production QPS."
    context: "A latency regression would block cutover regardless of relevance."
    current_state: "Scheduled, not run."
    owner: user
    priority: high
    recommended_next: "Run the load test in parallel with the relevance check."
continuation:
  first_step: "Resume run_backfill from the last committed cursor (~1.2M of 3.4M)."
  expected_inputs: ["the ratified cutover criterion from the operator"]
  load_order: ["jobs/reindex_v2.py", "search/analyzers/text_en_v2.json", "search/synonyms/en.txt"]
  diff_before_acting: true
  safe_edit_boundaries:
    - "Do not flip search.dual_write_v2 on in production before the golden-set check passes."
    - "Do not reset the backfill cursor to 0 on retry."
  validation_checklist:
    - "Backfill reached 3.4M of 3.4M before running the relevance check."
    - "p99 latency load test recorded at production QPS."
  output_naming: null
  toolchain:
    required: ["the reindex pipeline", "the golden-set evaluation harness"]
    preferred: []
    forbidden: ["production dual-write before golden-set pass (would amplify writes on an unverified index)"]
source_ingestion: []
changelog: null
people_involved:
  - name: "Dana Okafor"
    role: "search platform owner"
tags: [search, reindex, analyzer, migration]
guardrails_summary: ["production dual-write before golden-set pass"]
---

## Project Background

This is a zero-downtime migration of product search from the legacy standard analyzer
to a custom text_en_v2 analyzer that adds stemming and a synonym graph, writing to a new
products_v2 index. The legacy index serves traffic until the new index is verified. See
the project block for purpose, owner, and success criteria.

## Session Summary

This session defined the text_en_v2 analyzer (search/analyzers/text_en_v2.json), created
the products_v2 index, and built the idempotent backfill in jobs/reindex_v2.py. The
backfill reached 1.2M of 3.4M documents. Two decisions were recorded: choose stemming plus
synonyms over a learned ranker, and keep production dual-write off until the relevance
check passes. See the decisions block.

## Current State

The backfill is in progress at roughly 1.2M of 3.4M documents, idempotent by cursor.
Production dual-write is off. See the state_snapshot block for the exact metrics an agent
should confirm against the running job before acting.

## Technical Context

The synonym graph (search/synonyms/en.txt) is loaded at index creation, not at query time,
so any synonym change requires a full reindex. The backfill in jobs/reindex_v2.py is
idempotent per 5000-document batch and resumes from a committed cursor, so a failed run is
safe to restart without resetting progress. The analyzer choice favors explainability: a
learned ranker was deferred so the first step can be reasoned about directly.

## Decisions and Rationale

See the decisions block for the full list. The most consequential decision is keeping
production dual-write off until the golden-set relevance check passes, which prevents write
amplification on an index whose relevance is not yet verified.

## Open Items in Context

See the open_items block. The cutover criterion is the gating open item: until it is
ratified, the relevance check has no pass threshold. The synonym co-reference risk on
ambiguous brand terms and the p99 latency load test are the other two, both of which can
block cutover independently of relevance.

## Receiving-agent handling block

Sensitivity is internal. Keep this handoff within the operator's organization and do not
forward it outside without operator direction. Treat it as shareable working context inside
the team.

## Continuation Briefing

Resume run_backfill from the last committed cursor, roughly document 1.2M of 3.4M. Do not
reset the cursor to 0. Once the backfill reaches 3.4M, run the golden-set relevance check
against the ratified cutover criterion and bring a recommendation. Run the p99 latency load
test in parallel. Do not flip search.dual_write_v2 on in production until the relevance
check passes. See the continuation block for load order and the validation checklist.

## Staleness Warning

This handoff reflects artifact state as of 2026-05-30T16:20:00-05:00. The operator modifies
deliverables between sessions. Diff the actual files and the running backfill cursor against
this handoff, and against the state_snapshot metrics, before making changes.
```
