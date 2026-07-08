<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Roadmap

Deferred items and future direction for nc3-data-core-sample-skill. Nothing here is committed; the list records intent and the conditions under which each item would be taken up.

## Deferred from v0-1

| Item | Disposition |
|---|---|
| Comparative multi-artifact lens | Candidate. v0-1 is single-target per session; cross-artifact comparison is a future lens, out of scope now. |
| `scripts/` for mechanical helpers | Shipped in v0-2 as `scripts/core_sample_checks.py`: dash purity, description length, gap_count agreement, and deliverable filename generation. Further helpers are added as patterns stabilize across real runs. |
| review and security merge decision | Open question. Still unresolved at v0-2 (no real security run yet); decide at the next bump. The audit lens added in v0-2 overlaps both at operator altitude, one more input to the boundary decision. [INFORMATION GAP: operator preference after first security run] |
| Automatic Open Brain capture | Out of scope. The wellhead owns capture; Core Sample only formats compatibly and suggests the chain. |
| Standing scheduler integration | Out of scope now. Harness reconciliation may invoke Core Sample later. |

## Conditions for v1-0

v0-2 stays pre-production because it is unproven on real targets. The path to v1-0:

1. Run against 2 or 3 real targets, starting with the survey + review default end to end on a medium repo or document set.
2. Incorporate operator feedback from those runs.
3. Re-pass the acceptance checklist in [references/acceptance-checks.md](references/acceptance-checks.md) (13 checks as of v0-2).

## Known limits carried into v0-1

- **Context exhaustion on very large targets.** Mitigated by the recon-stage stratified-read proposal (flagged once, then proceed) and the mid-flight session-handoff checkpoint rule in SKILL.md. Not yet exercised against a target large enough to force the checkpoint.
- **Website and product lenses are less exercised than code.** The evidence protocol covers all artifact types, but the genesis build was proved against code and document artifacts. Dynamic-content and undemonstrable-artifact handling are asserted, not yet field-tested.
