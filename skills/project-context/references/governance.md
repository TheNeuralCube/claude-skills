<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Governance metadata framework (project-context v0.7.0)

The project-context skill ships a governance metadata framework so files can carry the policy attributes enterprise environments care about (sensitivity, retention, applicable frameworks). The framework is **a schema**, not an integration: the skill captures the metadata so downstream systems and future skill versions can act on it. The skill does not call DLP services, does not enforce retention, and does not apply ACLs.

All governance fields appear in every file's YAML frontmatter and are REQUIRED (though several may carry empty values like `[]` or `{}`). The framework is unchanged from v0.1.0 except for the per-record audit-block addition documented in section 6.

## File-level governance fields

The frontmatter declares the governance values that apply to records in that file:

```yaml
sensitivity: internal
retention: standard
governance_frameworks: []
custom_governance: {}
```

When a file is read by a downstream system or governance scanner, these fields set the baseline for everything in the file.

The skill does not support per-record governance overrides via inline brackets. The v0.1 inline-bracket form (`[sensitivity: confidential]` after a bullet) is removed. Records that need divergent governance go in a separate file. This is a workshop-locked decision: per-record overrides were rarely used in production and added parsing complexity without operational benefit.

## The four fields

### `sensitivity`

Allowed values: `open`, `internal`, `confidential`, `restricted`.

| Value | Meaning |
|---|---|
| `open` | Public or shareable with no restrictions. |
| `internal` | Within the organization or within the operator's trusted circle. **Upstream default.** |
| `confidential` | Limited to specific people, teams, or contracts. |
| `restricted` | Highly sensitive; access strictly controlled (legal hold, board-level, regulated PII). |

The upstream default is `internal`. `org-config.md` can change the org-level default via `compliance.default_sensitivity` (per the schema in `config/org-config.md.template`). `user-config.md` can override per user via `privacy.default_sensitivity` (per `config/user-config.md.template`).

### `retention`

Allowed values: `standard`, `extended`, `indefinite`.

| Value | Meaning |
|---|---|
| `standard` | Default project retention. **Upstream default for active and entities files.** |
| `extended` | Long-term retention. |
| `indefinite` | Retain without expiry. **Upstream default for archive files.** |

The v0.1 values `legal_hold` and `delete_after_<period>` are removed in v0.4.0 (`schema_version: "0.2"`). Organizations that need those semantics document them via `custom_governance` instead. See `references/schema-changelog.md`.

The upstream skill does not delete or archive files based on this value; the metadata is for downstream systems.

### `governance_frameworks`

A list of framework names that apply to the file. Free-form. Common entries: `HIPAA`, `SOX`, `GDPR`, `CCPA`, `internal-IP`, `customer-PII`, `export-controlled`. Empty list `[]` by default.

The upstream skill does not validate framework names. `org-config.md` can supply an allowed list if the deploying organization wants strict tagging.

### `custom_governance`

A free-form key-value object for org-specific governance dimensions that do not fit the three fields above. Example:

```yaml
custom_governance:
  data_classification: "Crown Jewels"
  bcdr_tier: "tier-2"
  approver: "compliance@example.com"
```

Empty `{}` by default. Downstream systems consume whatever keys the org puts here.

## Defaults summary

The override columns below cite the actual config-template field paths. Consult `config/user-config.md.template` and `config/org-config.md.template` for the complete schemas; some frontmatter governance fields (`retention`, `custom_governance`) are not currently exposed as config-template override targets and must be set at file frontmatter or chat-time invocation.

| Field | Upstream default | Where to override |
|---|---|---|
| `sensitivity` | `internal` | File frontmatter; `org-config.md`'s `compliance.default_sensitivity`; `user-config.md`'s `privacy.default_sensitivity`. |
| `retention` (active, entities) | `standard` | File frontmatter; chat-time operator instruction. Not currently exposed in `org-config.md.template` or `user-config.md.template`; deferred to a future schema bump if operator demand surfaces. |
| `retention` (archive) | `indefinite` | File frontmatter; chat-time operator instruction. Same template-exposure caveat as above. |
| `governance_frameworks` | `[]` | File frontmatter; `org-config.md`'s `compliance.regulatory_scope` (rough analog: lists frameworks like `SOX`, `HIPAA`, `ITAR`). `user-config.md` does not expose an analog. |
| `custom_governance` | `{}` | File frontmatter; chat-time operator instruction. Not currently exposed in either config template; orgs that need custom keys document them via the `compliance` or `methodology_overrides` sections of `org-config.md` per their convention. |

## Resolution order

When governance values are determined for a generated file, apply this resolution order:

1. Upstream defaults from `references/defaults.md`.
2. `org-config.md` if present.
3. `user-config.md` if present.
4. Operator instructions in the current invocation.

Each later layer overrides earlier layers for the fields it declares. Layers do not require values for every field; unspecified fields inherit from the prior layer.

The full resolution order (including non-governance settings) is detailed in `references/defaults.md`.

## Per-record audit metadata (new in v0.4.0)

Every record carries an `audit` block independent of the governance framework. The audit block records HOW a record was approved and is not the same thing as governance metadata. See `references/schema.md` for the schema. Brief summary:

```yaml
audit:
  approval_mode: auto | manual | hybrid
  approved_by: <user id or null>
  approved_at: <ISO-8601>
  warning_response: acknowledged | passive | dismissed | n/a
  importance_source: llm-auto | user-override
```

The audit block exists so quality issues (especially from auto-mode) can be diagnosed and coached after the fact, not as a blame mechanism. Governance fields (`sensitivity` etc.) describe WHAT the record is. Audit fields describe HOW it got into the file. Both are required.

## What the skill does and does not do

**The skill does:**
- Capture file-level governance metadata.
- Capture per-record audit metadata.
- Apply file-level defaults from upstream, `org-config.md`, and `user-config.md` in resolution order.
- Carry `custom_governance` keys through unchanged so downstream systems can read them.

**The skill does not:**
- Call DLP, ACL, or compliance services.
- Encrypt or redact records based on `sensitivity`.
- Auto-delete files based on `retention`.
- Validate framework names.
- Block generation when governance fields carry their default values.

Integrations (DLP, ACL, retention enforcement) are a future workstream tracked in `ROADMAP.md`.
