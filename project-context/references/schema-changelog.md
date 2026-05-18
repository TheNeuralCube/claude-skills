---
file_role: skill-reference
topic: schema-changelog
current_schema_version: "0.2"
skill_version: "0.4.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Schema changelog (project-context)

This file is the version-by-version history of the **data schema** the project-context skill writes to disk. It is distinct from `CHANGELOG.md` (which tracks skill releases). The schema version (`schema_version` in every file's frontmatter) is decoupled from the skill version (`generated_by.version` in every file's frontmatter): the schema version bumps only when the shape of stored data changes, while the skill version bumps on any release.

The build session enforces a drift-detection guard. Before commit, the build compares `references/schema.md` against the prior tag's schema. If the schema has changed but `schema_version` is unchanged from the prior release, the build refuses to commit and surfaces the diff. The operator must either bump `schema_version` and add an entry here, or revert the schema change. See section "Build-time drift detection" below.

## Schema versions

### Schema "0.2" — current

- **Introduced:** 2026-05-18 (skill release v0.4.0).
- **Used by skill versions:** 0.4.0 and forward (until the next schema bump).
- **Carrier files:** every file the skill writes (`project-context.md`, `entities.md`, `project-context-archive.md`).
- **Schema_version literal on disk:** `schema_version: "0.2"` (short, quoted).

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

## Versioning policy

The skill version (`0.4.0`, `0.4.1`, ...) tracks releases. The schema version (`"0.2"`, `"0.3"`, ...) tracks the data-shape contract. A patch release (e.g., `0.4.1`) that fixes documentation without touching the schema still writes `schema_version: "0.2"`. A future minor release (e.g., `0.5.0`) that adds a new optional field bumps schema to `"0.3"` and adds an entry here.

Until skill v1.0.0, schema bumps are allowed but every bump must be documented here with field-level diffs and a migration path. After v1.0.0, schema changes are MAJOR-version bumps with explicit deprecation notices on prior fields.

This versioning convention is intended for cross-skill adoption. The forthcoming nc3-meta-skill-forge skill (working name; see project-context `ROADMAP.md`) will codify it as a standard pattern for all skills in the monorepo.
