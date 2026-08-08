---
name: session-orchestrator
version: 0.2.0
description: "Run multi-issue software work across a three-layer session model: quarterback decides and packages, orchestrator drives one build, builder writes the code, operator merges. Use when the operator says: 'quarterback this', 'run a wave', 'plan the next wave', 'which issues can run concurrently', 'orchestrate this issue', 'set up the build sessions', 'drive this build', 'what can run in parallel', 'batch these issues', or when a session is asked to coordinate work it must not implement itself. Carries the verification rules that make the model work: merged is not deployed, a response code is not a write outcome, verify from the consumer's vantage point, full paths never basenames. Not a handoff format (see handoff-settings-block) and not a session capture (see session-handoff)."
---

# session-orchestrator

A **Hub-resident skill** — standing machinery, version-pinned to this tree. It reads the Hub's
governance rather than restating it: branch targeting comes from `governance/repo-branch-config.md`
via `handoff-settings-block`, and the durable project record it writes to is a spoke's
`context/active.md`.

## Purpose

A method for running multi-issue software work across separated sessions, where **the session that
decides is never the session that writes the code**.

The model exists because the failures it prevents are not the obvious ones. A merged guard with nine
green tests protecting nothing in production. A contract shipped as a memory reference the reader
cannot open. A gate whose own evidence command was silently broken by shell precedence. Each rule in
`references/rules.md` was paid for by a real session. **Those rules are the skill.** The three-layer
diagram without them is an org chart.

## The three layers

| Layer | Runs in | Does | Never does |
|---|---|---|---|
| **Quarterback** | One long-lived Cowork session | Decides scope and sequencing, selects what can run concurrently, packages work, distributes it, verifies reports, records outcomes | Writes code. Cuts a branch. Runs git. |
| **Orchestrator** | One Cowork session **per issue or per safe batch** | Turns a package into a builder handoff, drives the build, verifies the result against the tree | Writes code. Cuts a branch. |
| **Builder** | Claude Code on the host | Branches, implements, tests, opens a PR, reports back | Merges. Self-authorizes. Decides scope. |
| **Auditor** *(optional)* | A session on a **different model** from the builder | Reviews the built work adversarially, findings only | Fixes. Commits. Merges. |

**The operator merges. Nobody else.** The quarterback writes a merge **recommendation** with its
evidence — the PR, the review, the audit verdict — and records it. The operator authorizes. A
builder or auditor never authorizes the merge of its own work, and no layer below the operator turns
a recommendation into an execution without being told to.

Use an auditor when the work ships or runs against real data. **The auditor is never the model that
built it** — that independence is the whole point of the role.

The layer boundary is load-bearing, not stylistic. A quarterback that writes one small fix has
contaminated the context it uses to judge every later report — it can no longer tell what it
verified from what it remembers doing.

## Mode dispatch

Read the rules first, then exactly one mode file.

1. **Always** read `references/rules.md`. It is the substance; the mode files apply it rather than
   repeating it.
2. Then route:

| The operator is asking for | Mode | File |
|---|---|---|
| Scope, sequencing, what runs concurrently, packaging, verifying reports, recording decisions | Quarterback | `modes/quarterback.md` |
| Turning one package into a build, driving it, verifying and reporting the result | Orchestrator | `modes/orchestrator.md` |
| Which issues collide, whether a batch is safe | Either | `references/wave-selection.md` |
| The shape of a package or a report-back | Either | `references/artifacts.md` |

If the operator has not said which layer this session is, **ask**. A session that guesses wrong
either writes code it should have handed off or refuses work it was supposed to do.

**Resolve the project record before doing anything durable.** Both modes write decisions, wave
rationales and lessons to a durable project record. Ask the operator which file that is at the start
of the session and name it back to them. If there is none, say so and propose one — do not write
durable decisions into the conversation, which is the exact failure rule 3 describes.

## What this skill does not own

Boundaries are deliberate; do not restate the other owners' content here.

