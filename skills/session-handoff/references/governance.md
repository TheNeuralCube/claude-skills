---
file_role: skill-reference
topic: governance
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Governance metadata framework (session-handoff v0.1.0)

The session-handoff skill ships a governance metadata framework so handoffs carry the policy attributes enterprise environments care about (sensitivity, retention, applicable frameworks) and so the redaction subsystem can key off them. The framework is **a schema plus the rules that read it**, not an external integration: the skill captures the metadata, derives most-restrictive governance on consolidation, keys redaction off sensitivity, and emits a sensitivity-aware handling instruction to the receiving agent. v0.1.0 does not call DLP services, does not enforce retention, and does not apply ACLs.

The governance block is REQUIRED on every handoff (`references/schema.md` section 1). This file owns the taxonomy and the resolution order; it anchors both the sanctioned-destination awareness feature and share-sanitize.

## 1. The governance block

```yaml
governance:
  sensitivity: "open" | "internal" | "confidential" | "restricted"
  retention: <string|null>
  governance_frameworks: []
  custom_governance: <string|null>
```

### 1.1 sensitivity

Allowed values, ordered least to most restrictive: `open` < `internal` < `confidential` < `restricted`.

| Value | Meaning |
|---|---|
| `open` | Public or shareable with no restrictions. |
| `internal` | Within the organization or the operator's trusted circle. **Public default.** |
| `confidential` | Limited to specific people, teams, or contracts. |
| `restricted` | Highly sensitive; access strictly controlled (legal hold, board-level, regulated PII). |

The public default is `internal`. The ordering is load-bearing: consolidation takes `max(sources.sensitivity)` (`references/lineage.md` section 4), and the redaction `sensitivity_rules` map keys off the value (`references/redaction.md`).

### 1.2 retention

A free-form string or `null`, e.g. `"review_by 2026-08-31"` or `"indefinite"`. The skill does not delete or expire handoffs based on this value; it is metadata for downstream systems and for the operator. On consolidation, the strictest source retention wins.

### 1.3 governance_frameworks

A list of framework names that apply, e.g. `["SOX", "ITAR", "GDPR"]`. Empty `[]` in the public default. The skill does not validate framework names. On consolidation, the union of source frameworks applies. A handoff carrying any framework is treated as protected for source-retention gating (`references/lineage.md` section 5).

### 1.4 custom_governance

A free-form string for org-specific governance dimensions that do not fit the three fields above, or `null`. On consolidation, non-conflicting source values concatenate; a genuine conflict is flagged for operator review rather than silently resolved.

## 2. Resolution order

When governance values are determined for a generated handoff, apply this order, each later layer overriding the earlier for the fields it declares:

1. Public defaults from `references/defaults.md` (`sensitivity: internal`, `governance_frameworks: []`).
2. `config/org-config.md` if present (org taxonomy and regulatory scope).
3. `config/user-config.md` if present (per-user privacy defaults).
4. Operator instructions in the current invocation.

For a **consolidated** handoff, the most-restrictive derivation from the sources (`references/lineage.md` section 4) takes precedence over the default layers, because downgrading a consolidated classification would be a governance failure. Operator instruction can raise sensitivity above the derived value but pre-flight warns before lowering it.

## 3. The eight enterprise features and calibration

All governance behavior ships in the core. Burden is calibrated by config, not by fork: a personal user gets a light, ignorable experience; an enterprise gets a rigorous one.

| # | Feature | Public default | Enterprise (org-config) |
|---|---|---|---|
| 1 | Governance metadata on every handoff | `sensitivity: internal`, frameworks empty | org taxonomy and regulatory scope populated |
| 2 | Governance-aware redaction | keys off sensitivity via `sensitivity_rules` | stricter forced categories |
| 3 | Shared org-config across sister skills | one org-config honored by project-context and session-handoff | configure compliance once |
| 4 | Sanctioned-destination awareness | unrestricted until an org defines it | sanctioned list enforced; pre-flight warns or blocks |
| 5 | Redaction manifest | emitted on share-sanitize; categories and counts only | same; may be required by policy |
| 6 | Receiving-agent handling block | a standing, sensitivity-aware instruction in the handoff body | same; may be mandated |
| 7 | PII flagging | enabled (the one secure-by-default exception) | enabled, possibly stricter policy |
| 8 | Provenance and audit block | populates from config or null | populated; org may require `approved_by` |

### 3.1 Sanctioned-destination awareness (feature 4)

An org-config may declare a list of sanctioned destinations (platforms, tools, recipients). When set, pre-flight checks the stated or detected destination of a handoff against the list and warns (or, if the org sets enforcement to block, refuses) when the destination is not sanctioned. The public default declares no list, so the check is inert until an org defines it. The skill never invents a sanctioned list.

### 3.2 Receiving-agent handling block (feature 6)

Every handoff body carries a standing, sensitivity-aware instruction to the destination agent on how to treat the handoff. The exact wording per sensitivity is build-session latitude (design spec section 17); the intent per tier:

| Sensitivity | Handling instruction intent |
|---|---|
| `open` | No special handling; treat as shareable working context. |
| `internal` | Keep within the operator's trusted circle; do not forward outside the organization without operator direction. |
| `confidential` | Limited audience; do not redistribute; confirm the recipient is authorized before acting on or forwarding. |
| `restricted` | Strict handling; do not redistribute, quote, or persist beyond the immediate task without explicit operator authorization. |

The block is descriptive instruction to the receiving agent, not an enforcement mechanism. It travels in the resumption payload (`references/schema.md` section 2).

## 4. The two honesty guardrails

Stated here, in `references/schema.md` section 4.1, and in the README.

- **PII flagging is assistive.** The skill flags possible PII for review and never claims to have found or removed all PII. See `references/redaction.md`.
- **`approved_by` is self-asserted.** Verbatim: "approved_by is self-asserted from user-config identity. It is not platform-verified and must not be treated as authenticated identity until a platform identity API exists."

## 5. What v0.1.0 does and does not do

**v0.1.0 does:**
- Capture governance metadata on every handoff.
- Derive most-restrictive governance on consolidation.
- Key redaction off sensitivity via `sensitivity_rules`.
- Emit a sensitivity-aware receiving-agent handling block.
- Apply governance defaults in resolution order across config layers.
- Gate protected-source deletion on consolidation.

**v0.1.0 does not:**
- Call DLP, ACL, or compliance services.
- Enforce retention or auto-delete handoffs.
- Validate framework names.
- Treat `approved_by` as authenticated identity.
- Guarantee PII detection completeness.

Integrations (DLP, ACL, retention enforcement, a platform identity API for verified `approved_by`) are future workstreams tracked in `ROADMAP.md`.

## 6. Cross-references

- Governance block in the metadata contract: `references/schema.md` section 1.
- Most-restrictive consolidation propagation and source-retention gating: `references/lineage.md` sections 4 and 5.
- Redaction policy, `sensitivity_rules`, manifest: `references/redaction.md`.
- Sanctioned-destination and sanitization surfacing in pre-flight: `references/preflight.md`.
- Governance defaults: `references/defaults.md`.
- Config layering: `config/org-config.md.template`, `config/user-config.md.template`, `references/configure.md`.
