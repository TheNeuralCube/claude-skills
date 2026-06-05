---
file_role: skill-reference
topic: lineage
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Lineage and consolidation rules (session-handoff v0.1.0)

This file is the canonical definition of the lineage fields and the rules that govern supersession, consolidation identity, governance propagation, and source retention. The session-handoff analog to a topology graph is a **lineage chain**: supersession (one version replaces a prior version) and consolidation (one artifact gathers several sources). It is designed on its own terms, not borrowed from the benchmark.

The lineage fields are part of the metadata contract (`references/schema.md` section 1). This file owns their semantics.

## 1. The lineage fields

| Field | Owned by mode | Semantics |
|---|---|---|
| `handoff_id` | all | Stable identity of a handoff thread. Self-derived (`references/schema.md` section 3). Stable across `update` versions. |
| `handoff_version` | generate, update | Starts at 1, increments on `update`. Disambiguates versions sharing one `handoff_id`. |
| `supersedes` | update | `<handoff_id>#v<N>` pointing to the immediately prior version. `null` except on `update`. Robust to file moves because it points to an id-plus-version, not a path. |
| `prior_handoffs` | consolidate (preserved by share-sanitize) | The consolidation ledger: the immediate sources of a consolidated handoff. Non-empty for `mode: consolidate`, or preserved verbatim on a `share-sanitize` derivative of a consolidation; `[]` otherwise. Entry shape calibrated by config (section 3.1). |
| `consolidation_depth` | consolidate (preserved by share-sanitize) | 0 for non-consolidated handoffs; one greater than the maximum source depth on `consolidate`; preserved verbatim on a sanitized derivative. Audit only; does not feed the consolidate cap. |
| `derivative_of` | share-sanitize | `<handoff_id>#v<N>` marking a sanitized copy as a leaf derivative of a canonical handoff. `null` otherwise. |

The predecessor's external-lookup deferral is removed: there is no external registry. All identity and lineage live inside the document, which is the self-containment principle (P1).

## 2. Supersession (update)

`update` produces a new version of the same handoff thread.

- `handoff_id` is preserved unchanged.
- `handoff_version` increments by one.
- `supersedes` is set to the prior version's `<handoff_id>#v<N>`.
- The prior version is the **durable archive** for any detail the update curates away (see `references/defaults.md` length contract and `modes/update.md`). The latest version is not an append log; the accumulating total lives in the chain.

A reader resolving `supersedes` walks backward to the prior version. The chain is linear: each version supersedes exactly one prior version.

## 3. Consolidation identity

A consolidation produces a **new artifact identity**, never a continuation of a source thread.

- It gets a fresh `handoff_id` (minted from the consolidated topic and date per `references/schema.md` section 3).
- `generation_mode: consolidated`.
- `supersedes: null`. A consolidation supersedes nothing; it gathers.
- `prior_handoffs` is the ledger of the immediate sources.
- `consolidation_depth` is one greater than the maximum `consolidation_depth` among the sources, so re-consolidation is auditable at arbitrary depth.

Why a new identity rather than inheriting a source id: inheriting a source `handoff_id` would make the consolidation masquerade as a continuation of one thread and corrupt that thread's audited identity. External references to the source ids correctly resolve to the (now superseded-by-consolidation, but still self-identifying) source artifacts; the new artifact is discoverable through its ledger.

### 3.1 prior_handoffs entry shape (calibrated)

The ledger entry shape is set by config:

| Config tier | Entry shape | Rationale |
|---|---|---|
| Public default | an id string: `"HND-...#v2"` | minimal; the source files carry the rest |
| Enterprise org-config | an object: `{ id, kind: source\|consolidation, sensitivity }` | self-auditing without traversing files that may have been deleted |

The enriched object lets a consolidated handoff answer "what was I built from, and how sensitive was each source" without opening the sources, which matters when sources are later deleted (section 5).

## 4. Governance propagation (most-restrictive wins)

The consolidated governance is **derived from its sources, not defaulted**. Without this, consolidating a confidential source into an internal-default output would silently downgrade classification.

```
consolidated.sensitivity           = max(sources.sensitivity)        # most restrictive
consolidated.retention             = strictest(sources.retention)    # longest, tightest
consolidated.governance_frameworks = union(sources.frameworks)
consolidated.custom_governance     = concat, or flag conflict for operator review
```