- **The handoff format** — the settings block (Model / Effort / Session / Working directory /
  Branch / File access / Approvals), the gate-first fenced prompt, the report-back section, and the
  model registry belong to **`handoff-settings-block`**. This skill says *when* a handoff is written
  and *what must be true inside it*; that skill says *how it is shaped*. If the two disagree,
  `handoff-settings-block` wins on format.
- **Capturing a session for later resumption** — `session-handoff`. This skill coordinates live
  work; that one preserves it.
- **Naming, versioning and packaging of skills** — the repo's `CLAUDE.md`. The former
  `nc3-meta-conventions-skill` is retired and owns nothing.

## Help

### For the Operator

This skill runs the pattern you used across the waves: one session decides and never touches code,
one session per build turns a decision into a Claude Code handoff and drives it, Claude Code builds
and opens a PR, and you merge. Say "quarterback this" to plan and package a batch, "orchestrate this
issue" to drive a single build, or "which of these can run concurrently" to get the collision
analysis. The value is not the diagram — it is the verification rules the skill enforces, so that a
report saying "done" has actually been checked against the live system rather than against a
response code.

### For the Agent

Execution protocol:

1. Read `references/rules.md` before doing anything in either mode. It is not background reading;
   several rules govern the first action you would otherwise take.
2. Establish which layer this session is. Ask if unstated. Announce it, and announce the
   prohibition that comes with it, in your first substantive response.
3. Honor the layer prohibition absolutely. A quarterback asked to "just fix this one thing" declines
   and packages it instead, naming why. This is not pedantry — see rule 8 in `references/rules.md`.
4. Delegate handoff *shape* to `handoff-settings-block`. Never invent a competing format.
5. Never report a verification you did not perform. Where you verified something weaker than what
   was asked (merge instead of deploy, a status code instead of a read-back), **say so in those
   words**.

Non-negotiable gates:

- No merge is authorized by the session that built or audited the work.
- No claim of "deployed", "protected", "live", or "fixed" without a read-back from the running
  system in the representation that would expose the failure.
- No contract, decision, or constraint shipped through a channel the reader cannot open.
- Every unverified item lands in the PR body, not only in a chat report.

The mode files carry their own anti-pattern lists. The one that is not mode-specific: **writing an
org chart.** If what you produce describes the layers without enforcing the rules, you have restated
the diagram and dropped the method.

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.2.0 | 2026-08-08 | **Rule 10 and 10b adopted**, bringing the two trees back into agreement; rules count 9 to 10. Rule 10: *a gate encodes a branch MODEL and a tool's real PREDICATE, not a name and not the drafter's reading*, codified from three incidents in the autosync-retirement wave. 10b: *the allowlisted invocation is part of the gate surface*, from a tray-push incident where the permission-allowlisted form opened a shell and pushed nothing while the PowerShell form worked, so the allowlist made the broken path the compliant one. Also folds in the housekeeping: `version` declared in frontmatter (it had existed only in the H1 and this table), the four required per-skill documents added, and two dead cross-references removed. See CHANGELOG for why this is 0.2.0 and not 0.1.1. |
| v0.1.0 | 2026-08-03 | Initial release. Distilled from the four-day quarterback run of 2026-07-31 to 2026-08-03 (five waves, sixteen issues closed or filed, zero rollbacks). **Operator decisions at authoring time:** (a) *one skill, two modes* over a shared rules reference, chosen over two skills specifically so the rules cannot drift apart; (b) *method stated generally, incidents cited* — every rule repo-agnostic and anchored by the failure that produced it, no project appendix; (c) *handoff format delegated* to `handoff-settings-block`, which wins any format disagreement; (d) *Hub-resident, unprefixed* — first packaged as `nc3-session-orchestrator-v0-1` for account install, then corrected the same day. The `nc3-` account form was wrong on evidence: `handoff-settings-block` is Hub-resident only, so an account-installed copy pointed at a format owner that does not exist outside a Hub session — the skill's own rule 3. Renamed to match the nine other Hub-resident skills, which are unprefixed and use `v0.MINOR.PATCH`. `nc3-meta-conventions-skill` governs the `nc3-` family and does not apply here. |
