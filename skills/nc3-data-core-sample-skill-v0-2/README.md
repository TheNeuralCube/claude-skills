<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# nc3-data-core-sample-skill-v0-2

A frontier-class deep-analysis skill. Hand it one artifact (a codebase, repo, document set, website, architecture, or product) and it performs a single maximum-extraction pass, then emits dense, machine-readable deliverables written to be consumed cold by cheaper execution-class models and ingested into a harness or Open Brain pipeline.

The name extends the Neural Cube Black Gold family: a core sample drills a deep column through an existing formation and brings the strata up for analysis.

- **License:** Apache 2.0 (SPDX headers on repo wrapper files; skill-generated deliverables carry their own frontmatter, no SPDX).
- **Skill version:** v0-2. Pre-production. Earns v1-0 after use on 2 or 3 real targets and an eval pass.
- **Structure:** thin router. Root SKILL.md dispatches; execution logic lives per lens in `modes/`; shared contracts live once each in `references/`.
- **Effort class:** declares `frontier-max` for itself, never a model name. Outputs declare effort classes only.

## What it does

Six lenses, one shared evidence pass, dispatched from one entry point:

| Lens | Deliverable | Trigger examples |
|---|---|---|
| survey | as-built design spec + as-built build spec (two files) | "core sample this", "as-built spec this", "how does this system work, document it" |
| craft | engineering craft study (one file) | "craft study", "reverse engineer this for learning" |
| review | improvement review (one file) | "review this codebase", "find issues in this code" |
| security | security review (one file) | "security review this" |
| plan | war-gamed execution plan (one file) | "war game a plan for X" |
| audit | whole-system evaluation report card (one file) | "audit this system", "grade my harness", "evaluate my setup", "report-card this" |

Default when no lens is named: **survey + review**. `full assay` runs the five analysis lenses (survey, craft, review, security, plan); audit runs only when explicitly requested. The audit lens is the sole lens whose consumer is the human operator rather than an execution-class model: it uses plain language and defines jargon inline, while every other contract rule holds. The craft lens is opt-in (it is operator-development-specific). The plan lens requires an operator-stated objective; absent one it degrades into a recommended-roadmap section inside review and says so once.

All selected lenses render from one evidence base. The artifact is never re-read per lens.

## The three defining constraints

1. **Scarcity.** The session behaves as if no follow-up frontier session will occur for weeks: it reads the whole artifact, resolves every resolvable ambiguity in-session, and emits an explicit `[INFORMATION GAP: ...]` (with the exact question to answer) for anything it cannot resolve, so the gap is workable without another frontier pass.
2. **Asymmetry.** Frontier reasoning in, execution-class consumability out. Every deliverable is explicit over implicit, enumerated over narrative, with no reasoning left as an exercise.
3. **The war game.** No deliverable containing recommendations, plans, or findings ships without an adversarial self-critique pass whose results are written into the deliverable as a final "War game" section. A missing war-game section where required is a failed run.

## Files

```
nc3-data-core-sample-skill-v0-2/
  SKILL.md                          thin router: identity, posture, dispatch, protocol spine, help
  modes/
    survey.md                       as-built design + build spec lens
    craft.md                        engineering craft study lens
    review.md                       improvement review lens
    security.md                     security review lens
    plan.md                         war-gamed execution plan lens
    audit.md                        whole-system evaluation report card lens
  references/
    deliverable-contract.md         output frontmatter schema + document conventions (single source)
    war-game-protocol.md            the mandatory adversarial gate (single source)
    evidence-protocol.md            read discipline per artifact type (single source)
```

No `scripts/` or `assets/` as of v0-2. Mechanical helpers (frontmatter and filename generation, the dash and length checks) remain a candidate for a future version.

## Output filenames

Pattern: `{YYYY-MM-DD}_{target-slug}_{lens-tag}_core-sample.md`, with lens tags `design-spec`, `build-spec`, `craft-study`, `review`, `security-review`, `plan`, `audit`. The date prefix, underscore top-level delimiters, and the single hyphenated suffix `core-sample` conform to the Output Artifact Filename Convention owned by the Neural Cube conventions skill.

## Non-negotiables

No em or en dashes anywhere. No empty fields (INFORMATION GAP markers instead). Every claim traceable to a citation or explicitly gapped. Effort classes only, never model names. Core Sample never modifies the target artifact; it analyzes and plans only.

## Provenance

Built to the 2026-07-07 build spec, which encodes the manual workflow proved by that day's crescent-harness deep-dive session (an as-built design spec, an as-built build spec, and an engineering craft study of a colleague's codebase). This skill makes that one-off workflow repeatable on any artifact.
