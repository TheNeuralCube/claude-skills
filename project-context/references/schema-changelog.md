---
file_role: skill-reference
topic: schema-changelog
current_schema_version: "0.4"
skill_version: "0.6.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Schema changelog (project-context)

This file is the version-by-version history of the **data schema** the project-context skill writes to disk. It is distinct from `CHANGELOG.md` (which tracks skill releases). The schema version (`schema_version` in every file's frontmatter) is decoupled from the skill version (`generated_by.version` in every file's frontmatter): the schema version bumps only when the shape of stored data changes, while the skill version bumps on any release.

The build session enforces a drift-detection guard. Before commit, the build compares `references/schema.md` against the prior tag's schema. If the schema has changed but `schema_version` is unchanged from the prior release, the build refuses to commit and surfaces the diff. The operator must either bump `schema_version` and add an entry here, or revert the schema change. See section "Build-time drift detection" below.

## Schema versions

### Schema "0.4" — current

- **Introduced:** 2026-05-22 (skill release v0.6.0).
- **Used by skill versions:** 0.6.0 and forward (until the next schema bump).
- **Carrier files:** every file the skill writes (`project-context.md`, `entities.md`, `project-context-archive.md`).
- **Schema_version literal on disk:** `schema_version: "0.4"` (short, quoted).

**Field-level diff from schema "0.3":**

| Change | Detail |
|---|---|
| `topology` | New REQUIRED block in the frontmatter of all three files. Universal across all projects regardless of role. Contains: `role` (enum: `hub`, `spoke-dev`, `spoke-solution`, `standalone`, `unclassified`), `hub_reference` (string or null), `hub_version` (string or null), `last_hub_sync` (ISO 8601 or null), `parent` (string or null, for hybrid topology), `declared_by` (`operator` or `skill-default`), `declared_at` (ISO 8601). The full schema, role definitions, validation rules, and spoke inventory format live in `references/topology.md`. |

No other field-level changes from "0.3". All other schema mechanics (`_managed_by` field, `file_role`, `schema_version`, lifecycle fields, `id_prefix_legend`, audit block, archive `checkpoints` array, per-record schema, body section structure other than the new `## Spoke Inventory` section for Hub projects) carry forward unchanged.

**Body-section diff from schema "0.3":**

| Change | Detail |
|---|---|
| `## Spoke Inventory` (Hub projects only) | New section in the body of `project-context.md` immediately after frontmatter, present only when `topology.role: hub`. Markdown table with columns: Name, Role, Artifact Type, Source Hub Version, Status, Parent. Operator-maintained. The skill never auto-discovers spokes; the audit trigger refreshes the Status column at audit time but does not write the inventory itself (out of scope for v0.6.0). See `references/topology.md` section 3. |

**Migration path from "0.3":** automated, one-time per project, in-place upgrade (Scenario F). Pre-flight detects canonical filenames with `_managed_by: project-context-skill` and `schema_version: "0.3"` and no `topology` block; the operator confirms with `confirm v0.6.0 upgrade`; the skill rewrites the three files adding the `topology` block (with `role: "unclassified"` default and all relationship fields null) and changing `schema_version: "0.3"` → `schema_version: "0.4"`. All other content preserved unchanged. After the upgrade, the skill prompts the operator to declare topology role via the role-declaration prompt (`references/preflight.md` section 13.1). See `references/migration.md` section 10.

**Rationale:** schema "0.4" formalizes hub-spoke governance metadata as part of project identity. The 2026-05-21 hub-spoke governance workshop locked the federal-state model (decision V1 of the parent vision doc) with two-layer supremacy: HUB INHERITANCE BLOCK in spoke templates plus the Hub instructions attached file. v0.6.0 makes `project-context.md` the runtime store for the topology side of that model. The schema bump (0.3 → 0.4) accompanies the topology metadata work because the new REQUIRED `topology` block is backward-incompatible with the v0.3 file format. By semver convention, a schema bump with a new required block exceeds patch-release scope and triggers at least a minor version bump (hence v0.6.0 rather than v0.5.1).

