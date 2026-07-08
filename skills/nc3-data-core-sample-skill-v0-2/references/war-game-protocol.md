# War-game protocol

The mandatory adversarial quality gate. Every deliverable containing recommendations, plans, or findings passes this gate before shipping. The gate is executed by the same session, self-adversarially. Results are WRITTEN INTO the deliverable as a final section titled "War game", never discarded. A deliverable missing its war-game section where required is a failed run.

Applicability: review, security, and plan lenses run the full protocol. Survey runs it against its recommendations section only. Craft runs it against its collaboration predictions.

## Executable checklist

Run the steps in order. Each step produces written output in the War game section.

### 1. Red-team the top findings

For each of the top N findings or recommendations (N = 5 default, fewer if the deliverable has fewer):

- Steelman the strongest argument that the finding is wrong, overstated, or not worth doing.
- If the steelman wins, demote or delete the finding and say so.
- Record the surviving verdict in one line each, in a table: finding ID, steelman summary, verdict (survives / demoted / deleted).

### 2. Pre-mortem

Applies to plan and review lenses; for security, frame it as "if this system is breached in 12 months, the three most likely vectors are". Assume the plan or fix sequence was executed and failed:

- Enumerate the three most probable causes of failure.
- For each: add a mitigation, or an explicit accepted-risk line. No third option.

### 3. Assumptions ledger

Every deliverable carries this table so a downstream consumer knows what to re-check:

| Assumption | Tier | Re-check owner |
|---|---|---|
| <assumption stated plainly> | verified in evidence / inferred / assumed | <operator, execution session, or named source> |

Tier definitions: "verified in evidence" means a citation exists in the document; "inferred" means derived from evidence but not directly stated; "assumed" means taken on faith and flagged for re-check.

### 4. Consumer simulation

Re-read the deliverable AS the execution-class consumer, cold, with only the document and the artifact:

- Is any step ambiguous? Any reference unresolvable? Any reasoning missing or left as an exercise?
- Fix defects in place in the body, then note in the War game section that the pass ran and what it changed (or "no changes" if clean).

### 5. Fluff purge

Final deletion pass. Remove anything that does not inform a decision or an action. The three named defect types:

1. Praise without consequence.
2. Hedging without content.
3. Restated context.

Dense over polite is the standing rule. Note in the War game section that the purge ran.
