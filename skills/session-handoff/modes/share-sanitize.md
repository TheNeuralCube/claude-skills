---
file_role: skill-mode
mode: share-sanitize
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Mode: share-sanitize

## Pre-flight prerequisite

This mode runs only after pre-flight (`references/preflight.md`) has completed and the operator has typed `confirm sanitize`. Redaction is a decision with sharing consequences, so the token gate is mandatory. Do not execute this mode without pre-flight completion and the token.

share-sanitize produces a redacted derivative copy of a handoff plus a manifest of what was removed (categories and counts only, never content). It is the built-in mini-system behind the `redaction_provider` seam: a deliberately minimal, model-driven redactor that a future sister skill (document-sanitizer) can replace without changing this mode's shape.

share-sanitize is one of the three unproven modes new in v0.1.0. Its derivative identity, the manifest, the seam routing, and the honesty guardrails are field-tested in the build session; any failure is build-blocking (build spec section 5.1).

Redaction mechanics: `references/redaction.md`. Derivative identity: `references/lineage.md` section 6. Governance taxonomy: `references/governance.md`.

## 1. The seam, not the engine

Behind a stable contract (in: handoff plus policy; out: redacted copy plus manifest) is the `redaction_provider` switch (`config/redaction-policy.md`):

- `redaction_provider: built-in` (default): run the masking and PII-flagging steps here, with the model (sections 3 and 5).
- any other value (e.g. `document-sanitizer`): route the masking and flagging steps to that provider against the same contract. This mode's shape, its derivative identity, and its manifest do not change.

Do not build a comprehensive redaction engine in this mode. The built-in provider is intentionally minimal.

## 2. Load the policy and resolve the active set

1. Load `config/redaction-policy.md`, or `references/defaults.md` if absent.
2. Resolve the active category set: `sensitivity_rules[handoff.governance.sensitivity]` plus any categories named at invocation (e.g. "redact this for the vendor" may add `client_names`).

## 3. Run PII flagging (assistive, never auto-removes)

If `pii_flagging.enabled` (default true), scan for the configured PII categories and flag candidates for operator review. PII flagging is distinct from redaction: it flags, it does not remove. A flagged item the operator chooses to keep is recorded in the manifest as `pii_flagged_not_redacted` (count only). PII flagging is assistive and never claims completeness (`references/redaction.md` section 5).

## 4. Surface the plan (pre-flight) and gate

Pre-flight has surfaced the plan: the categories to mask, the candidate counts, and the assistive disclaimer, and has required `confirm sanitize`. Proceed only after the token.

## 5. Produce the redacted derivative copy

Mask the active category set per `masking_style` (`tag` default: `[REDACTED:category]`) across both zones (`references/schema.md` section 2): the Zone 1 tier-2 structured blocks (a client name in `artifacts`, `state_snapshot`, or `people_involved`; a credential in `continuation.toolchain`) and the Zone 2 narrative. The tier-1 metadata contract and the lineage fields are preserved (they carry no masked content). Write the redacted copy with:

- the **same `handoff_id`** as the source (the sanitized copy is recognizably the same handoff),
- `derivative_of` set to the source `<handoff_id>#v<N>`,
- `generation_mode: sanitized`,
- `mode: share-sanitize`,
- `supersedes: null` (a sanitized copy is a leaf derivative, not in the supersession chain; `references/lineage.md` section 6),
- `prior_handoffs` and `consolidation_depth` **preserved verbatim from the source** (so a sanitized derivative of a consolidation carries that consolidation's ledger and depth, and a derivative of a plain handoff carries `[]` and `0`). share-sanitize masks content; it does not rewrite lineage (`references/lineage.md` sections 6 and 7).

The canonical, unredacted handoff is unchanged and remains canonical.

## 6. Emit the redaction manifest

Emit the manifest (`references/redaction.md` section 4): categories and counts only, never content. It carries `source_handoff_id`, `redacted_at`, `redaction_provider`, `policy_schema_version`, the by-category counts, `pii_flagged_not_redacted`, `masking_style`, and the mandatory assistive disclaimer:

```
Redaction is assistive and model-based. It is not guaranteed to find or remove all
sensitive content. Review the redacted output before sharing.
```

Set `audit.redaction_manifest` on the derivative copy to the manifest path.

## 7. Validate and write

1. Run the validation checklist (`references/schema.md` section 6) and lineage-consistency rules (`references/lineage.md` section 7): `mode: share-sanitize` requires `derivative_of` non-null, `generation_mode: sanitized`, `supersedes: null`.
2. Filename for the derivative: `<handoff_id>-v<N>-sanitized.md` (keeps it visibly distinct from the canonical file).
3. No SPDX header on the handoff or the manifest (operator work product).

## 8. Post-flight

Emit the post-flight summary (`references/preflight.md` section 9): the manifest summary (categories and counts), the assistive disclaimer restated, the flagged-not-redacted count, the `derivative_of` pointer, and a reminder that the canonical handoff is unchanged and that the operator should review the redacted output before sharing.

## 9. Failure handling

| Failure | Handling |
|---|---|
| No policy and no defaults reachable | Halt; do not guess a redaction set. |
| `redaction_provider` is non-built-in but the provider is unavailable | Report; do not silently fall back to a weaker redactor without telling the operator. |
| Source handoff not found | Report; nothing to sanitize. |
| Validation or lineage-consistency check fails | Halt; report; do not present the copy. |
| The redactor cannot guarantee completeness | This is expected and disclosed, not a failure. The assistive disclaimer is mandatory; never claim completeness. |

## 10. Cross-references

- Built-in redactor, manifest format, the `redaction_provider` seam: `references/redaction.md`.
- Derivative identity rules: `references/lineage.md` section 6.
- Sensitivity taxonomy and `sensitivity_rules`: `references/governance.md`, `config/redaction-policy.md.template`.
- Sanitization surfacing and the `confirm sanitize` token: `references/preflight.md`.
- A plain-language walkthrough: `USAGE.md`.
- A worked example: `references/examples/example-sanitized-handoff.md`.
