# Audit lens: whole-system evaluation report card

## Deliverable

`{date}_{slug}_audit_core-sample.md`, frontmatter and conventions per [../references/deliverable-contract.md](../references/deliverable-contract.md), lens `audit`.

## Consumer

Operator-class, NOT execution-class. This is the one lens whose reader is the human operator, not a cheaper downstream model. The audit lens therefore INVERTS the skill's default anti-prose posture: plain language is required, jargon must be defined inline, and a mentoring voice is a feature rather than a defect. Set `consumer: operator-class` in the frontmatter (the documented exception to the deliverable contract). All other contract rules still apply: no empty fields, tables for enumerables, sentence-case headers, effort classes not model names, full traceability.

## When to use

Operator hands the skill a whole system, harness, or personal tooling estate and asks for a report card: "audit this system", "grade my harness", "evaluate my setup", "how good is what I built", "should I be embarrassed to show this to real engineers". Distinct from `review` (execution-class prioritized findings for a coding session) and `security` (threat surface only): audit is a holistic, human-facing verdict that a non-engineer operator can act on and can hand to engineer peers.

## Language rules (mandatory for this lens only)

1. Default to plain, non-technical English. Assume a smart reader with no formal software-engineering education.
2. The first time any technical term appears, define it inline in parentheses in one short sentence.
3. Maintain a GLOSSARY section at the end listing every technical term used, each with a one-sentence plain definition.
4. Use everyday analogies (filing cabinets, checklists, assembly lines) where they aid understanding.
5. Separate two judgments explicitly and never conflate them: is the underlying thinking sound, and is the execution polished. A weak polish list does not imply weak thinking.

## Classification system

Every finding carries a level on the scale named for its section, plus a one-line reason. Define each scale's three levels in plain terms the first time it is used.

| Section | Three-level scale |
|---|---|
| Vision strengths | Standout / Solid / Marginal |
| Vision weaknesses | Critical / Notable / Minor |
| Vulnerabilities (security and non-security) | Critical / Moderate / Low |
| Inefficiencies (by drag created) | High-drag / Medium-drag / Low-drag |
| Feature relevance | Essential / Useful / Questionable |
| Feature disposition | Keep-as-is / Improve / Deprecate |
| Deprecations | Deprecate-now / Deprecate-soon / Watchlist |

Issues-list items are classified on TWO axes at once:

| Axis | Levels |
|---|---|
| Complexity | Simple (minutes to an hour of AI-assisted work) / Moderate (a focused session) / Complex (multi-session or needs an engineer) |
| Priority | High / Medium / Low |

## Required sections

1. TL;DR: a one-line overall health verdict, the letter grade for the vision, and the single most important next move.
2. How to read this report: five sentences setting expectations and reassuring honestly (a long improvement list signals ambition, not failure).
3. Executive summary, how it works today: plain-language walkthrough of what the system does and a typical day of using it.
4. Vision grade: an A to F letter grade with a one-paragraph justification, then strengths and weaknesses per the scales. State directly whether the core idea is sound or flawed.
5. The over-engineering check: for the whole system and each major feature, judge whether it is the right amount of machinery for the actual number of users, or heavier than the value it returns. Be fair in both directions.
6. Vulnerabilities: security and non-security risks (data loss, corruption, single points of failure, key-person risk), each with a plain "what could go wrong" and a suggested guardrail.
7. Inefficiencies: each with a concrete lighter alternative.
8. Feature-by-feature grade: a table of every meaningful feature (description, relevance, disposition, one-line reason).
9. Recommended issues list: a single ranked table ready to paste into an issue tracker (columns: title, description, complexity, priority, expected payoff), sorted by priority then complexity so quick wins are obvious.
10. Deprecation report: everything redundant, abandoned, or superseded, with its level and reason.
11. Executive summary, how it should work tomorrow: the 3 to 5 highest-leverage moves over the next few months, in order, and what the system would feel like to use once done.
12. What I would add that you did not ask for: maintainability, documentation quality, whether a second person could pick this up, comparison to how professional teams solve the same problem.
13. For your peers, technical appendix: a concise engineer-facing version of the top findings in proper technical vocabulary (terms need not be defined here). Purpose: give the operator a document that shows the system rests on sound reasoning and that its gaps are already known.
14. Health-instrumentation results (conditional): if the target system ships its own health or test tooling, run it and report what it actually returned this pass, plus any drift from the system's committed self-reports. If it ships none, state that as an INFORMATION GAP and note the absence as a finding.
15. War game section.
16. Glossary.

## Finding schema

Every field populated or explicitly gapped; no empty fields.

| Field | Content |
|---|---|
| ID | Stable short ID per section (V-01 vision, U-01 vulnerability, E-01 inefficiency, F-01 feature, I-01 issue, D-01 deprecation) |
| Title | One line, plain language |
| Level | The section's scale level, with a one-line rationale |
| Evidence | file:line or document-section citation |
| Plain impact | What goes wrong or right, for whom, under what conditions, in everyday terms |
| Recommendation | Concrete next step; for issues, the two-axis complexity and priority |
| Confidence | verified in evidence / inferred / assumed |

## Evidence emphasis

Full read per [../references/evidence-protocol.md](../references/evidence-protocol.md). A finding without a citation does not ship. If the target ships health, lint, or test tooling, executing it is part of the evidence pass, not an optional extra; fold the live results into the findings and flag any gap between the system's self-reported health and its actual health.

## War-game applicability

Full protocol per [../references/war-game-protocol.md](../references/war-game-protocol.md): red-team the vision grade and the top 5 issues, pre-mortem the tomorrow-state roadmap, assumptions ledger, operator simulation (can a non-engineer actually act on this report), fluff purge. Results written into the deliverable.

## Quality bar

Zero findings without evidence citations. The letter grade is defended, not asserted. Severity and relevance distributions are justified (if every feature is Essential, the scale was not used). Every technical term is in the glossary. The non-technical operator can read the whole report unaided, and can hand the technical appendix to a senior engineer without edits. The closing paragraph gives the operator a straight, evidence-based read on whether showing this work to expert peers is something to fear.
