---
file_role: skill-mode
mode: update
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Mode: update

## Pre-flight prerequisite

This mode runs only after pre-flight (`references/preflight.md`) has completed and the operator has typed `confirm update`. update is destructive in the sense that it supersedes the prior version (it moves the "latest" pointer), so the token gate is mandatory. Do not execute this mode without pre-flight completion and the token.

update produces a new version-suffixed handoff that supersedes the prior version while preserving the same `handoff_id`. It is the operator's deliberate, higher-fidelity alternative to lossy platform auto-compaction: the operator controls fidelity, and pre-flight surfaces what will be carried, compressed, or dropped before any write.

update is one of the three unproven modes new in v0.1.0. Its identity rules, curation, and length projection are field-tested in the build session; any failure in identity, lineage, or content preservation of live items is build-blocking (build spec section 5.1).

Schema reference: `references/schema.md`. Lineage: `references/lineage.md`. Length contract: `references/defaults.md` section 4.

## 1. Locate the prior handoff

1. Use the prior handoff pre-flight found via `_managed_by: session-handoff-skill` and the operator-named or detected `handoff_id`.
2. **If the prior is stale-schema**, compose retrofit first (`modes/retrofit.md` section 6): upgrade the schema losslessly, then continue here. Post-flight reports the composition (deviation reporting).

## 2. Preserve identity, increment version, set supersession

- Preserve `handoff_id` unchanged.
- Increment `handoff_version` by one.
- Set `supersedes` to the prior `<handoff_id>#v<N>` (`references/lineage.md` section 2).
- Keep `mode: update`, `generation_mode: live`, `supersedes` non-null, `prior_handoffs: []`, `derivative_of: null`, `consolidation_depth` unchanged from the prior.

The prior version is retained as the durable archive for any detail this update curates away. update does not delete the prior file.

## 3. Current-versus-resolved curation (the lossy step, controlled)

This is the heart of update. It is a **lightweight heuristic**, not a scoring algorithm and not a merge classifier.

| Item class | Treatment |
|---|---|
| Live items: open decisions, active open items, current state, standing guardrails | Carry forward at **full fidelity**. This is a hard rule. Live items are never compressed. |
| Resolved-since-prior items: decisions now settled, open items now closed, state now superseded | Compress to **one-line ledger entries**. The full detail stays recoverable in the superseded prior version. |

The split is between "still live" and "resolved since the prior version," not between "important" and "unimportant." Dropping or compressing a live item is a defect; the build session tests the split explicitly.

For each resolved item compressed to a ledger line, the line names what it was and points to the prior version for detail (e.g. "Auth provider choice settled on Auth0; see v2 for the comparison.").

## 4. Project the length and surface a verdict

1. Project the regenerated length against `length_contract.per_version_soft_target` (tokens; destination-aware via `config/platform-parameters.md`, tightening to the destination limit when smaller). The operator-facing proxy is a word count.
2. If the projection is over budget, pre-flight surfaces a verdict recommending which resolved items to compress further. It surfaces; it does **not** hard-block (`references/defaults.md` section 4).
3. The per-version budget is the technical ceiling. update accumulates by design across the chain, but each version stays within the per-version budget; the accumulating total lives in the supersession chain, not in the latest file.

## 5. Write the resumption payload

Regenerate the two-zone payload. The field-by-field schema is owned by `modes/generate.md` section 4; the Zone 2 sections, activation, and order are owned by `references/section-activation.md`. update applies the curation across both zones:

- **Zone 1 structured blocks:** live items stay at full fidelity in `open_items`, the live `decisions`, the current `state_snapshot`, the live `known_issues`, and `continuation`. Resolved items compress: a resolved decision keeps its `decision` and a one-line `rationale` pointing to the prior version; a closed open item drops out of `open_items` and is recorded in the `changelog` block. The `changelog` block is populated on update (it is conditional-on-supersession and update always supersedes): set `from_version`/`to_version`, record `data_changes`/`structural_changes`, and list each item resolved since the prior version in `changelog.resolved_since_prior` as a one-line ledger entry that points to the prior version for detail (`references/schema.md` section 2.1).
- **Zone 2 narrative:** live context at full fidelity; resolved context compresses to ledger lines in Decisions and Rationale and Open Items in Context, each pointing to the prior version for detail.

Refresh `state_captured_at`, `status`, `stage`, `review_by`, and `agent_actionable`. Re-derive governance per the resolution order (governance can change between versions if the operator or org-config changed it; never silently lower sensitivity). Carry forward `schemas`, `artifacts`, and `source_ingestion` blocks that are still live at full fidelity; do not prosify the verifiable `state_markers`/`metrics`.

## 6. Write the file and validate

1. Filename: `<handoff_id>-v<N>.md` with the incremented `handoff_version`.
2. Run the validation checklist (`references/schema.md` section 6) and the lineage-consistency rules (`references/lineage.md` section 7): `mode: update` requires `supersedes` non-null and `handoff_version > 1`.
3. No SPDX header on the handoff.

## 7. Post-flight

Emit the post-flight summary (`references/preflight.md` section 9): the preserved `handoff_id`, the new `handoff_version`, the `supersedes` pointer, and a **curation report** stating what was carried at full fidelity and what was compressed to ledger lines. If the length projection was over budget, restate the recommendation and what the operator chose. Note that the prior version is retained as the archive.

## 8. Failure handling

| Failure | Handling |
|---|---|
| Prior handoff not found | Report; offer to treat as a fresh generate instead. Do not invent a supersession. |
| Prior is stale-schema | Compose retrofit first (`modes/retrofit.md` section 6); report the composition. |
| A live item would be dropped or compressed | Defect; do not write. Live items carry at full fidelity. |
| Projection over budget | Surface the verdict and recommendation; never hard-block; let the operator decide. |
| Validation or lineage-consistency check fails | Halt; report; do not present the file. |

## 9. Cross-references

- Supersession semantics: `references/lineage.md` section 2.
- The length contract and the per-version budget: `references/defaults.md` section 4.
- Destination-aware budget tightening: `config/platform-parameters.md`, `references/platform-specific-parameters.md`.
- The retrofit step update composes on stale input: `modes/retrofit.md` section 6.
- Pre-flight and the `confirm update` token: `references/preflight.md`.
- A worked example: `references/examples/example-updated-handoff.md`.