The topology block enables three downstream behaviors in v0.6.0: (a) topology validation at pre-flight (per `references/preflight.md` section 10), (b) stale-spoke detection on spoke projects (section 11 of preflight), and (c) the audit trigger handler on Hub projects (section 12 of preflight). Two new informational verdicts (`⚠ Stale Spoke` and `⚠ Upgrade Available (v0.5.0 to v0.6.0)`) accompany the schema bump.

---

### Schema "0.3" — historical, still supported for upgrade migration

- **Introduced:** 2026-05-19 (skill release v0.5.0).
- **Used by skill versions:** 0.5.0 only.
- **Carrier files:** every file the skill writes (`project-context.md`, `entities.md`, `project-context-archive.md`).
- **Schema_version literal on disk:** `schema_version: "0.3"` (short, quoted).
- **v0.6.0 handling:** v0.6.0 detects schema "0.3" files (canonical filenames with `_managed_by: project-context-skill` AND `schema_version: "0.3"` AND no `topology` block) and offers an in-place Scenario F upgrade migration to "0.4" via the `confirm v0.6.0 upgrade` token path. The schema is not directly writable by v0.6.0 — v0.6.0 always writes "0.4".

**Field-level diff from schema "0.2":**

| Change | Detail |
|---|---|
| `_managed_by` | New REQUIRED string field in the frontmatter of all three files. Canonical value: `project-context-skill`. The leading underscore signals internal metadata, not user-facing data. The field is the registry marker that makes pre-flight detection reliable: `project_knowledge_search` for `_managed_by: project-context-skill` returns chunks where this distinctive YAML field actually appears, which is only in files under skill management. |

No other field-level changes from "0.2". All other schema mechanics (`file_role`, `schema_version`, `project`, `project_id`, lifecycle fields, `id_prefix_legend`, audit block, archive `checkpoints` array, per-record schema, body section structure) carry forward unchanged.

**Migration path from "0.2":** automated, one-time per project, in-place upgrade. Pre-flight detects canonical filenames with `schema_version: "0.2"` and no `_managed_by` field; the operator confirms with `confirm upgrade`; the skill rewrites the three files adding `_managed_by: project-context-skill` and changing `schema_version: "0.2"` → `schema_version: "0.3"`. All other content preserved unchanged. See `references/migration.md` section 9.

**Rationale:** schema "0.3" closes the protocol-enforcement gap documented in the 2026-05-19 postmortem. The pre-flight check in v0.4.0 was prose-described but not structurally enforced; under inference-time load, the model could skip pre-flight and write v0.1-era format records over a live v0.4.0 schema-0.2 system. v0.5.0 introduces a mandatory pre-flight protocol gated by SKILL.md's `## Protocol` section and a post-flight summary, both backed by reliable schema detection. The `_managed_by` field is the detection anchor: it is distinctive enough that `project_knowledge_search` returns only chunks from files under skill management, eliminating the false-positive problem the postmortem's broad-search approach would have suffered.

The schema bump (0.2 → 0.3) accompanies the protocol-enforcement work because the new REQUIRED field is backward-incompatible with the v0.2 file format. By semver convention, a schema bump with a new required field exceeds patch-release scope and triggers at least a minor version bump (hence v0.5.0 rather than v0.4.1). This release sets the precedent for future bumps.

---

### Schema "0.2" — historical, still supported for upgrade migration

- **Introduced:** 2026-05-18 (skill release v0.4.0).
- **Used by skill versions:** 0.4.0 only.
- **Carrier files:** every file the skill writes (`project-context.md`, `entities.md`, `project-context-archive.md`).
- **Schema_version literal on disk:** `schema_version: "0.2"` (short, quoted).
- **v0.5.0 handling:** v0.5.0 detects schema "0.2" files (canonical filenames with `schema_version: "0.2"` and no `_managed_by` field) and offers an in-place upgrade migration to "0.3" via the `confirm upgrade` token path. The schema is not directly writable by v0.5.0 — v0.5.0 always writes "0.3".

**Field-level diff from schema "0.1":**

