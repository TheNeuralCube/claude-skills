---
file_role: skill-reference
topic: defaults
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Defaults (session-handoff v0.1.0)

This file is the single source of truth for the universal public defaults the skill applies when no `config/user-config.md`, `config/org-config.md`, or `config/redaction-policy.md` overrides them. It is skill-owned and not user-editable: it lives in `references/`, not `config/`. Editable knobs live in the config layer.

Resolution order: `config/user-config.md` > `config/org-config.md` > this file > field-level inferences from session state. For governance on consolidated handoffs, most-restrictive derivation from sources takes precedence over the default layers (`references/lineage.md` section 4).

If a value appears here, it can be overridden in a config file. If a value does not appear here, it is not user-tunable in v0.1.0 (see section 8).

## 1. Sanitization gate

```yaml
sanitization_prompt: on-signal     # always | on-signal | never
```

- `always` (set by an enterprise org-config that wants a sanitize prompt on every run) fires the blocking sanitize question on every invocation.
- `on-signal` (public default) fires the blocking sanitize question only when sharing is signaled or sensitive content (including flagged PII) is detected.
- `never` suppresses the blocking question. The locked sanitization-surfacing line (section 2) still always emits regardless of this setting.

Out-of-box default is `on-signal`. Move to `always` only if `on-signal` under-fires in practice.

## 2. Sanitization surfacing (always on, not configurable)

Pre-flight always emits this line verbatim, regardless of `sanitization_prompt`:

```
Sanitization is available. If this handoff will be shared with another person, run
share-sanitize to produce a redacted copy and a manifest of what was removed. Say
"sanitize this for sharing" to invoke it.
```

The surfacing line is not gated and not editable. Only the **blocking** sanitize question is gated, by `sanitization_prompt`.

## 3. PII flagging

```yaml
pii_flagging:
  enabled: true                      # secure-by-default exception
  categories: [name, email, phone, address, gov_id, account_number]
  mode: flag-for-review              # never auto-removes
```

PII flagging is the one secure-by-default exception: it is enabled out of the box. It is assistive (flags for operator review; never auto-removes; never claims completeness). See `references/redaction.md`.

## 4. The update length contract

```yaml
length_contract:
  unit: tokens                       # words shown as the operator-facing proxy
  per_version_soft_target: 12000     # readability and review budget, not a hard cap
  destination_aware: true            # tightens to the destination limit when smaller
  on_overflow: surface_and_curate    # pre-flight recommends curation; never hard-blocks
```

- The budget is **per-version**, not accumulating-total. The latest handoff is not an append log; the accumulating total lives in the supersession chain.
- On `update`, live items (open decisions, active open items, current state) carry forward at full fidelity. Items resolved since the prior version compress to one-line ledger entries; their detail stays recoverable in the superseded version.
- The destination-aware budget tightens to the destination platform's limit when that is smaller than `per_version_soft_target` (`config/platform-parameters.md`).
- On overflow, pre-flight surfaces a verdict recommending which resolved items to compress. It surfaces; it does not hard-block.

The curation is a lightweight heuristic (current at full fidelity, resolved to ledger lines). It is explicitly not a scoring algorithm or a merge classifier. The per-version soft target starts at 12000 tokens and is tuned against real handoffs.

## 5. The consolidate cap

```yaml
consolidate:
  max_sources: 3            # soft review-batch guardrail, NOT the technical ceiling
  cap_mode: soft            # soft = warn plus override token above cap; hard = refuse
```

Two gates protect two different things:

| Gate | Protects | Arbiter |
|---|---|---|
| per-version budget (section 4) | destination context fit and review digestibility | tokens, destination-aware; the real ceiling |
| source count cap | operator review quality, merge fidelity | soft count, default 3; a human-factors guardrail |

- In `soft` mode, N over `max_sources` requires `confirm over-cap`.
- In `hard` mode, N over `max_sources` is refused.
- The value 3 is a soft, non-load-bearing default. An enterprise org-config may set `cap_mode: hard` for approval discipline and may tighten `max_sources` for high-sensitivity merges.

## 6. Governance defaults

```yaml
governance:
  sensitivity: internal
  retention: null
  governance_frameworks: []
  custom_governance: null
```

Public defaults are light and ignorable. Enterprise org-config populates the taxonomy and regulatory scope. See `references/governance.md`.

## 7. Default trigger phrases

The five modes share one entry point; pre-flight auto-routes. The default trigger phrases (case-insensitive, whitespace-tolerant) are catalogued in `SKILL.md` and `references/preflight.md`. Triggers are not redefined here; this section records only that the default set is the one shipped in SKILL.md and is not narrowed by the public config.

## 8. What is NOT configurable in v0.1.0

These behaviors are fixed at the skill level. Listed so deployers do not look for override knobs.

- The pre-flight protocol and the `## Protocol` structural gate.
- The pre-flight algorithm, verdict set, and routing table.
- The metadata-contract field set and the `_managed_by` string.
- The `handoff_id` derivation and the `HND` prefix.
- The confirmation token names.
- The mode taxonomy (distinct internal paths, one auto-routed entry point).
- The seam-not-engine boundary for share-sanitize.
- The locked sanitization-surfacing line (section 2).
- The two honesty guardrails (PII assistive; `approved_by` self-asserted).
- The no-empty-fields Parse Error.

If a deployer needs to change one of these, the right answer is a config-expressible behavior (if one exists) or a future skill release, not an override.

## 9. Cross-references

- Governance taxonomy and resolution order: `references/governance.md`.
- Redaction policy and the `redaction_provider` seam: `references/redaction.md`.
- Length contract application: `modes/update.md`.
- Consolidate cap application: `modes/consolidate.md`.
- Pre-flight, verdicts, tokens, sanitization surfacing: `references/preflight.md`.
- Per-platform limits and overflow strategy: `config/platform-parameters.md`, `references/platform-specific-parameters.md`.
- Config layering and the shared interview: `references/configure.md`.