Sensitivity ordering, most restrictive last: `open` < `internal` < `confidential` < `restricted`. The consolidated handoff takes the maximum.

`retention`: take the strictest (longest or tightest) of the sources. When retention strings are not directly comparable, retain all and flag for operator review rather than guessing.

`custom_governance`: concatenate non-conflicting source values. On a genuine conflict (two sources assert incompatible custom governance), do not silently pick one; flag the conflict in pre-flight for operator review.

This propagation is enforced and tested. The mixed-sensitivity test (one confidential source among internal sources, output must be confidential) is mandatory; see `references/preflight.md` and the build test matrix.

## 5. Source retention

Source deletion after consolidation is operator-opt-in. The flattened lineage is captured into the post-flight audit record **at consolidation time**, so a consolidated handoff's complete provenance survives even if light sources are later deleted.

Pre-flight blocks source deletion (requires `confirm delete protected sources`) when any source is `confidential` or `restricted`, or carries `governance_frameworks`. Sources are retained by default; the operator must explicitly opt in to deletion.

```
default: retain all sources
delete requested + any source confidential/restricted/framework-bearing
  -> require `confirm delete protected sources`
delete requested + all sources open/internal, no frameworks
  -> permitted after standard confirmation
```

## 6. Derivative identity (share-sanitize)

A `share-sanitize` output is a **leaf derivative**, not canonical and not in the supersession chain. It is a faithful redacted copy, so it preserves the source's lineage verbatim and adds one field.

- `handoff_id` is preserved from the source (the sanitized copy is recognizably the same handoff).
- `derivative_of` is set to the source `<handoff_id>#v<N>`.
- `generation_mode: sanitized`.
- `supersedes: null`. A sanitized copy supersedes nothing; the canonical handoff remains canonical.
- `prior_handoffs` and `consolidation_depth` are **preserved verbatim from the source**. A sanitized derivative of a consolidation therefore carries the source consolidation's ledger and depth (it is a redacted copy of that consolidated artifact); a sanitized derivative of a plain handoff carries `[]` and `0`, as its source did. share-sanitize masks content; it does not rewrite lineage.

A reader encountering a `derivative_of` value knows the file is a redacted copy and that a canonical, unredacted version exists under the same `handoff_id`. When that source was a consolidation, the derivative's `prior_handoffs` ledger still resolves the consolidation's sources. See `references/redaction.md`.

## 7. Internal consistency rules

Pre-flight and the mode validation passes enforce:

| Rule | Constraint |
|---|---|
| update implies supersedes | `mode: update` requires `supersedes` non-null and `handoff_version > 1`. |
| supersedes implies update | `supersedes` non-null requires `mode: update` (or a composed retrofit-then-update). |
| consolidate implies ledger | `mode: consolidate` requires `prior_handoffs` non-empty, `supersedes: null`, `generation_mode: consolidated`. |
| sanitize implies derivative | `mode: share-sanitize` requires `derivative_of` non-null, `generation_mode: sanitized`, `supersedes: null`. It preserves the source's `prior_handoffs` and `consolidation_depth` verbatim. |
| prior_handoffs population | `prior_handoffs` is non-empty only for `mode: consolidate` OR for a `share-sanitize` derivative whose source was a consolidation (preserved verbatim). `[]` in every other case. |
| generate is clean | `mode: generate` requires `supersedes: null`, `prior_handoffs: []`, `derivative_of: null`, `handoff_version: 1`, `consolidation_depth: 0`. |
| depth is non-negative | `consolidation_depth >= 0`; non-zero only on a consolidation or on a sanitized derivative of one (preserved verbatim). |

A violation is a Parse Error surfaced in pre-flight or a build-blocking defect surfaced in the mode validation pass.

## 8. Cross-references

- The lineage fields in the metadata contract: `references/schema.md` section 1.
- Update curation and the length contract: `modes/update.md`, `references/defaults.md`.
- Consolidate mechanics, the cap, and the ledger: `modes/consolidate.md`, `references/defaults.md`.
- Share-sanitize derivative emission: `modes/share-sanitize.md`, `references/redaction.md`.
- Governance taxonomy and resolution order: `references/governance.md`.
- Pre-flight verdicts and tokens: `references/preflight.md`.