| Change | Detail |
|---|---|
| File-set restructured | One dated file per session → three rolling-filename files (`project-context.md`, `entities.md`, `project-context-archive.md`). |
| Filename architecture | Dated filenames (`YYYY-MM-DD-project-context*.md`) replaced by rolling filenames; date lives in `last_merged` frontmatter. |
| `file_role` | New REQUIRED field replacing the old `file_type` / `file_subtype` pair. Values: `project-context`, `entities`, `archive`. |
| `project_id` | New REQUIRED kebab-case slug. |
| `update_count` | New REQUIRED monotonic integer per file. Drives update-based scoring decay (see `references/scoring.md`). |
| `record_count` | New REQUIRED integer. |
| `last_merged` | New REQUIRED ISO-8601 timestamp; replaces date-in-filename. |
| `read_order` | New REQUIRED list of section names, varies by `file_role`. |
| `how_to_read` | New REQUIRED multi-line plain-text reader instruction. |
| `id_prefix_legend` | New REQUIRED map of all eight ID prefixes (`dec`, `con`, `csn`, `opn`, `trm`, `ref`, `ent`, `arc`). Carried in every file so a reader has the legend regardless of which file is loaded. |
| `authors` | New REQUIRED list, currently `[]` (reserved for platform identity API). |
| `retention` allowed values | Reduced to `standard`, `extended`, `indefinite`. The old `legal_hold` and `delete_after_<period>` values are dropped in v0.2 — orgs that need those values document them via `custom_governance` instead. |
| Body section structure (active file) | Was 7 sections (Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot) → now 6 (Decisions, Constraints, Current State, Open Items, Terminology, External References). "Entities" moved to its own file. "State snapshot" renamed "Current State." |
| Body section structure (entities file) | New file with 5 sub-sections: People, Places, Things, Organizations, Datasets. |
| Body section structure (archive file) | One section `## Records`. Flat list; `status` field discriminates `superseded` vs `archived`. |
| Per-record schema | Completely overhauled. Removed inline `[tier]` / `[categories]` brackets. Added per-record `id`, lifecycle fields (`first_seen_update`, `last_seen_update`, `first_seen_at`, `last_seen_at`, `times_seen`), `importance` (1-10), `status`, provenance (`source_quote`, `source_kind`, `source_ref`), `links`, and the `audit` block. |
| Audit block | New REQUIRED per-record block: `approval_mode` (`auto`/`manual`/`hybrid`), `approved_by` (nullable), `approved_at`, `warning_response` (`acknowledged`/`passive`/`dismissed`/`n/a`), `importance_source` (`llm-auto`/`user-override`). |
| Three preservation tiers | Removed. Replaced by update-based scoring (see `references/scoring.md`) plus the five-op merge classifier (ADD/UPDATE/NOOP/DEMOTE/SUPERSEDE). |
| Inline category tags | Removed. Categories were open-vocabulary tags in v0.1; in v0.2 categorization is implicit in the section/file structure. |
| `consolidation_summary` | Removed. Replaced by archive `checkpoints` frontmatter array, which logs every merge (not only consolidation). |
| `checkpoints` (archive only) | New REQUIRED frontmatter array on archive files. Ordered list of per-merge checkpoint objects (`update`, `timestamp`, `summary`, `approver`). |
| Archive-record extra fields | New: `prior_id` (always), `superseded_by` + `superseded_at_update` (on `status: superseded`), `demoted_at_update` (on `status: archived`), optional `restore_command`. |

**Migration path from "0.1":** automated, one-time per project, initiated by pre-flight detection of legacy v0.1.x-v0.3.x dated files. See `references/migration.md` for the full algorithm.

**Rationale:** schema "0.2" supports the v0.4.0 three-file rolling architecture, the five-op merge classifier, update-based decay, and the audit trail required for the published auto-mode. These were the operational gaps in v0.1 (manual consolidation overhead, no decay model, no audit, no per-record provenance) that justified a major architectural pivot.

---

### Schema "0.1" — legacy (replaced)

