---
file_role: skill-reference
topic: topology
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Topology (project-context v0.7.0)

The topology block and the `## Spoke Inventory` section are carried verbatim from schema 0.4 into schema 0.5; this file is unchanged in substance for v0.7.0. The only adjustment is that the managed context file is now named `pc-NNNN-context.md` (the active context file of the current generation) rather than `project-context.md`; references below use the `pc-NNNN-context.md` name.

This file is the authoritative specification for the topology metadata introduced in v0.6.0 (schema 0.4). Every project the skill manages has a topology relationship to other projects, and that relationship is part of the project's active state. Operations, pre-flight, and the audit trigger reference this file.

The first principle (P1) is: a project's topology relationship to other projects is part of its active state. v0.5.0 and earlier described what a project was about; v0.6.0 also describes how it relates to other projects.

## 1. Topology metadata schema

Lives in the YAML frontmatter of every file the skill writes (`pc-NNNN-context.md`, `pc-NNNN-entities.md`, `pc-NNNN-archive.md`). Required for schema 0.4.

```yaml
topology:
  role: "hub" | "spoke-dev" | "spoke-solution" | "standalone" | "unclassified"
  hub_reference: <string|null>
  hub_version: <string|null>
  last_hub_sync: <ISO 8601|null>
  parent: <string|null>
  declared_by: "operator" | "skill-default"
  declared_at: <ISO 8601>
```

Field definitions:

| Field | Type | Semantics |
|---|---|---|
| `role` | enum | Project's topology classification. One of the five role values defined in section 2. Required. |
| `hub_reference` | string or null | Human-readable name of the Hub project this spoke reports to. Populated for `spoke-*` only; null otherwise. |
| `hub_version` | string or null | The Hub instructions version the spoke declared (e.g., `"v0.9"`). Populated for `spoke-*` only; null otherwise. |
| `last_hub_sync` | ISO 8601 timestamp or null | When the spoke last reconciled against its Hub source. Populated for `spoke-*` only; null otherwise. |
| `parent` | string or null | Name of the parent spoke for hybrid topology (Solution > Skill). Null for direct-Hub spokes and non-spoke roles. |
| `declared_by` | enum | Who declared the role: `operator` (operator confirmed) or `skill-default` (skill defaulted on upgrade or migration). |
| `declared_at` | ISO 8601 timestamp | When the current role declaration was last written. Updated whenever the operator changes role or confirms an unclassified default. |

The schema is universal: every project carries a topology block regardless of role. The block is never absent from a schema 0.4 file.

## 2. Role definitions

Five role values are defined. The skill never invents a role; the operator declares, or the skill defaults to `unclassified` during upgrade.

### 2.1 `hub`

The canonical project that holds methodology, conventions, and posture for its dependents. Hub projects own a spoke inventory and do not themselves report to another Hub.

- `hub_reference`: null
- `hub_version`: null
- `last_hub_sync`: null
- `parent`: null
- Body of `pc-NNNN-context.md` includes a `## Spoke Inventory` section (see section 3).

### 2.2 `spoke-dev`

A skill development project. Inherits governance from a Hub. Examples: `Skill: project-context`, `Skill: session-recap`, `Skill: data-wellhead`.

- `hub_reference`: required, non-null (e.g., `"AI Engineering Hub"`)
- `hub_version`: required, non-null (e.g., `"v0.9"`)
- `last_hub_sync`: required, non-null (ISO 8601 timestamp)
- `parent`: null for direct-Hub spokes; populated when the dev spoke is a child of a Solution spoke in hybrid topology (e.g., `nc3-mt-sanitization` under `nc3-meeting-transcription`).

### 2.3 `spoke-solution`

A customer or internal solution project. Inherits governance from a Hub. May own child dev spokes. Examples: `nc3-meeting-transcription`, customer deliverable projects.

- `hub_reference`: required, non-null
- `hub_version`: required, non-null
- `last_hub_sync`: required, non-null
- `parent`: null (Solution spokes do not nest under other Solutions)

