<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Usage

How to run nc3-data-core-sample-skill and what to expect. This skill is meant for an expensive, rarely-run frontier-class session; the depth of the read is the point of the cost.

## Before you start

- Have the artifact ready: a repo or codebase path, a document set, a URL set for a website, or the collected artifacts for a product or architecture.
- Know whether you have an objective. The plan lens needs one (for example, "port the render pipeline to our stack"). Without an objective the plan lens degrades into a roadmap section inside the review.
- Expect at most one clarifying question at intake, batching lens selection, sensitivity label, and anything genuinely blocking. If nothing is blocking, the session proceeds on documented defaults.

## Triggering and lens selection

Say some form of "core sample this" and point at the artifact.

| You say | You get |
|---|---|
| "core sample this repo" (no lens) | survey + review: an as-built design spec, an as-built build spec, and an improvement review |
| "full assay" | the five analysis lenses: survey, craft, review, security, plan (audit is requested explicitly) |
| "craft study this" | the engineering craft study |
| "security review this" | the security review |
| "war game a plan to <objective>" | the war-gamed execution plan |
| "audit this system", "grade my harness", "report-card this" | the whole-system evaluation report card, written in plain language for you rather than for a downstream model |

You can name several lenses at once. They all render from one read of the artifact; the session never re-reads it per lens.

## What happens during the run

1. **Intake.** The session identifies the artifact and any objective, and asks its one question only if something blocks the work.
2. **Reconnaissance.** It inventories structure, size, entry points, and documentation, and builds an internal read plan. If the target is disproportionately large for a full frontier-depth read, it flags that once and proposes a stratified read, then proceeds.
3. **Full evidence read.** Diagnostic-first: it reads before concluding. For code that means every load-bearing file, all docs, config, tests, CI, and deploy. Evidence notes accumulate with citations.
4. **Per-lens analysis.** Each selected lens is rendered from the shared evidence base in the operator document format.
5. **War game.** Recommendations, findings, and plans pass an adversarial self-critique whose results are written into the deliverable as a final section.
6. **Handoff.** Files are emitted per the filename convention, and the session closes with a short summary: the deliverables list, the top three findings, and the war-game verdicts. No walkthrough prose.

## The deliverables

Files are named `{YYYY-MM-DD}_{target-slug}_{lens-tag}_core-sample.md`. Each carries YAML frontmatter (title, date, skill, target, lens, sensitivity, consumer, provenance, gap count) and is self-contained: a session with only that file and the artifact can act on it. There are no references to "our conversation." The consumer is `execution-class` for every lens except audit, whose report card is written for you and carries `consumer: operator-class`.

Two things to check on any deliverable:

- **Gaps are workable.** Every `[INFORMATION GAP: ...]` marker states the exact question to answer, so a cheaper session or you can close it without another frontier pass.
- **The war game is present** wherever it applies (review, security, plan, audit always; survey for its recommendations; craft for its predictions). Its absence there is a failed run.

## After the run

The session suggests, once and without forcing, running session-handoff to checkpoint the work and the wellhead to capture durable insights into Open Brain. The deliverables are already chunker-compatible (clean markdown, YAML frontmatter), so ingestion needs no rework.

## First recommended run

Point it at a medium repo or document set with no lens specified, and validate the survey + review default end to end. That is the highest-value general pair and the fastest way to see whether the outputs are dense and cold-readable enough for your execution-class consumers.
