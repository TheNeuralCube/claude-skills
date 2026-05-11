<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Governance metadata framework

The project-context skill ships a governance metadata framework so that records and files can carry the policy attributes enterprise environments care about (sensitivity, audience, retention, applicable frameworks). The framework is **a schema**, not an integration. v0.1.0 does not call DLP services, does not enforce retention, and does not apply ACLs. It captures the metadata so downstream systems and future skill versions can act on it.

All governance fields are **optional**. Every output is valid even when no governance field is set.

## Two layers: file-level defaults and per-item overrides

### File-level defaults

The frontmatter declares default governance values that apply to every record in the file unless a record overrides them:

```yaml
sensitivity: internal
audience: ""
retention: standard
governance_frameworks: []
custom_governance: {}
```

When a file is read by a downstream session or governance scanner, file-level defaults set the baseline. A file marked `sensitivity: internal` is treated as internal; only records that declare an override deviate from that.

### Per-item overrides

When a single record diverges from the file-level baseline, the divergence is declared inline:

```markdown
- Customer-level revenue figures are confidential. [categories: governance, finance] [sensitivity: confidential]
```

The inline `[sensitivity: confidential]` bracket overrides the file-level `sensitivity: internal` for this record only. Other records in the file continue to inherit the file-level default.

Any of the file-level governance fields may be overridden inline. Inline brackets always carry one field per bracket pair.

## The five fields

### `sensitivity`

Allowed values: `open`, `internal`, `confidential`, `restricted`.

| Value | Meaning |
|---|---|
| `open` | Public or shareable with no restrictions. |
| `internal` | Within the organization or within the operator's trusted circle. **Upstream default.** |
| `confidential` | Limited to specific people, teams, or contracts. |
| `restricted` | Highly sensitive; access strictly controlled (e.g., legal hold material, board-level information, regulated PII). |

The upstream default is `internal`. Org-config can change the default via `defaults.sensitivity`.

### `audience`

Free-form string. Common values: `team`, `leadership`, `legal`, `compliance`, `engineering`, `external-partners`, `vendor`, `customer`. Empty by default.

Org-config can constrain to a vocabulary by listing allowed values. The upstream skill does not enforce a vocabulary.

### `retention`

Allowed values: `standard`, `extended`, `legal_hold`, `delete_after_<period>` (e.g., `delete_after_30d`, `delete_after_180d`, `delete_after_1y`).

| Value | Typical mapping (org-config defines actual durations) |
|---|---|
| `standard` | Default project retention (often 12 months). **Upstream default.** |
| `extended` | Long-term retention (often 5 years). |
| `legal_hold` | Indefinite; do not delete without legal sign-off. |
| `delete_after_<period>` | Explicit deletion target. |

The upstream skill does not delete or archive anything; the metadata is for downstream systems.

### `governance_frameworks`

A list of framework names that apply to the record or file. Free-form. Common entries: `HIPAA`, `SOX`, `GDPR`, `CCPA`, `internal-IP`, `customer-PII`, `export-controlled`. Empty by default.

The upstream skill does not validate framework names. Org-config can supply an allowed list if the deploying organization wants strict tagging.

### `custom_governance`

A free-form key-value object for org-specific governance dimensions that do not fit the four fields above. Examples:

```yaml
custom_governance:
  data_classification: "Crown Jewels"
  bcdr_tier: "tier-2"
  approver: "compliance@example.com"
```

Inline overrides for `custom_governance` keys use the same per-bracket form:

```markdown
- <record content>. [categories: legal] [custom_governance.bcdr_tier: tier-1]
```

## Worked example

A file-level frontmatter declares:

```yaml
sensitivity: internal
audience: ""
retention: standard
governance_frameworks: [internal-IP]
custom_governance: {}
```

The body contains:

```markdown
## Decisions

- Adopt the four-segment customer model. [categories: customer, strategy]
- Customer-level revenue figures are confidential; aggregate figures are internal. [categories: governance, finance] [sensitivity: confidential]
- Pricing methodology is restricted to the deal team. [categories: pricing, governance] [sensitivity: restricted] [audience: deal-team]
```

Reading rules a downstream system applies:

- The first record inherits everything from the file-level frontmatter: `internal` sensitivity, no audience, `standard` retention, `internal-IP` framework.
- The second record overrides only sensitivity to `confidential`. Other fields still inherit.
- The third record overrides sensitivity to `restricted` and adds an audience of `deal-team`. Retention and frameworks still inherit.

## Defaults summary

| Field | Upstream default | Where to override |
|---|---|---|
| `sensitivity` | `internal` | File frontmatter; per-record inline; org-config `defaults.sensitivity`. |
| `audience` | empty | File frontmatter; per-record inline; org-config `defaults.audience`. |
| `retention` | `standard` | File frontmatter; per-record inline; org-config `defaults.retention`. |
| `governance_frameworks` | `[]` | File frontmatter; per-record inline; org-config `defaults.governance_frameworks`. |
| `custom_governance` | `{}` | File frontmatter; per-record inline; org-config does not have a dedicated default but can set values via custom org-config sections. |

## Resolution order

When governance values are determined for a generated file or record, apply this resolution order:

1. Upstream defaults from this skill.
2. Organization defaults from `org-config.md`, if present.
3. Operator instructions in the current invocation.
4. Record-level inline overrides for specific records.

Each later layer overrides earlier layers for the specific fields it declares. Layers do not require values for every field; unspecified fields inherit from the prior layer.

## What v0.1.0 does and does not do

**v0.1.0 does:**
- Capture governance metadata at file and record level.
- Apply file-level defaults to records that do not declare overrides.
- Allow per-record overrides on any governance field.
- Allow org-config.md to change file-level defaults at deployment time.
- Carry `custom_governance` keys through unchanged so downstream systems can read them.

**v0.1.0 does not:**
- Call DLP, ACL, or compliance services.
- Encrypt or redact records based on `sensitivity`.
- Auto-delete files based on `retention`.
- Validate that framework names are real frameworks.
- Block generation when governance fields are absent or unusual.

The framework is the deliverable. Integrations are a v0.2.0+ workstream.
