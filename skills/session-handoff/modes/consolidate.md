---
file_role: skill-mode
mode: consolidate
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Mode: consolidate

## Pre-flight prerequisite

This mode runs only after pre-flight (`references/preflight.md`) has completed and the operator has typed `confirm consolidate` (plus `confirm over-cap` and `confirm delete protected sources` where applicable). Do not execute this mode without pre-flight completion and the required tokens.

consolidate gathers N prior handoffs (cap-bounded) plus optional new conversation into one consolidated handoff with a new identity and a ledger of its sources. A consolidation is a new artifact, never a continuation of a source thread.

consolidate is one of the three unproven modes new in v0.1.0. Its identity rules, the prior_handoffs ledger, most-restrictive governance propagation, the cap, and governance-gated source retention are field-tested in the build session; any failure in identity, lineage, governance propagation, or content preservation is build-blocking (build spec section 5.1).

Schema reference: `references/schema.md`. Lineage and governance propagation: `references/lineage.md`. Cap defaults: `references/defaults.md` section 5.

## 1. Gather the sources and check the cap

1. Gather the N source handoffs the operator selected.
2. Check the cap (`references/defaults.md` section 5):
   - `cap_mode: soft` (default): if N exceeds `max_sources` (default 3), require `confirm over-cap` before proceeding.
   - `cap_mode: hard`: if N exceeds `max_sources`, refuse above the cap.
3. The per-version budget is the real technical ceiling; the count cap is a human-factors guardrail protecting review quality. Both gates apply.
4. **If any source is stale-schema**, compose retrofit on that source first (`modes/retrofit.md`) so all sources are at the current schema before merging.

## 2. Mint a new identity

- Mint a fresh `handoff_id` from the consolidated topic and date (`references/schema.md` section 3).
- Set `mode: consolidate`, `generation_mode: consolidated`.
- `supersedes: null` (a consolidation supersedes nothing; it gathers).
- `handoff_version: 1`.
- `consolidation_depth` is one greater than the maximum `consolidation_depth` among the sources (so re-consolidation is auditable at arbitrary depth). It does not feed the cap.

## 3. Build the prior_handoffs ledger

Build `prior_handoffs` from the immediate sources. Entry shape is calibrated by config (`references/lineage.md` section 3.1):

- Public default: an id string, `"<handoff_id>#v<N>"`.
- Enterprise org-config: an object `{ id, kind: source|consolidation, sensitivity }`, so the consolidated handoff self-audits without opening sources that may later be deleted.

## 4. Derive governance (most-restrictive wins)

Derive the consolidated governance from the sources, never defaulted (`references/lineage.md` section 4):

```
consolidated.sensitivity           = max(sources.sensitivity)        # open < internal < confidential < restricted
consolidated.retention             = strictest(sources.retention)
consolidated.governance_frameworks = union(sources.frameworks)
consolidated.custom_governance     = concat non-conflicting, else flag conflict for operator review
```

Never silently downgrade: consolidating a confidential source into an internal default is a governance failure. The mixed-sensitivity case (one confidential source among internal sources, output must be confidential) is mandatory in testing.

## 5. Merge content with current-versus-resolved curation

Merge the source two-zone payloads using the same current-versus-resolved curation as update (`modes/update.md` sections 3 and 5), against the per-version budget. The payload schema is owned by `modes/generate.md` section 4; the Zone 2 sections by `references/section-activation.md`.

- **Zone 1:** union and de-duplicate the structured blocks across sources. Live `open_items`, `decisions`, `state_snapshot`, `artifacts`, `schemas`, and `source_ingestion` carry at full fidelity; preserve verifiable `state_markers`/`metrics`, do not prosify them. Resolved items compress into the consolidated `changelog`. The merged `artifacts.deliverables` is the union of distinct deliverables across sources.
- **Zone 2:** live narrative carries at full fidelity, de-duplicated; resolved narrative compresses to ledger lines pointing back to the source that holds the detail.
- When two sources conflict on a live item, surface the conflict to the operator rather than silently picking one.

The curation is the same lightweight heuristic, not a scoring algorithm or merge classifier.

## 6. Capture the flattened lineage into the audit record

At consolidation time, capture the **flattened lineage** (the full source-and-version list, including each source's governance) into the post-flight audit record. This is what makes a consolidated handoff's complete provenance survive even if light sources are later deleted (`references/lineage.md` section 5). Do this before any source-deletion step.

## 7. Source retention

Sources are retained by default. If the operator asks to delete sources:

- If any source is `confidential` or `restricted`, or carries `governance_frameworks`, require `confirm delete protected sources`.
- If all sources are `open` or `internal` with no frameworks, proceed after standard confirmation.

The flattened lineage (section 6) is already captured, so deletion does not lose provenance. The skill itself does not delete files on platforms without a file-management API; it reports which sources the operator may delete after verifying the consolidated handoff.

## 8. Write the file and validate

1. Filename: `<new_handoff_id>-v1.md`.
2. Run the validation checklist (`references/schema.md` section 6) and lineage-consistency rules (`references/lineage.md` section 7): `mode: consolidate` requires `prior_handoffs` non-empty, `supersedes: null`, `generation_mode: consolidated`.
3. No SPDX header on the handoff.

## 9. Post-flight

Emit the post-flight summary (`references/preflight.md` section 9): the new `handoff_id`, the `prior_handoffs` ledger, `generation_mode: consolidated`, `consolidation_depth`, the derived most-restrictive governance, and the flattened lineage captured into the audit record. If the operator opted to delete sources, list which sources to delete after verifying the consolidated handoff, and confirm the protected-source gate was satisfied.

## 10. Failure handling

| Failure | Handling |
|---|---|
| N over cap, soft mode | Require `confirm over-cap`. |
| N over cap, hard mode | Refuse above `max_sources`; report. |
| A source is stale-schema | Compose retrofit on it first. |
| Mixed-sensitivity sources | Derive most-restrictive; never downgrade. |
| custom_governance conflict | Flag for operator review; do not silently resolve. |
| Live items conflict across sources | Surface to operator; do not silently pick one. |
| Delete requested on protected sources | Require `confirm delete protected sources`; lineage already captured. |
| Validation or lineage-consistency check fails | Halt; report; do not present the file. |

## 11. Cross-references

- Consolidation identity, ledger shape, governance propagation, source retention: `references/lineage.md` sections 3 to 5.
- The cap and its two gates: `references/defaults.md` section 5.
- The shared current-versus-resolved curation: `modes/update.md` section 3.
- The retrofit step composed on stale sources: `modes/retrofit.md`.
- Pre-flight, the consolidate tokens, the mixed-sensitivity example: `references/preflight.md`.
- A worked example: `references/examples/example-consolidated-handoff.md`.
