---
file_role: skill-reference
topic: schema-changelog
current_schema_version: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Schema changelog (session-handoff)

This file is the version-by-version history of the **metadata contract** the session-handoff skill writes to disk. It is distinct from `CHANGELOG.md` (which tracks skill releases). The schema version (`schema_version` in every handoff's frontmatter) is decoupled from the skill version (`skill_version`): the schema version bumps only when the shape of the contract changes, the skill version bumps on every release.

State this decoupling loudly: the skill ships at v0.1.0 and the schema ships at "0.1" by coincidence, not by coupling. A future patch release (e.g. v0.1.1) that fixes documentation without touching the contract still writes `schema_version: "0.1"`. A future release that adds a required field bumps the schema to "0.2" and adds an entry here.

retrofit reads this file's Supported Schemas matrix for schema-version detection.

## Schema versions

### Schema "0.1" - current (inception)

- **Introduced:** 2026-06-02 (skill release v0.1.0).
- **Used by skill versions:** 0.1.0 and forward (until the next schema bump).
- **Carrier files:** every handoff the skill writes, plus the config and manifest files the skill writes (which carry `schema_version` and `_managed_by` in their own frontmatter).
- **Schema_version literal on disk:** `schema_version: "0.1"` (short, quoted).

**Why a fresh 0.1 rather than inheriting a v1.5 schema version.** session-handoff is the public-ized successor to an internal predecessor skill (v1.5; credited in `CHANGELOG.md`). The generate and retrofit cores are mature and carry forward, but the contract is substantially reworked for the public release:

| Change from the v1.5 schema | Detail |
|---|---|
| Two-tier frontmatter | A tight versioned metadata contract (owned by `references/schema.md`) is separated from a mode-coupled resumption payload (owned by the mode files). v1.5 had a single flat frontmatter. |
| `_managed_by: session-handoff-skill` | New registry marker, mirroring the project-context `-skill` suffix convention, so pre-flight detects prior handoffs reliably. |
| Self-contained lineage | `handoff_id`, `handoff_version`, `supersedes`, `prior_handoffs`, `consolidation_depth`, `derivative_of` are all defined in-contract. The predecessor's external lookup table is removed; all identity lives in-document. The `HND` prefix replaces the predecessor's id prefix. |
| `governance` block | `sensitivity` (kept from v1.5) is now nested under a governance block with `retention`, `governance_frameworks`, and `custom_governance`. |
| `generated_by` and `audit` blocks | New. Provenance (how it was made, system-inferred) and audit (who vouched, self-asserted) are separate blocks. The two honesty guardrails are stated in `references/schema.md` section 4.1. |
| Brand-free strip | v1.5 fields `aspect`, `confidence`, `last_verified`, `thread_chain`, `vault_path`, `parent_moc`, `aliases`, `related_notes`, `life_domains` are removed from the core and move to a separately-packaged org-config profile. `source_session_type` folds under `generated_by`. |

Because the contract gains unproven fields (the audit block and the consolidation ledger), a fresh "0.1" is the honest version stamp. There is no migration path from the v1.5 schema in the public artifact; older internal files are migrated by the separately-packaged org-specific variant, not by the public skill.

**Migration path from prior schemas:** none in the public artifact. v0.1.0 reads and writes "0.1" only. retrofit (`modes/retrofit.md`) exists to upgrade **future** stale-schema handoffs once later schema versions ship; at inception there is no older public schema to upgrade from.

## Supported Schemas

This release of the skill (v0.1.0) supports:

- **Read/write:** schema "0.1" (current). All v0.1.0 writes produce schema "0.1" with `_managed_by: session-handoff-skill`, a two-tier frontmatter, and the governance, generated_by, and audit blocks.
- **Read for retrofit:** none yet. retrofit is implemented, but at inception there is no older public schema to upgrade from, so the retrofit path and the update-on-stale path are **genesis-untestable**: they cannot be exercised end-to-end until a prior public schema ships. This is expected for a genesis release and is not a release blocker; the mechanism is in place and becomes testable at the first future schema bump. Tracked in `ROADMAP.md` under Deferred verification.
- **Refuse:** schemas newer than "0.1" (e.g. a hypothetical "0.2" produced by a future skill version). Verdict: `✗ Mismatch and refuse: project newer than skill`. The skill reveals the expected schema and refuses to write. See `references/preflight.md`.
- **Refuse:** unrecognized `schema_version` values that match no documented pattern. Verdict: `✗ Parse Error` or `✗ Mismatch and refuse` depending on whether the value is malformed or syntactically valid but unknown.

The compatibility matrix is the authoritative input to pre-flight classification. See `references/preflight.md` for the algorithm that consumes this matrix and produces the operator-facing report block.

## Build-time drift detection (forward-looking)

From the next release onward, the build session should run a drift-detection guard before commit, mirroring the benchmark:

1. Read `references/schema.md` from the working tree.
2. Read `references/schema.md` from the prior release tag (`session-handoff-v0.1.0` for the next build).
3. Compute the contract diff (added, removed, renamed fields; changed semantics).
4. Compare the current `schema_version` against the prior tag's value.
5. If the contract diffs and `schema_version` is unchanged: halt and surface the diff. Either bump `schema_version` and add an entry here, or revert the change.
6. If the contract diffs and `schema_version` is bumped: verify this file has an entry for the new version covering every field-level change. If missing, halt.
7. If the contract is identical and `schema_version` is unchanged: the guard passes.

At inception (v0.1.0) there is no prior tag, so the guard is a no-op for this build. It activates at the next release.

## Versioning policy

The skill version (`0.1.0`, `0.2.0`, ...) tracks releases. The schema version (`"0.1"`, `"0.2"`, ...) tracks the contract. A patch release that fixes docs without touching the contract keeps the schema version. A schema bump that adds a required field is backward-incompatible with the prior contract and exceeds patch-release scope by semver convention, so it triggers at least a minor version bump.

Until skill v1.0.0, schema bumps are allowed but every bump must be documented here with field-level diffs and a retrofit path. The skill stays at 0.x until update, consolidate, and share-sanitize are proven; the generate and retrofit cores are mature (carried from v1.5) but the three new modes are unproven, so v1.0.0 is not yet earned.

This decoupled-versioning convention and the `_managed_by` registry-marker convention are shared with the sister skill project-context.
