<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Roadmap

Deferred items and future direction for `session-orchestrator`. Nothing here is committed; the list records intent and the conditions under which each item would be taken up.

## Open structural question

| Item | Disposition |
|---|---|
| **Relocation to a private Hub-skills repository** | **Decided, not yet executed (operator decision, 2026-08-06).** This skill is Hub-resident: it delegates handoff shape to `handoff-settings-block` and writes its durable record to a spoke's `context/active.md`, neither of which is published here. A public consumer therefore installs a skill that points at owners it cannot open. The resolution is a dedicated private repository for Hub-resident skills, to be created as separate work; this skill moves there and is withdrawn from public distribution at that point. Until then it stays published with the portability notice carried in README.md and USAGE.md. |

## Deferred from v0.1.0

| Item | Disposition |
|---|---|
| **De-Hubbing into a portable public variant** | Rejected for now, superseded by the relocation decision above. Making the skill portable would mean either inlining the handoff format (duplicating `handoff-settings-block` and guaranteeing the two drift apart, which is the exact failure the one-skill-two-modes decision avoided) or dropping the format delegation entirely. Both cost more than moving the skill to where its dependencies live. |
| **A project appendix of real incidents** | Rejected at authoring time and still rejected. Every rule is stated repo-agnostically and anchored by the failure that produced it. An appendix would tie the skill to one project's history and invite readers to treat the rules as that project's quirks. |
| **Splitting quarterback and orchestrator into two skills** | Rejected at authoring time. One skill with two modes exists specifically so the shared rules cannot drift apart. Revisit only if the mode files grow far enough apart that the shared rules are no longer genuinely shared. |
| **A rule for post-deployment monitoring** | Candidate. Rules 1 and 2 cover the gap between merged and deployed, but nothing yet covers what to watch after a deploy lands. Would need a real failure to anchor it, per the skill's own authoring standard. (Rule 10 took the tenth slot with unrelated content; this item was never about that rule.) |
| **Machine-checkable acceptance criteria in the package template** | Candidate. Acceptance criteria are prose today, so the verification bar depends on the reading session's judgment. A structured form would make rule 6 mechanically enforceable rather than a discipline. |

## Conditions for v1.0.0

v0.1.x stays at 0.x because the model has been proven on one operator, one repository family, and one four-day run.

1. The model runs successfully on a repository and issue set outside the one it was distilled from.
2. At least one wave runs with an independent auditor in the loop, and the second-model independence demonstrably catches something the builder missed.
3. No rule in `references/rules.md` is found to be project-specific once exercised elsewhere.
4. The relocation decision above is executed, so the skill's stated dependencies are actually resolvable by everyone who can install it.

## Known limitations

- **Hub coupling.** Stated plainly above and in README.md. This is the skill's largest defect as a published artifact, and it is a distribution problem rather than a design problem.
- **Single-operator provenance.** Ten rules from one operator's practice: rules 1 to 9 from a four-day quarterback run, rule 10 and 10b from a later autosync-retirement wave. They are real and each was paid for, but they are not yet known to generalize beyond that operator.
- **The rules are enforced by a reading agent, not by tooling.** Nothing mechanically prevents a session from claiming a verification it did not perform. The gates are prose contracts, which is why rule 8 exists.