### 2.4 `standalone`

A project with no Hub relationship. The project does not inherit from a Hub and does not appear in a Hub's spoke inventory.

- `hub_reference`: null
- `hub_version`: null
- `last_hub_sync`: null
- `parent`: null

A standalone project is a legitimate, supported configuration. The skill does not pressure standalone projects to declare a Hub.

### 2.5 `unclassified`

Backward-compatibility default for projects upgrading from v0.5.0 (schema 0.3) to v0.6.0 (schema 0.4) via Scenario F. The skill writes `unclassified` when it cannot ask the operator (mid-write) and prompts the operator to declare a real role on the next invocation.

- All relationship fields null.
- `declared_by`: `"skill-default"` until the operator declares.
- Persistent: an unclassified project keeps operating normally; the skill re-prompts on each invocation until the operator declares.

`unclassified` is a transitional state, not a target state. The skill does not force a deadline for declaration.

## 3. Spoke inventory format (Hub projects only)

Required for `role: hub`. Lives in the body of `pc-NNNN-context.md` immediately after the YAML frontmatter and before any other body content. Format:

```markdown
## Spoke Inventory

| Name | Role | Artifact Type | Source Hub Version | Status | Parent |
|------|------|---------------|--------------------|--------|--------|
| <spoke name> | spoke-dev or spoke-solution | skill or project or other | v0.X | current or STALE | - or <parent name> |
```

Column definitions:

| Column | Semantics |
|---|---|
| `Name` | Human-readable identifier matching the spoke's Claude Project name. Skill spokes use the `Skill: <skill-artifact-name>` convention per Hub naming. |
| `Role` | `spoke-dev` or `spoke-solution`. Must match the spoke's own `topology.role`. |
| `Artifact Type` | `skill`, `project`, `org-deliverable`, or other Hub-recognized type. |
| `Source Hub Version` | The Hub version the spoke declared in its own `topology.hub_version`. |
| `Status` | `current` if `Source Hub Version` matches the Hub's current instructions version; `STALE` otherwise. Computed at audit-trigger invocation, not at every write. |
| `Parent` | Name of the parent spoke for hybrid topology (Solution > Skill); `-` for direct-Hub spokes. |

Section heading is exactly `## Spoke Inventory` (case-sensitive). The skill parses by exact heading match.

Empty spoke inventory: a Hub project with no spokes yet renders the section as heading plus column header row only, no data rows. Do not omit the section.

Sort order between writes is operator-maintained (most recently added first is the suggested convention but not enforced). The audit trigger re-sorts: STALE spokes alphabetical first, then current spokes alphabetical.

The spoke inventory is operator-maintained. The skill does not auto-discover spokes across tenants. When a new spoke is created (via project-creator skill in Workstream 3), the operator updates the Hub's inventory manually until cross-project automation is built.

## 4. Audit trigger semantics

A read-only trigger invokable in Hub projects only. Produces a staleness report comparing each spoke's `Source Hub Version` against the Hub's current instructions version.

### 4.1 Trigger phrases

The skill matches any of these phrases (case-insensitive, whitespace-tolerant):

- `audit spoke projects`
- `audit the spokes`
- `which spokes are stale`
- `show me spoke staleness`
- `spoke inventory audit`
- `run spoke audit`

### 4.2 Pre-flight gate

1. Pre-flight detects the audit trigger phrase.
2. Skill validates `topology.role == "hub"` in the current project's `pc-NNNN-context.md` frontmatter.
3. If role is not `hub`: skill refuses with the message "Audit trigger valid only in Hub projects" and exits the operation.
4. If role is `hub`: skill proceeds to audit execution.

### 4.3 Audit execution

