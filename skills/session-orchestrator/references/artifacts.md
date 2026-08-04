# The two artifacts: package and report-back

The method moves on exactly two documents. Everything else is conversation.

A **package** is what the quarterback hands an orchestrator. A **report-back** is what returns. Both
ship as **files the other party can open** (rule 3) — a path in the project record, an outbox file,
a PR body. Never a memory store, never a message in a thread that ends.

Adapt the headings; keep every field. A field you have nothing to put in is answered "none" or
"unknown", never deleted — a missing field reads as "not applicable" when it usually means "not
thought about".

---

## Package template

```markdown
# Package — <issue id and one-line title>

## Issue
<link or id, and the full body reference the orchestrator can open>

## Acceptance criteria
1. <criterion>
2. <criterion>

**Completes after the merge?** <yes/no — list which criteria>
  (If yes: the PR carries NO closing keyword. Rule 6.)

## Verification bar
- **Strength required:** merged | deployed | live-exercised   (rule 1 — pick one, explicitly)
- **Read-back representation:** <the view that would expose the failure>   (rule 2)
- **The check that must be run:** <exact observation, not "confirm it works">

## Constraints
| Constraint | Who may lift it |
|---|---|
| <e.g. do not touch the schema> | operator / quarterback / nobody |

(Rule 9. "Nobody" is valid and often correct. An unowned constraint gets lifted by whoever is most
inconvenienced by it.)

## Files this issue may touch
<full paths — the set the wave selection was decided on. Rule 5.>
**If the build turns out to need a path not listed here, STOP and report the collision.**

## Reporting contract
Return exactly these facts:
- <SHA / PR URL / test count / the specific observation>
- Anything unverified, named as unverified
- Deviations, and whether each was filed as an issue

## Where this lands
- Project record: <path>
- Outbox / package file: <path>
```

---

## Report-back template

```markdown
# Report — <issue id>

## Outcome
<one line: what now exists>

## Facts, with evidence
| Claim | Evidence | How it was checked |
|---|---|---|
| Tests pass | <count> on <SHA> | ran the suite on the branch head |
| PR open | <URL>, base <branch> | opened the PR and read the base |
| <the substantive claim> | <observation> | <the exact command or view> |

## Verification strength
- **Merge-verified / deploy-verified / live-exercised:** <which one>   (rule 1)
- If the bar was "deployed" and only the merge was checked, **say so here in those words.**

## Not verified
- <item> — <why not>
- (Each of these also appears in the PR body. Rule 9. The chat report dies with the session.)

## Deviations
| Deviation | Does a later block depend on it? | Filed as |
|---|---|---|
| <what changed> | yes/no | issue <id> or n/a   (rule 7) |

## Collisions or scope pressure
<paths outside the package's set, adjacent problems found, anything the wave selection missed>
```

---

## Why these are templates and not prose

The constraints in this method are only real if they survive the trip between sessions. A package
written freehand reliably loses the two fields that are hardest to think about — the verification
*strength* and the constraint *authority* — because nothing in a blank page asks for them.

The template asks.
