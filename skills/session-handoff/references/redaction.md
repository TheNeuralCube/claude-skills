---
file_role: skill-reference
topic: redaction
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Redaction subsystem (session-handoff v0.1.0)

This file specifies the built-in redactor that share-sanitize uses, the redaction manifest format, and the `redaction_provider` seam. The governing design principle is **the seam, not the engine**: share-sanitize is built with a clean delegation contract rather than a hardwired redaction engine, so a future sister skill (document-sanitizer) can own the general engine without changing share-sanitize's shape.

Mechanics here are consumed by `modes/share-sanitize.md`. The redaction policy lives in `config/redaction-policy.md` (operator-editable); its template is `config/redaction-policy.md.template`. When no policy is present, the skill falls back to the public defaults in `references/defaults.md`.

## 1. The seam, not the engine

The redaction step is a stable contract:

```
in:  a handoff + a redaction policy
out: a redacted derivative copy + a manifest of categories and counts (never the content)
```

Behind the contract is a `redaction_provider` switch:

```yaml
# config/redaction-policy.md
redaction_provider: built-in        # 0.1.0 default; document-sanitizer reserved for the future shared engine
```

- `redaction_provider: built-in` runs the masking and PII-flagging steps with the model (the deliberately minimal redactor specified below).
- When the candidate `document-sanitizer` sister skill ships and becomes the general redaction engine, the switch flips to `document-sanitizer` and the masking and flagging steps route to that skill against the same contract (in: handoff plus policy; out: redacted copy plus manifest). share-sanitize does not change shape, because the contract held.

Do not build a comprehensive redaction engine in this skill. The built-in provider is intentionally minimal; the engine, if it grows, belongs in the sister skill.

## 2. Redaction policy schema

The policy keys off the org-config compliance taxonomy (`references/governance.md`).

```yaml
# config/redaction-policy.md (rendered from config/redaction-policy.md.template)
redaction_provider: built-in
pii_flagging:
  enabled: true                      # secure-by-default exception
  categories: [name, email, phone, address, gov_id, account_number]
  mode: flag-for-review              # never auto-removes; flags for operator decision
categories: [pii, financials, client_names, internal_names, credentials]
masking_style: tag                   # redact -> [REDACTED]; tag -> [REDACTED:category]; hash -> stable token
sensitivity_rules:
  open:         []                                          # nothing forced
  internal:     [credentials]
  confidential: [credentials, pii, client_names]
  restricted:   [credentials, pii, client_names, financials, internal_names]
custom_patterns: []                  # optional org descriptors or regex
```

### 2.1 PII flagging versus redaction (distinct mechanisms)

These are deliberately separate so the honesty guardrail stays legible.

| Mechanism | What it does | Default |
|---|---|---|
| PII flagging | An assistive detection signal. Scans for PII categories and flags candidates for operator review. Feeds the on-signal sanitize gate. **Never auto-removes.** | enabled |
| Redaction | The masking share-sanitize applies, governed by `categories`, `sensitivity_rules`, and any categories named at invocation. | runs on share-sanitize |

PII flagging is the one secure-by-default exception (it is on out of the box). It flags; the operator decides. A flagged item the operator chooses to keep is recorded in the manifest as `pii_flagged_not_redacted` (count only), so the decision is auditable.

### 2.2 masking_style

| Style | Output |
|---|---|
| `redact` | `[REDACTED]` |
| `tag` | `[REDACTED:category]` (default; preserves what kind of thing was removed) |
| `hash` | a stable token, so repeated occurrences of the same value remain co-referenced without revealing it |

## 3. The built-in mini-system

share-sanitize runs these steps (full flow in `modes/share-sanitize.md`):

1. Load `config/redaction-policy.md`, or `references/defaults.md` if absent.
2. Resolve the active category set: `sensitivity_rules[handoff.governance.sensitivity]` plus any categories named at invocation.
3. Run PII flagging if enabled; flag candidates for review (does not remove).
4. Pre-flight surfaces the plan (categories to mask, candidate counts, the assistive disclaimer) and requires `confirm sanitize`, since redaction is a decision.
5. Produce the redacted derivative copy: same `handoff_id`, `derivative_of` set to the source `<handoff_id>#v<N>`, `generation_mode: sanitized`, and the source's `prior_handoffs` and `consolidation_depth` preserved verbatim. The copy is a leaf derivative, not canonical and not in the supersession chain (`references/lineage.md` sections 6 and 7).
6. Emit the redaction manifest (section 4): categories and counts only, never content.
7. Set `audit.redaction_manifest` on the derivative to the manifest path.
8. Post-flight reports the manifest summary.

## 4. The redaction manifest

The manifest reports categories and counts only. It never reproduces redacted content. Manifest rendering details (column order, counts format) are build-session latitude within this schema.

```yaml
---
schema_version: "0.1"
_managed_by: session-handoff-skill
manifest_type: redaction
source_handoff_id: "<handoff_id>#v<N>"
redacted_at: <ISO 8601>
redaction_provider: built-in
policy_schema_version: "0.1"
---
# Reports categories and counts only. Never reproduces redacted content.
summary:
  total_redactions: <int>
  by_category: { pii: <int>, financials: <int>, client_names: <int> }
  pii_flagged_not_redacted: <int>    # operator chose to keep; recorded for audit
  masking_style: tag
disclaimer: >
  Redaction is assistive and model-based. It is not guaranteed to find or remove all
  sensitive content. Review the redacted output before sharing.
```

The `disclaimer` is mandatory on every manifest. The `pii_flagged_not_redacted` count is mandatory whenever PII flagging ran and the operator kept any flagged item.

## 5. The honesty guardrail (mandatory)

The built-in redactor must never over-claim completeness.

- The assistive disclaimer (section 4) appears on the manifest and is restated in the share-sanitize post-flight summary.
- PII flagging is framed as review-only in all operator-facing output: the skill flags possible PII and never claims to have found or removed all of it.
- The redacted copy carries `generation_mode: sanitized` and `derivative_of`, so no reader mistakes it for the canonical, unredacted handoff.

## 6. Cross-references

- The share-sanitize flow that drives this subsystem: `modes/share-sanitize.md`.
- Derivative identity rules for sanitized copies: `references/lineage.md` section 6.
- Sensitivity taxonomy the policy keys off: `references/governance.md`.
- Sanitization surfacing line and the on-signal gate: `references/preflight.md`, `references/defaults.md`.
- Redaction policy template and field guide: `config/redaction-policy.md.template`.
- The shared config interview: `references/configure.md`.
