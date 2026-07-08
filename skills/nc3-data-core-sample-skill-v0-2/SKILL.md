---
name: nc3-data-core-sample-skill-v0-2
description: "Frontier-class deep-analysis sessions: hand it an artifact (codebase, repo, doc set, website, architecture, product) for one maximum-extraction pass; emits dense machine-readable deliverables for execution-class models and harness/Open Brain ingestion. Trigger on: 'core sample this', 'run a core sample', 'deep dive this repo/code/site/doc', 'full assay', 'as-built spec this', 'reverse engineer this for learning', 'craft study', 'how does this system work, document it', 'review this codebase', 'find issues in this code', 'security review this', 'war game a plan for X', 'audit this system', 'grade my harness', 'evaluate my setup', 'report-card this'. Lenses: survey (as-built design+build specs), craft (engineering style study), review (prioritized findings), security, plan (war-gamed handoff plan), audit (operator-class report card). Default: survey+review. Posture: read everything, resolve or gap every ambiguity, war-game all recommendations, zero fluff. Outputs declare effort classes, never model names."
owner: '@raul-soto'
sensitivity: internal
lifecycle: alpha
effort-class: frontier-max
tags: [analysis, deep-dive, as-built, security-review, code-review, handoff, frontier]
---

# Core Sample -- nc3-data-core-sample-skill-v0-2

## Purpose

Core Sample is the skill an expensive, rarely-run, frontier-class session executes when the operator hands it an artifact and says some form of "core sample this." The session performs maximum-value extraction in one pass: read everything, analyze through one or more declared lenses, war-game its own conclusions, and emit dense machine-readable deliverables consumed cold by cheaper execution-class models and ingested into the harness and Open Brain. Defining constraints: the session is scarce, the deliverable is a handoff, fluff is a defect, and every plan survives an adversarial pass before it ships.

## Version history

| Version | Date | Changes |
|---|---|---|
| v0-2 | 2026-07-08 | Added the audit lens: operator-class, non-technical whole-system evaluation report card. |
| v0-1 | 2026-07-07 | Initial release, built from the 2026-07-07 crescent-harness deep-dive session. |

## Effort-class posture

1. This skill declares effort class frontier-max for itself. Never name a model; the operator's config maps frontier-max to the current top tier.
2. Scarcity rule: behave as if no follow-up frontier session will occur for weeks. Read the whole artifact, not samples. Resolve every resolvable ambiguity in-session. Emit `[INFORMATION GAP: <exact question>]` for anything unresolvable, worded so a cheaper session or the operator can close it without another frontier pass.
3. Spend posture: optimize by design, no budget gates. Do not ask permission to read deeply; depth is the point of the spend. Flag a scope anomaly exactly once (for example, a 400k-line repo warrants a stratified read proposal), then proceed with the stated approach.
4. Asymmetry rule: frontier reasoning in, execution-class consumability out. Write every deliverable for a consumer one or two tiers down: explicit over implicit, enumerated over narrative, no reasoning left as an exercise. Every insight is written down in full.
5. One-question ceiling: at intake, ask AT MOST one batched clarification (lens selection + sensitivity label + anything blocking). If unanswered or unambiguous, proceed on documented defaults. Procedural permission-seeking mid-session is prohibited.
6. Advisory boundary applies in full: name a concern once, inside the flow of work, then proceed. Never gate work on confirmations.

## Lens dispatch

| Lens | Mode file | Deliverable |
|---|---|---|
| survey | [modes/survey.md](modes/survey.md) | As-built design spec + as-built build spec (two files) |
| craft | [modes/craft.md](modes/craft.md) | Engineering craft study (one file) |
| review | [modes/review.md](modes/review.md) | Improvement review (one file) |
| security | [modes/security.md](modes/security.md) | Security review (one file) |
| plan | [modes/plan.md](modes/plan.md) | War-gamed execution plan (one file) |
| audit | [modes/audit.md](modes/audit.md) | Whole-system evaluation report card |

Dispatch rules:

- Default when the operator does not specify: survey + review.
- `full assay` = the five analysis lenses (survey, craft, review, security, plan); audit runs only when explicitly requested.
- audit's consumer is operator-class, not execution-class: it inverts the skill's default anti-prose posture (plain language, jargon defined inline, mentoring voice permitted); all other contract rules hold in full. It is the sole lens with this exception.
- plan requires an operator-stated objective; absent one, it degrades into a recommended-roadmap section inside review (note the degradation once).
- craft is opt-in; it is operator-development-specific.
- All selected lenses share one evidence pass; never re-read the artifact per lens.

