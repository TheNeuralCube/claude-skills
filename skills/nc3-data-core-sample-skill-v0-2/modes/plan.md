# Plan lens: war-gamed execution plan

## Precondition

An operator-stated objective is required. Absent one, do NOT emit a standalone plan: fold a recommended-roadmap section into the review deliverable and note the degradation once. Do not interview the operator to extract an objective beyond the one-question ceiling.

## Deliverable

`{date}_{slug}_plan_core-sample.md`, frontmatter and conventions per [../references/deliverable-contract.md](../references/deliverable-contract.md), lens `plan`.

## Consumer

Execution-class, cold. The reader starts module 1 within minutes of opening the file.

## Required sections

1. Objective restated in one sentence, with success criteria that are measurable and binary where possible.
2. Constraints and assumptions ledger, up front (assumption, tier, re-check owner; schema in [../references/war-game-protocol.md](../references/war-game-protocol.md) step 3).
3. Module/phase map table: id, name, depends-on, gate-to-pass. Mirrors the operator's SDD-to-build-spec lifecycle: design intent flows down, each module gate is binary.
4. Per-module specification, detailed enough that an execution session generates its own short build spec from it: interfaces, file-level targets, test/verify commands, rollback or abandon criteria.
5. Explicit effort-class assignment per module: which modules need a frontier design pass first vs which are execution-class buildable as specified.
6. Sequencing rationale (why this order; what unblocks what).
7. Full war game section, including the pre-mortem.
8. Handoff note: the exact first action for the execution session, verbatim.

## Evidence emphasis

The plan is grounded in the shared evidence base per [../references/evidence-protocol.md](../references/evidence-protocol.md): every file-level target cites a real path, every interface claim cites the artifact. A plan step that references an unverified surface carries an INFORMATION GAP marker instead of a guess.

## War-game applicability

Full protocol per [../references/war-game-protocol.md](../references/war-game-protocol.md): red-team the top plan decisions, pre-mortem (three most probable failure causes, each mitigated or accepted), assumptions ledger, consumer simulation, fluff purge. Results written into the deliverable.

## Quality bar

An execution session reading only this file plus the artifact starts module 1 within minutes and knows exactly when to stop and escalate (every module has a gate and an abandon criterion). No module requires frontier reasoning that has not already been done and written down here.