- **Used by skill versions:** 0.1.0, 0.2.0, 0.3.0, 0.3.1, 0.3.2.
- **Carrier files:** dated single-file output (`YYYY-MM-DD-project-context[-{topic}].md` and `YYYY-MM-DD-project-context-consolidated[-N].md`).
- **Schema_version literal on disk — historical accident:** v0.1.0 through v0.3.2 wrote the **skill version** into the `schema_version` field as an unquoted YAML string (e.g., `schema_version: v0.1.0`, then `schema_version: v0.2.0`, then `schema_version: v0.3.2`). This was an artifact of schema versioning not being a separate concept in those releases — the field tracked the producing skill rather than the data shape. Effectively all of those releases shared the same data shape; the value of the field varied per release without any schema change. v0.4.0 establishes decoupled schema versioning and standardizes on the short quoted form (`schema_version: "0.2"`).
- **Migration detection** treats any value matching `v0.1.x`, `0.1.x`, `v0.2.x`, `0.2.x`, `v0.3.x`, `0.3.x` (quoted or unquoted, with or without the leading `v`) as "this is from the v0.1-era schema regardless of how it was serialized." See `references/migration.md` for the exact detection logic.

**Schema "0.1" field set (for migration reference):**

```yaml
file_type: project-context
file_subtype: fresh | consolidated
schema_version: <skill-version-string, see note above>
created: <ISO-8601>
project_name: <string>
session_topic: <string>
sessions_covered: [list]
source_files: [list]
related_session_recap: <filename or null>
related_files: [list]
sensitivity: open | internal | confidential | restricted    # default internal
audience: <free-form string>
retention: standard | extended | legal_hold | delete_after_<period>   # default standard
governance_frameworks: [list]
custom_governance: <object>
generated_by:
  skill: project-context
  version: <skill version>
  mode: generate | consolidate
  model: <model identifier>
  generation_date: <ISO-8601>
# consolidation_summary present on consolidated files only:
consolidation_summary:
  source_file_count: <integer>
  records_after_dedup: <integer>
  records_dropped_transient: <integer>
  records_compressed_summary: <integer>
```

**Body in schema "0.1":** seven sections in fixed order — Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot. Records were markdown bullets with inline metadata `[tier: full|summary|transient] [categories: tag1, tag2, ...]` and optional inline governance overrides.

## Supported Schemas

This release of the skill (v0.6.0) supports:

- **Read/write:** schema "0.4" (current). All v0.6.0 writes produce schema "0.4" with `_managed_by: project-context-skill` and a `topology` block in frontmatter (per `references/topology.md`).
- **Read for upgrade:** schema "0.3" (v0.5.0 format). Detection: canonical filenames + `_managed_by: project-context-skill` + `schema_version: "0.3"` + no `topology` block. Migration path: in-place Scenario F upgrade (add `topology` block with `role: "unclassified"` default, bump `schema_version` to "0.4", preserve content). Operator confirmation token: `confirm v0.6.0 upgrade`. See `references/migration.md` section 10.
- **Read for upgrade:** schema "0.2" (v0.4.0 format). Detection: canonical filenames + `schema_version: "0.2"` + no `_managed_by` field. Migration path: in-place Scenario E upgrade (add `_managed_by`, bump `schema_version` to "0.3", preserve content); operator re-invokes for Scenario F to reach "0.4". Operator confirmation token: `confirm upgrade`. See `references/migration.md` section 9.
- **Read for migration:** v0.1-era literals (`v0.1.0` unquoted, `"0.1"` quoted, and the broader regex `^"?v?0\.(1|2|3)(\.\d+)?"?$` covering v0.1.0–v0.3.2 historical writes — see "Schema '0.1'" below). Detection: legacy filename pattern OR legacy `schema_version` literal. Migration path: full Scenario D legacy migration. v0.6.0 preserves the v0.5.0 legacy migration algorithm (`references/migration.md` sections 3–8) verbatim; legacy migration produces schema "0.3" files, after which pre-flight routes through Scenario F to reach schema "0.4". Operator confirmation token: `confirm migration`. See `references/migration.md` section 3.
- **Refuse:** schemas newer than "0.4" (e.g., a hypothetical "0.5" produced by a future skill version). Verdict: `✗ MISMATCH: project newer than skill`. Operator path: upgrade the local skill copy. Override path exists (`override version mismatch and proceed`) but is marked NOT RECOMMENDED.
- **Refuse:** unrecognized `schema_version` values that match no documented pattern. Verdict: `✗ Mismatch: unknown schema` or `✗ Parse Error` depending on whether the value is a malformed literal or a syntactically valid but unknown one. Operator path: identify the file or override.
- **Refuse:** schema "0.4" files with no `topology` block (malformed v0.6.0 data, not legacy). Verdict: `✗ Parse Error` with topology diagnostic. See `references/migration.md` section 1 disambiguation notes.

