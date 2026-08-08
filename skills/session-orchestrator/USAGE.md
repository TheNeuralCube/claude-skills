<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Usage

How to run `session-orchestrator`. See `SKILL.md` for the router and `references/rules.md` for the rules every mode enforces.

> **Portability notice.** This skill is Hub-resident and references a `handoff-settings-block` format owner and a spoke project record that are not published in this repository. See README.md.

## Before you start

Two things must be true before the skill does anything durable.

1. **The session knows which layer it is.** If you have not said, the skill asks. A session that guesses wrong either writes code it should have handed off or refuses work it was supposed to do.
2. **The durable project record is named.** Both modes write decisions, wave rationales, and lessons somewhere permanent. The skill asks which file that is and names it back to you. If there is none, it proposes one rather than writing durable decisions into the conversation — the exact failure rule 3 describes.

## Quarterback: decide, sequence, package, verify

Say "quarterback this", "run a wave", or "plan the next wave".

1. The skill reads `references/rules.md`, announces that this session is the quarterback, and announces the prohibition that comes with it: no code, no branches, no git.
2. It works the issue set, applies `references/wave-selection.md` to decide what can run concurrently, and records the selection with its rationale.
3. For each selected issue it writes a **package** per `references/artifacts.md`: the issue, acceptance criteria, the verification bar, constraints and who can lift each one, the files the issue may touch, the reporting contract, and where the work lands.
4. As reports come back it verifies each **against the source**, not against the report's own confidence, then records the outcome.
5. It writes a merge **recommendation** with its evidence. You authorize.

A quarterback asked to "just fix this one thing" declines and packages it instead, naming why. That refusal is the skill working.

## Orchestrator: turn one package into a build

Say "orchestrate this issue", "set up the build sessions", or "drive this build".

1. The skill reads the rules, announces the orchestrator layer and its prohibition: no code, no branches.
2. It turns the package into a builder handoff, delegating the handoff *shape* to `handoff-settings-block` and never inventing a competing format.
3. It drives the build and verifies the result **against the tree**, from the consumer's vantage point.
4. It reports back per the report-back template: outcome, facts with evidence, and an explicit statement of verification strength.

## Concurrency: what can run at once

Say "which of these can run concurrently", "what can run in parallel", or "batch these issues". Either mode can answer, using `references/wave-selection.md`.

The procedure gives you a collision analysis rather than a yes or no, and it names its own blind spot. Read the cost asymmetry it documents: a false collision is cheap (work serializes that could have run in parallel), and a missed collision is expensive (two builders write the same file).

## The gates you cannot talk past

These are non-negotiable and apply in every mode.

- **No merge is authorized by the session that built or audited the work.**
- **No claim of "deployed", "protected", "live", or "fixed" without a read-back from the running system** in the representation that would expose the failure. Merged is not deployed. A response code is not a write outcome.
- **No contract, decision, or constraint shipped through a channel the reader cannot open.**
- **Every unverified item lands in the PR body**, not only in a chat report.

Where a session verified something weaker than what was asked (a merge instead of a deploy, a status code instead of a read-back), it must say so **in those words**. Reporting a verification you did not perform is the failure the whole model exists to prevent.

## Adding an auditor

Use one when the work ships or runs against real data.

- The auditor runs on a **different model** from the builder. That independence is the role.
- It produces findings only, each with a severity and an overall verdict.
- It never applies fixes, never touches git, and never authorizes a merge.

## The anti-pattern

**Writing an org chart.** If what a session produces describes the layers without enforcing the rules, it has restated the diagram and dropped the method. The mode files carry their own anti-pattern lists; this is the one that is not mode-specific.