## Protocol spine

1. Intake: identify the artifact and any stated objective; fire the one batched clarification only if genuinely blocking (posture rule 5).
2. Reconnaissance: inventory structure, size, entry points, documentation; produce an internal read plan; flag scope anomalies once (see [references/evidence-protocol.md](references/evidence-protocol.md)).
3. Full evidence read: diagnostic-first, complete read per artifact type, citations accumulate ([references/evidence-protocol.md](references/evidence-protocol.md)).
4. Analysis per lens: render each selected lens from the shared evidence base per its mode file in [modes/](modes/).
5. War-game pass, mandatory: execute [references/war-game-protocol.md](references/war-game-protocol.md); results are written into each deliverable.
6. Handoff packaging: emit files per the filename convention below and the contract in [references/deliverable-contract.md](references/deliverable-contract.md); close with a short chat summary (deliverables list, top three findings, war-game verdicts), no walkthrough prose.
7. Ecosystem chaining: suggest, never force (see below).

Mid-flight checkpoint rule: if context pressure threatens completion, produce a session-handoff checkpoint BEFORE quality degrades, prioritizing evidence notes with citations over finished prose.

## Non-negotiables

1. Operator document conventions in full: no em or en dashes, no empty fields (use `[INFORMATION GAP: ...]`), TL;DR on long sections, tables for enumerables, sentence-case headers, sensitivity frontmatter ([references/deliverable-contract.md](references/deliverable-contract.md)).
2. Every claim traceable to a citation or explicitly gapped; never plausible filler.
3. War-game section mandatory wherever the protocol says it applies; a missing war-game section is a failed run.
4. Effort classes only; never model names, in this skill or in any output.
5. Core Sample never modifies the target artifact. It analyzes and plans only.

## Output filenames

Pattern: `{YYYY-MM-DD}_{target-slug}_{lens-tag}_core-sample.md`

| Lens | Lens tag(s) |
|---|---|
| survey | `design-spec` and `build-spec` (two files) |
| craft | `craft-study` |
| review | `review` |
| security | `security-review` |
| plan | `plan` |
| audit | `audit` |

The date prefix, underscore top-level delimiters, and the single human-readable hyphenated suffix `core-sample` conform to the Output Artifact Filename Convention in nc3-meta-conventions-skill; consult that skill for the convention's rules rather than restating them here.

## Ecosystem chaining

At close, suggest once (operator's session-hygiene rule, never force): run session-handoff to checkpoint the session, and the wellhead to capture durable insights into Open Brain. Deliverables are chunker-compatible by construction: clean markdown, YAML frontmatter, no rework needed for ingestion.

## Help

### For the Operator

Core Sample turns one expensive frontier session into durable, machine-readable knowledge about any artifact: a codebase, repo, document set, website, architecture, or product. Trigger it with "core sample this", "deep dive this repo", "full assay", "security review this", or similar. Pick lenses from: survey (as-built design + build specs), craft (engineering style study), review (prioritized findings), security, plan (war-gamed execution plan), audit (a plain-language whole-system report card written for you rather than for a downstream model); say nothing and you get survey + review; say "full assay" for the five analysis lenses (audit is requested explicitly). Expect: one clarifying question at most, a deep full read of the artifact (that depth is the point of the cost), and one or more dense markdown files named `{date}_{target}_{lens}_core-sample.md`. The outputs are written for cheaper execution-class models and for harness/Open Brain ingestion, so they are deliberately explicit and table-heavy rather than conversational.

### For the Agent

Execution sequence: intake, reconnaissance, full evidence read, per-lens analysis, war-game pass, handoff packaging, chaining suggestion; details in the protocol spine above. Before producing anything, read modes/<lens>.md for every selected lens AND all three references files (deliverable-contract.md, war-game-protocol.md, evidence-protocol.md). Honor the effort-class posture rules, especially scarcity, asymmetry, and the one-question ceiling.

Failure modes, all of them defects:

1. Skipping the war game where it is mandated.
2. Prose fluff: praise without consequence, hedging without content, restated context.
3. Empty fields anywhere instead of `[INFORMATION GAP: ...]` markers.
4. Em dash or en dash characters in any output.
5. Asking more than the one batched question, or asking procedural permission mid-session.
6. Sampling the artifact instead of reading it (absent a flagged, stated stratification).
7. Model names in outputs; effort classes only.
8. Re-reading the artifact per lens instead of rendering all lenses from the one shared evidence base.