1. Read the spoke inventory from the body of `pc-NNNN-context.md`.
2. Search project knowledge for files matching the pattern `ai-engineering-hub-instructions-v*.md`.
3. Parse the current Hub instructions version from the attached filename (e.g., `ai-engineering-hub-instructions-v0-9.md` parses to `v0.9`).
4. For each spoke row in the inventory:
   - Compare `Source Hub Version` against the parsed Hub instructions version.
   - If they match: `Status` = `current`.
   - If they differ: `Status` = `STALE`.
5. Compute the drift expression for STALE spokes (e.g., `4 minor versions behind`). Use semantic version arithmetic on the minor version when the major version matches; if major versions differ, report `major version drift`.
6. Sort: STALE spokes alphabetical, then current spokes alphabetical.
7. Emit the audit report block (format below).

### 4.4 Audit report block format

```markdown
## Spoke Audit Report

**Hub project:** <hub project name>
**Current Hub instructions version:** <parsed version>
**Audit date:** <ISO date>

### Stale spokes (N)

| Name | Role | At Version | Current | Drift |
|------|------|------------|---------|-------|
| <spoke name> | <role> | <source version> | <hub version> | <drift expression> |

### Current spokes (N)

| Name | Role | At Version |
|------|------|------------|
| <spoke name> | <role> | <source version> |

### Recommended action

Run the project-creator skill's upgrade mode against stale spokes when ready.
```

Implementation notes:

- Section headings are exact strings: `## Spoke Audit Report`, `### Stale spokes (N)`, `### Current spokes (N)`, `### Recommended action`. The `(N)` placeholder is replaced with the numeric count of rows in that section.
- Column widths render cleanly at approximately 80 character width (mobile-friendly). The skill does not pad to fixed column widths; markdown table rendering handles layout.
- If no stale spokes are found, emit the `### Stale spokes (0)` heading and the column header row only (no data rows). Same for `### Current spokes (0)` when applicable.
- If the Hub instructions file is absent, emit an informational note in place of `Current Hub instructions version`: `(Hub instructions file not attached; staleness comparison skipped)` and emit the spoke inventory rows without Status changes.

### 4.5 Audit is read-only

The audit trigger does not modify `pc-NNNN-context.md`. It does not write the updated Status column back to the spoke inventory. A future trigger (`refresh spoke inventory`, not yet implemented) will own write-back. The operator updates the Status column manually after reading the audit report if they want the inventory column to reflect the audit's findings.

The audit trigger does not invoke upgrades. The project-creator skill in Workstream 3 owns the upgrade flow.

### 4.6 Severity classification

The skill reports drift without severity classification. A spoke 4 minor versions behind and a spoke 1 minor version behind both render as `STALE` with their respective drift expressions. The operator decides priority.

A future release may add severity (e.g., critical, warning, info) based on Hub-defined thresholds. The skill does not pre-empt that design.

## 5. Hybrid topology rules

Hybrid topology is the federal-state governance pattern locked in the 2026-05-21 hub-spoke governance workshop (decision V3 of the parent vision doc). Three levels of nesting are supported:

```
Hub
├── spoke-dev (direct-Hub skill spoke)
├── spoke-solution (direct-Hub solution spoke)
│   └── spoke-dev (child skill spoke nested under a Solution)
```

The `parent` field on a child spoke's topology block names its immediate parent. For direct-Hub spokes, `parent` is null. For child spokes nested under a Solution, `parent` is the Solution's project name.

Examples:

- `Skill: project-context` is a direct-Hub spoke. `role: spoke-dev`, `parent: null`.
- `nc3-meeting-transcription` is a direct-Hub Solution spoke. `role: spoke-solution`, `parent: null`.
- `nc3-mt-sanitization` is a child Dev spoke under the Solution. `role: spoke-dev`, `parent: "nc3-meeting-transcription"`.

Rules:

- Only Solution spokes (`role: spoke-solution`) can be parents.
- Only Dev spokes (`role: spoke-dev`) can have a parent.
- Hub projects are never parents in the `topology.parent` sense; Hub appears as the ultimate ancestor via every spoke's `hub_reference`.
- Standalone projects are never parents and never have a parent.
- Nesting beyond Hub > Solution > Dev (e.g., Hub > Solution > Solution > Dev) is out of scope. If operator demand surfaces, a future release will reconsider.

