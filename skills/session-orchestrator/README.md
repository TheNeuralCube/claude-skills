<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# session-orchestrator

A method for running multi-issue software work across separated sessions, where **the session that decides is never the session that writes the code**.

- **License:** Apache 2.0 (SPDX headers on repo wrapper files).
- **Skill version:** 0.1.1, declared in the SKILL.md frontmatter.
- **Provenance:** distilled from a four-day quarterback run (2026-07-31 to 2026-08-03): five waves, sixteen issues closed or filed, zero rollbacks.

> **Portability notice.** This skill is **Hub-resident**. It reads governance that lives outside this repository — branch targeting via a `handoff-settings-block` skill and a repo-branch config, and a durable project record in a spoke's `context/active.md`. Those are not published here, so an installed copy will reference owners it cannot open. The skill is slated to move to a private Hub-skills repository; it remains published here in the interim. The verification rules in `references/rules.md` are repo-agnostic and useful on their own.

## Why it exists

The failures this model prevents are not the obvious ones:

- A merged guard with nine green tests protecting nothing in production.
- A contract shipped as a memory reference the reader cannot open.
- A gate whose own evidence command was silently broken by shell precedence.

Each rule in `references/rules.md` was paid for by a real session. **Those rules are the skill.** The three-layer diagram without them is an org chart.

## The layers

| Layer | Runs in | Does | Never does |
|---|---|---|---|
| **Quarterback** | one long-lived session | decides scope and sequencing, selects what runs concurrently, packages work, verifies reports, records outcomes | writes code, cuts a branch, runs git |
| **Orchestrator** | one session per issue or safe batch | turns a package into a builder handoff, drives the build, verifies the result against the tree | writes code, cuts a branch |
| **Builder** | a coding agent on the host | branches, implements, tests, opens a PR, reports back | merges, self-authorizes, decides scope |
| **Auditor** *(optional)* | a session on a **different model** from the builder | reviews adversarially, findings only | fixes, commits, merges |

**The operator merges. Nobody else.** The quarterback writes a merge *recommendation* with its evidence and records it. The operator authorizes.

The layer boundary is load-bearing, not stylistic. A quarterback that writes one small fix has contaminated the context it uses to judge every later report — it can no longer tell what it verified from what it remembers doing.

Use an auditor when the work ships or runs against real data. The auditor is never the model that built it; that independence is the whole point of the role.

## The nine verification rules

`references/rules.md` is read first in every mode. It is the substance; the mode files apply it rather than repeating it.

| # | Rule |
|---|---|
| 1 | Merged is not deployed |
| 2 | A response code is not evidence of a write's outcome |
| 3 | Verify from the consumer's vantage point |
| 4 | A shell snippet inside a handoff is shipped code |
| 5 | Compare full paths, never basenames |
| 6 | No closing keyword when the acceptance criterion is post-merge |
| 7 | A deviation a later block depends on is an issue, not a paragraph |
| 8 | Verify reports against the source before propagating them |
| 9 | Name who can lift each constraint, and put unverified items in the PR body |

## Files

```
session-orchestrator/
  SKILL.md                    router: layers, mode dispatch, boundaries, non-negotiable gates
  modes/
    quarterback.md            deciding, sequencing, packaging, verifying reports
    orchestrator.md           turning one package into a build and verifying the result
  references/
    rules.md                  the nine verification rules; read first, always
    wave-selection.md         which issues collide, whether a batch is safe
    artifacts.md              the package and report-back templates
```

## What this skill does not own

- **The handoff format** — the settings block, the gate-first fenced prompt, the report-back section, and the model registry belong to `handoff-settings-block`. This skill says *when* a handoff is written and *what must be true inside it*; that skill says *how it is shaped*.
- **Capturing a session for later resumption** — `session-handoff`. This skill coordinates live work; that one preserves it.
- **Naming, versioning, and packaging of skills** — this repository's `CLAUDE.md`.
