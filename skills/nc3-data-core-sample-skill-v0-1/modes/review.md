# Review lens: improvement review

## Deliverable

`{date}_{slug}_review_core-sample.md`, frontmatter and conventions per [../references/deliverable-contract.md](../references/deliverable-contract.md), lens `review`.

## Consumer

Execution-class, cold. The reader opens finding #1 and starts working.

## Required sections

1. TL;DR: a one-line health verdict plus the top three findings.
2. Scope and method statement (what was reviewed, how, what was excluded).
3. Findings table first (ID, title, severity, category, one-line impact), THEN per-finding detail.
4. Positive patterns worth preserving, so an execution session does not "fix" strengths.
5. Recommended sequencing of fixes.
6. War game section.

## Finding schema

Every field populated or explicitly gapped; no empty fields.

| Field | Content |
|---|---|
| ID | Stable short ID (R-01, R-02, ...) |
| Title | One line |
| Severity | critical / high / medium / low, with a one-line severity rationale |
| Category | correctness, reliability, performance, maintainability, gap-vs-intent, debt |
| Evidence | file:line or document section citation |
| Impact | What goes wrong, for whom, under what conditions |
| Fix sketch | Concrete enough for an execution session to start immediately |
| Effort estimate | Effort-class terms only, e.g. "one execution-class session", "frontier design pass required first" |
| Confidence | verified in evidence / inferred / assumed |

## Evidence emphasis

Full read per [../references/evidence-protocol.md](../references/evidence-protocol.md). A finding without a citation does not ship. Weight correctness and reliability evidence (tests, error paths, edge handling) above style observations.

## War-game applicability

Full protocol per [../references/war-game-protocol.md](../references/war-game-protocol.md): red-team the top 5 findings, pre-mortem the fix sequencing, assumptions ledger, consumer simulation, fluff purge. Results written into the deliverable.

## Quality bar

Zero findings without evidence citations. Severity distribution justified (if everything is critical, nothing is). An execution session could open finding #1 and begin within minutes.