In a Hub's spoke inventory, child spokes appear with their parent's name in the `Parent` column. The audit trigger treats child spokes the same as direct-Hub spokes for staleness comparison: each child spoke declares its own `hub_version`, and the audit compares that value against the Hub instructions version. The `parent` relationship is informational in the inventory; it does not change staleness math.

## 6. Validation rules

The skill enforces these rules at write time. Violations produce a Parse Error in pre-flight; the skill refuses to write a file with an invalid topology block.

### 6.1 Required-by-role fields

| Role | Required non-null fields | Required null fields |
|---|---|---|
| `hub` | (none) | `hub_reference`, `hub_version`, `last_hub_sync`, `parent` |
| `spoke-dev` | `hub_reference`, `hub_version`, `last_hub_sync` | (none; `parent` optional) |
| `spoke-solution` | `hub_reference`, `hub_version`, `last_hub_sync` | `parent` |
| `standalone` | (none) | `hub_reference`, `hub_version`, `last_hub_sync`, `parent` |
| `unclassified` | (none) | (none; all relationship fields permitted null) |

`role`, `declared_by`, and `declared_at` are always required and non-null regardless of role.

### 6.2 No-empty-fields principle

Every field in the topology block must have one of:

- A confident value (e.g., `role: hub`, `hub_reference: "AI Engineering Hub"`).
- An explicit `null` (where the role permits or requires null per section 6.1).
- An explicit placeholder like `[tbd]` (permitted only in template files, not in active project files).

A literally empty field (e.g., `hub_reference:` with no value) is a Parse Error. The skill emits: "Topology field `<field>` is empty; expected confident value, explicit placeholder, or null with reason."

### 6.3 Role-value validation

`role` must be one of the five enum values: `hub`, `spoke-dev`, `spoke-solution`, `standalone`, `unclassified`. Any other value is a Parse Error.

The skill is case-sensitive on role values (lowercase only). `Hub`, `HUB`, `Spoke-Dev`, etc. are Parse Errors.

### 6.4 ISO 8601 validation

`last_hub_sync` and `declared_at`, when non-null, must parse as ISO 8601 timestamps. Date-only strings (`YYYY-MM-DD`) are accepted as shorthand for midnight UTC of that date. Non-parseable strings are Parse Errors.

### 6.5 declared_by validation

`declared_by` must be one of: `operator`, `skill-default`. Any other value is a Parse Error.

When the operator declares a role (whether on fresh project, after Scenario F, or via re-declaration), the skill writes `declared_by: "operator"` and stamps `declared_at` with the current ISO 8601 timestamp.

When the skill defaults a role (only on Scenario F upgrade, where the operator has not yet been asked), the skill writes `declared_by: "skill-default"` and stamps `declared_at` with the upgrade timestamp.

### 6.6 Hub-reference / spoke-inventory consistency

The skill does not enforce bidirectional consistency between a spoke's `hub_reference` and the Hub project's spoke inventory. The spoke inventory is operator-maintained (per section 3); the skill writes the spoke side correctly but does not auto-update the Hub side. Inconsistency between the two surfaces is an operator-maintenance concern and is surfaced (not silently fixed) by the audit trigger.

## 7. Cross-references

| Document | Relationship |
|---|---|
| `references/schema.md` | Schema 0.4 frontmatter includes the topology block defined here |
| `references/preflight.md` | Pre-flight reads topology to detect Scenario F upgrade need, stale-spoke verdicts, and audit-trigger gating |
| `references/migration.md` | Scenario F migration writes the topology block with unclassified defaults |
| `references/schema-changelog.md` | Schema 0.4 entry references this file as the topology specification |
| `SKILL.md` | Audit trigger phrases registered in the trigger surface; routes through this file's semantics |