The compatibility matrix is the authoritative input to pre-flight classification. See `references/preflight.md` for the algorithm that consumes this matrix and produces the operator-facing report block.

## Build-time drift detection

Every build session running on a v0.4.0+ release must run the drift-detection guard before commit:

1. Read `references/schema.md` from the working tree.
2. Read `references/schema.md` from the prior release tag (e.g., `project-context-v0.3.2` for the v0.4.0 build).
3. Compute the schema diff (added fields, removed fields, renamed fields, changed semantics).
4. Compare the current `schema_version` in `references/schema.md` against the prior tag's value.
5. **If schema diffs and `schema_version` is unchanged:** the build halts and surfaces the diff. The operator must either bump `schema_version` and add an entry to this file, or revert the schema change.
6. **If schema diffs and `schema_version` is bumped:** verify this file contains an entry for the new version covering every field-level change. If missing, halt.
7. **If schema is identical and `schema_version` is unchanged:** drift check passes.

This mechanism catches the "I forgot to bump" failure mode mechanically rather than relying on operator discipline. It also catches the inverse failure ("bumped without writing a changelog entry").

For the v0.4.0 build: the prior tag is `project-context-v0.3.2`. The schemas differ (everything listed above). `schema_version` bumps from the unquoted-skill-version form to `"0.2"`. This entry documents every field-level change. The guard passes.

For the v0.5.0 build: the prior tag is `project-context-v0.4.0`. The schemas differ by exactly one field (the new REQUIRED `_managed_by` in frontmatter). `schema_version` bumps from `"0.2"` to `"0.3"`. This file's schema "0.3" entry documents the field-level change. The guard passes.

For the v0.6.0 build: the prior tag is `project-context-v0.5.0`. The schemas differ by exactly one block (the new REQUIRED `topology` block in frontmatter, plus the new `## Spoke Inventory` body section for Hub projects). `schema_version` bumps from `"0.3"` to `"0.4"`. This file's schema "0.4" entry documents the block-level change. The guard passes.

## Versioning policy

The skill version (`0.4.0`, `0.5.0`, ...) tracks releases. The schema version (`"0.2"`, `"0.3"`, ...) tracks the data-shape contract. A patch release (e.g., `0.5.1`) that fixes documentation without touching the schema still writes `schema_version: "0.3"`. A future minor release that adds a new field bumps schema to `"0.4"` and adds an entry here.

**Schema bumps trigger at least a minor version bump.** v0.5.0 establishes this precedent: a schema bump with a new REQUIRED field is backward-incompatible with the prior file format and exceeds patch-release scope by semver convention. Future skills and future project-context versions should follow this pattern.

Until skill v1.0.0, schema bumps are allowed but every bump must be documented here with field-level diffs and a migration path. After v1.0.0, schema changes are MAJOR-version bumps with explicit deprecation notices on prior fields.

This versioning convention is intended for cross-skill adoption. The forthcoming nc3-meta-skill-forge skill (working name; see project-context `ROADMAP.md`) will codify it as a standard pattern for all skills in the monorepo. The `_managed_by` field introduced in schema "0.3" is implicitly a cross-skill convention from the moment v0.5.0 ships: other skills writing to project knowledge can use the same field shape with their own identifiers (`session-recap-skill`, `wellhead-skill`, etc.) to mark files they manage.
