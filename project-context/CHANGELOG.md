<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to the project-context skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The skill version (e.g., `0.5.0`) tracks releases. Beginning with v0.4.0, the **schema version** (`schema_version` in every file's frontmatter) is **decoupled** from the skill version. The schema version bumps only when the shape of stored data changes; the skill version bumps on every release. See `references/schema-changelog.md` for the version-by-version history of the data schema.

## [0.5.0] — 2026-05-19

### Added
- **Mandatory pre-flight protocol (`## Protocol` section in SKILL.md).** Pre-flight is now a structural gate: SKILL.md's `## Protocol` is the first content after frontmatter, the model cannot reach operational content without passing through it, and the model must emit a pre-flight report block as the first content of every response before any generation. The protocol cites `references/preflight.md` as the authoritative source. Failure to complete pre-flight before generation is a protocol violation, not an optimization. Anti-rationalization clause is model-facing: operator urgency or perceived urgency does not license skipping pre-flight.
- **`references/preflight.md` (new file).** Authoritative specification for the pre-flight protocol and the symmetric post-flight summary. Contains: purpose (closing the postmortem-documented enforcement gap), first principle (project state is authoritative), pre-flight algorithm (three-tier `project_knowledge_search` strategy + six-step classification), pre-flight report block format with verdict glyphs `✓ ⚠ ✗`, scenario examples (A Fresh, B Matched, C Skill-too-old, D Legacy, E v0.4.0 Upgrade), confirmation token catalog, token matching rules, token mismatch error format, pre-flight completion criteria, infrastructure-failure handling, and post-flight summary specification.
- **Schema "0.3" with new REQUIRED `_managed_by: project-context-skill` field.** Frontmatter of all three files (`project-context.md`, `entities.md`, `project-context-archive.md`) carries this field. The leading underscore signals internal metadata, not user-facing data. The field is the registry marker that makes pre-flight detection reliable: `project_knowledge_search` for `_managed_by: project-context-skill` returns chunks where this distinctive YAML field actually appears, which is only in files under skill management. Schema bump 0.2 → 0.3. `references/schema-changelog.md` documents the field-level diff and the new "Supported Schemas" matrix.
- **Upgrade migration (v0.4.0 → v0.5.0).** New migration path: pre-flight detects canonical filenames with `schema_version: "0.2"` and no `_managed_by`, emits verdict `⚠ Upgrade Available`, and after `confirm upgrade` rewrites the three files adding `_managed_by` and bumping `schema_version` to `"0.3"`. All record content preserved verbatim — frontmatter-only modification. See `references/migration.md` section 9. Operator brief uses the download-and-replace pattern (no legacy-file deletion because filenames are unchanged).
- **Post-flight summary block.** Symmetric closing block to pre-flight: same verdict-glyph convention, same skippability-is-a-violation rule. Reports what was actually written, schema version, skill version, operation performed (with deviation note if execution diverged from pre-flight's proposal), and operator action required. Failure cases emit `✗ Failed` post-flight with diagnostic. Specification in `references/preflight.md` section 9.
- **Pre-flight prerequisite gating notes** at the top of each `operations/*.md` file (`default.md`, `merge_external.md`, `compact.md`, `rebuild.md`). Redundancy is intentional: the model encounters the gating signal both at SKILL.md entry and at each operation file's entry, so operations cannot be misread as standalone instructions.
- **Two new pre-flight verdicts:** `⚠ Upgrade Available` (v0.4.0 → v0.5.0 upgrade scenario) and `✗ Infrastructure Failure` (`project_knowledge_search` errored). Infrastructure failure does NOT default to assuming-fresh; the project may have state we cannot see.
- **"Supported Schemas" section** in `references/schema-changelog.md`. Authoritative compatibility matrix listing what v0.5.0 reads, writes, migrates from, and refuses. Pre-flight cites this matrix when classifying project state.
- **`USAGE.md` "Upgrading from v0.4.0" section.** Operator-facing walkthrough of the upgrade migration scenario, including the `confirm upgrade` token and the no-legacy-deletion flow.

### Changed
- **`references/migration.md` retargeted to schema "0.3".** Legacy migration (v0.1-era → current) now produces schema "0.3" files with `_managed_by` instead of schema "0.2" files; operators with v0.1-era projects skip schema "0.2" entirely. Detection logic refactored from two-step to four-branch (CURRENT, UPGRADE_AVAILABLE, LEGACY, UNKNOWN) with `_managed_by` as the explicit disambiguator. The existing legacy regex `^"?v?0\.(1|2|3)(\.\d+)?"?$` is preserved verbatim from v0.4.0 — broader pattern coverage including v0.2.0-shaped legacy literals — but its evaluation is now downstream of the new step-1 and step-2 branches.
- **`references/schema.md` updated to schema "0.3".** New required field `_managed_by` added to frontmatter definition; validation checklist updated (rule 2 becomes `schema_version` exactly `"0.3"`; new rule 3 requires `_managed_by: project-context-skill`).
- **`references/schema-changelog.md` adds schema "0.3" entry.** New top entry above schema "0.2" with field-level diff and rationale; schema "0.2" demoted to historical-but-supported (for upgrade migration); new "Supported Schemas" section added.
- **`SKILL.md` "Pre-flight check (common prologue)" section renamed and reduced to "Pre-flight surface guard".** Per Q2 outcome: the section now preserves the surface-guard text inline (it can terminate the operation before any `project_knowledge_search` is issued) and defers protocol-enforcement content to `references/preflight.md`. The post-surface-guard runtime steps (project detection, conflict detection, migration trigger, configuration resolution) are described in `references/operations.md` section 4. The "common prologue" label retired because that implied multi-step pre-flight content that no longer lives in SKILL.md.
- **`references/operations.md` section 4 updated with pointer note** deferring protocol-enforcement authority to `references/preflight.md`. Per Q1 outcome: inventory categorized the seven steps as (a) surface guard / operator-facing surface text (stays), (b) project detection / conflict detection / migration trigger handling / configuration resolution / post-pre-flight runtime (stays), (c) file discovery / schema verification (defers to preflight.md's three-tier search and four-branch classification). Step 3 was condensed to a deferral to preflight.md; step 4 is now reserved. Steps 1, 2, 5, 6, 7 remain meaningful as operation-side concerns post-pre-flight.
- **Example files in `references/examples/`** updated to schema "0.3" frontmatter: `example-project-context.md`, `example-entities.md`, `example-project-context-archive.md` now carry `_managed_by: project-context-skill` and `schema_version: "0.3"`; `generated_by.version` bumped to `"0.5.0"`. Record content unchanged.
- **Stale-reference sweep applied across the unchanged-files bucket.** Doc-accuracy updates to current-state references (e.g., `schema_version: "0.2"` → `"0.3"`, `v0.4.0` → `v0.5.0`, "in v0.4.0" → "in v0.5.0") in `USAGE.md`, `references/defaults.md`, `references/governance.md`, `references/scoring.md`, `references/user-config-template.md`, `references/org-config-template.md`, and `references/examples/example-user-config.md`. Historical references (when the field was added, when the schema bumped, fictional record content in example files) preserved unchanged. Two forward references genericized: `governance.md` line 125 "v0.5.0+ workstream" → "future workstream"; `org-config-template.md` line 128 "v0.5.0+ feature request" → "future-release feature request" (the v0.5.0+ phrasing was forward-looking from v0.4.0's perspective and would have re-staled at v0.5.0 ship).
- **`SKILL.md` frontmatter version `0.4.0` → `0.5.0`.** Description preserves all 19 v0.1.0 trigger phrases verbatim plus the v0.4.0 additions; only the version token `v0.4.0` → `v0.5.0` changes. Final byte count: 942 chars, well within the 1024-byte limit.

### Migration
- **Two migration paths in v0.5.0:**
  - Legacy migration (v0.1-era → schema "0.3"): existing v0.4.0 logic retargeted to produce schema "0.3" output directly. Operator confirmation token: `confirm migration`. Brief uses the `download → verify → delete old → upload new` pattern with exact filenames listed.
  - Upgrade migration (schema "0.2" → schema "0.3"): NEW. Frontmatter-only rewrite. Operator confirmation token: `confirm upgrade`. Brief uses the download-and-replace pattern (no legacy deletion).

### Notes
- **Schema bump triggers minor version bump precedent.** v0.5.0 establishes that schema changes — even single-field additions — exceed patch-release scope by semver convention and warrant at least a minor version bump. Future schema bumps should follow this pattern. See `references/schema-changelog.md` Versioning policy section.
- **`_managed_by` field implicitly establishes a cross-skill convention.** Other skills writing to project knowledge may use the same field shape with their own identifiers (`session-recap-skill`, `wellhead-skill`, etc.). Formalization deferred to the future nc3-meta-skill-forge skill.
- **The 2026-05-19 postmortem** (`2026-05-19-postmortem-project-context-skill-schema-mismatch.md` in the v0.5.0 build inputs) is the release trigger. Five Priority-1 and Priority-2 action items map to v0.5.0 changes: AI-01 (structural gate via `## Protocol`), AI-02 (required pre-flight report block), AI-03 (version-compatibility check), AI-04 (registry marker as `_managed_by` field), AI-05 (confirmation token requirement on existing-system detection), AI-06 (anti-rationalization language, promoted from P3 to embedded in Protocol section), AI-08 (post-flight summary). AI-07 documented across schema-changelog.md and preflight.md. AI-09 and AI-10 explicitly deferred per design spec §16.

## [0.4.0] — 2026-05-18

### Added
- **Three-file rolling architecture.** Output is now three files with rolling filenames: `project-context.md` (active grounding file), `entities.md` (stable reference data), `project-context-archive.md` (append-only history). Date lives in the `last_merged` frontmatter, not in the filename. Files are eagerly created on first invocation with HTML-comment-delimited placeholder blocks that the skill removes on first record write.
- **Four named operations** replacing the two modes. `default` (parse conversation, classify, propose, write), `merge_external` (same flow on an attached file), `compact` (batch-demote weak records), `rebuild` (regenerate active file from archive; mandatory pre-commit review). See `operations/`.
- **Five-op merge classifier.** ADD, UPDATE, NOOP, DEMOTE, SUPERSEDE — Mem0-style four plus the operator's DEMOTE extension. Classifier pseudocode lives in `references/operations.md`.
- **Hybrid brake** (default `merge_policy`). Auto-apply ADD and NOOP; gate UPDATE, DEMOTE, SUPERSEDE for operator approval. Alternative policies: `gate` (require approval on every change), `auto` (auto-approve everything, with mandatory warning and full audit trail).
- **Update-based scoring algorithm** with 6 tunable coefficients (`alpha`, `beta`, `gamma`, `delta`, `epsilon`, `lambda`) and a default `demotion_threshold` of 5. Decay is measured in file updates, not calendar time — a project untouched for six months sees zero decay. Formula and worked examples in `references/scoring.md`.
- **Auto-mode** shipped as a published option. Mandatory per-session warning matches design spec §12.3 verbatim. Every auto-approved record carries `audit.approval_mode: auto` and a visible `[AUTO]` prefix on `content`. Audit metadata enables coaching and quality diagnosis after the fact.
- **Per-record audit block.** Every record has `audit.approval_mode`, `audit.approved_by` (nullable in v0.4.0), `audit.approved_at`, `audit.warning_response`, `audit.importance_source`.
- **Three-layer configuration.** `user-config.md` (new in v0.4.0) > `org-config.md` > skill defaults from `references/defaults.md`. The `user-config.md` convention is intended as cross-skill: future skills in the monorepo adopt the same pattern. See `references/user-config-template.md`.
- **Decoupled schema versioning** plus `references/schema-changelog.md`. Schema is now `"0.2"` (the short, quoted form). The build session enforces a drift-detection guard against the prior tag.
- **`id_prefix_legend`** REQUIRED frontmatter map carried in every file the skill writes. Eight ID prefixes: `dec`, `con`, `csn`, `opn`, `trm`, `ref`, `ent`, `arc`.
- **Archive `checkpoints` array** in YAML frontmatter (not body). Per-merge log of what changed each update.
- **Migration** from v0.1.x-v0.3.x dated files. Automated, one-time, non-destructive. Operator brief lists each legacy file by exact filename with required order of operations (download new → verify → delete old → upload new). See `references/migration.md`.
- **ROADMAP.md** and **USAGE.md** added to the per-skill file set.

### Changed
- **Body sections** for the active file: was 7 (Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot) → now 6 (Decisions, Constraints, Current State, Open Items, Terminology, External References). "Entities" moved to its own file. "State snapshot" renamed "Current State."
- **Per-record format** rewritten. The v0.1 inline-bracket metadata (`[tier: full | summary | transient] [categories: tag1, tag2]`) is gone. Records now carry structured per-record YAML with lifecycle, scoring, status, provenance, links, and audit blocks.
- **Three preservation tiers** (`full`, `summary`, `transient`) are removed. Update-based scoring plus the merge classifier replaces them. Migration translates legacy `full` → `importance: 8`, `summary` → `importance: 5`, drops `transient`.
- **Open category tags** are removed. Categorization is implicit in the section/file structure.
- **Filename convention.** Dated filenames retired in favor of rolling filenames. The date now lives in `last_merged` frontmatter.
- **`schema_version` field.** Bumped from the unquoted-skill-version form used by v0.1.0-v0.3.2 (e.g., `schema_version: v0.1.0`, `schema_version: v0.3.2`) to the short, quoted, decoupled form `schema_version: "0.2"`. The shift to a decoupled scheme is documented in `references/schema-changelog.md`.
- **`retention` allowed values.** Reduced to `standard | extended | indefinite`. The v0.1 values `legal_hold` and `delete_after_<period>` are removed; organizations document those semantics via `custom_governance` instead.
- **Per-record governance overrides** (inline brackets) are removed. Records that need divergent governance go in a separate file.
- **`modes/` directory** removed; replaced by `operations/`.
- **`SKILL.md`** rewritten as a thin router with surface guard + pre-flight + routing to four operation files. All 19 v0.1.0 trigger phrases preserved verbatim in the description; new v0.4.0 phrases added for compact, rebuild, and merge_external.
- **README.md** rewritten for the three-file architecture and four operations.

### Removed
- `modes/generate.md` and `modes/consolidate.md` (replaced by `operations/`).
- `references/examples/example-fresh-project-context.md` and `references/examples/example-consolidated-project-context.md` (replaced by four v0.4.0 examples covering active, entities, archive, and user-config).
- Inline per-record `[tier: ...]`, `[categories: ...]`, and inline-governance bracket syntax.
- `consolidation_summary` frontmatter block (replaced by archive `checkpoints` array).

### Notes
- **Model-assumption disclosure** in SKILL.md: this skill is optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking). Active-file token budgets (target 30K, soft warning 50K, hard ceiling 80K) assume substantial effective context. On lighter models, data integrity may degrade as files approach the hard ceiling.
- **Operator-attribution-on-generated-SPDX flag** carried since v0.1.0 was resolved in v0.3.2 (no SPDX on generated outputs) and remains resolved. v0.4.0 example files in `references/examples/` follow the no-SPDX rule. Skill source files carry Apache 2.0 SPDX headers as before.
- **`user-config.md` cross-skill convention.** The new file pattern (Linux-conf-style markdown with YAML body, kebab-case keys, settings commented out by default with prose rationale, single source of truth in `references/defaults.md`, resolution order user > org > skill) is intended as the canonical example for future skills in the monorepo. Repo-root `CONTRIBUTING.md` points to `references/user-config-template.md`. The nc3-meta-skill-forge skill (working name; tracked in `ROADMAP.md`) will absorb the convention as its canonical home in a future release.
- **Design-spec historical correction.** Design spec §15 stated that v0.1.0-v0.3.2 wrote `schema_version: "0.1"`. Actual v0.3.2 output wrote `schema_version: v0.1.0` (unquoted, full skill-version string). `references/schema-changelog.md` documents the historical reality; migration detection is liberal (matches `v0.1.0`, `0.1.0`, `0.1`, etc.) so real v0.3.2 files are recognized. The design spec correction is a separate doc-only follow-up.

### Migration
- One-time, per-project, automated. Pre-flight detects legacy `*-project-context*.md` files. The skill writes the three new files and surfaces an operator brief listing each legacy file by exact name for manual deletion (the skill cannot delete Project files in v0.4.0 — no platform API). Required order of operations: download new → verify → delete old → upload new. See `references/migration.md`.

## [0.3.2] — 2026-05-11

### Added
- Surface-compatibility guard in `SKILL.md` pre-flight. The skill now politely declines when invoked from Claude Code and recommends the `session-recap` skill instead. project-context targets AI workspaces with persistent project contexts (claude.ai Projects, ChatGPT Projects, Copilot M365 Projects); `session-recap` covers Claude Code and other filesystem-based surfaces.

### Changed
- Generated project-context files no longer carry an `SPDX-License-Identifier` header. The generated content is the operator's work product; the operator chooses the license for their own captured context. Apache 2.0 continues to apply to the skill source files only. Examples updated to match the new no-SPDX convention.

### Notes
- Schema unchanged from v0.1.0. The `schema_version` field in generated outputs remains `v0.1.0`.
- The operator-attribution-on-generated-SPDX flag carried forward in v0.1.0, v0.2.0, and v0.3.0 Notes is **resolved** with this release. Generated outputs have no SPDX header by default.

## [0.3.1] — 2026-05-11

### Fixed
- `modes/consolidate.md` step 9 validation invariant. The v0.3.0 wording instructed the model to verify `records_after_dedup + records_dropped_transient + records_compressed_summary` reflects the input record count, which double-counts records that remained in the output after summary-tier compression (those records are already inside `records_after_dedup` because compression keeps records in the output, just collapsed). The check would fail valid consolidations or push the model to fudge counts to make the equation balance. The new wording treats the three fields as descriptive counters rather than algebraic terms; a strict input-records invariant is deferred until the schema gains the missing fields (records removed by dedup merging, records consumed by compression).
- `modes/generate.md` step 2 same-day collision check. The v0.3.0 wording only checked for `YYYY-MM-DD-project-context-{topic-slug}.md` filenames, which silently misses bare `YYYY-MM-DD-project-context.md` files produced when the operator skipped the topic in step 1. The new step 2 branches on whether a slug was chosen and checks the exact target filename, so broad/no-topic runs reuse the same bare file via the merge prompt instead of overwriting it. The step heading also changed from "Detect same-day same-topic existing file" to "Detect a same-day filename collision" to reflect the broader scope.

### Changed
- `SKILL.md` frontmatter `version: 0.3.0` → `version: 0.3.1`.
- `references/org-config-template.md` example `config_version: v0.3.0` → `v0.3.1`. Schema unchanged; v0.1.0–v0.3.0 configs remain forward-compatible.

### Notes
- Both fixes were surfaced by a P2 automated bot review on PR #1 (TheNeuralCube/claude-skills) immediately after v0.3.0 merged. Acknowledged on the original PR and queued for this patch.
- Schema is unchanged in v0.3.1; generated files continue to declare `schema_version: v0.1.0`. A future schema revision will add fields to support a strict input-records invariant in consolidate mode (records removed by dedup merging, records consumed by summary compression).
- The operator-attribution-on-generated-SPDX flag from v0.1.0 remains open; carried forward to v0.4.0+.

## [0.3.0] — 2026-05-11

### Added
- Operator brief in both modes. `modes/generate.md` step 11 (renamed from "Print the summary" to "Print the operator brief") and `modes/consolidate.md` step 11 now produce a two-part output: a content/consolidation summary plus **explicit, plain-language next-step instructions** that walk a non-technical operator through downloading the generated file, opening their Project, navigating to "Project knowledge," uploading the new file, and handling any older project-context files. The wording defaults to claude.ai Projects terminology with documented adaptations for ChatGPT Projects and Copilot M365 Projects. Consolidate mode's brief is stronger: it forces a review-before-remove step because consolidation can make subtle mistakes and the source files are the operator's only safety net.

### Changed
- Generate mode no longer prompts about session-recap. `modes/generate.md` step 7 previously instructed the bot to *"ask the operator after generation whether they want the `related_session_recap` field populated"* when status was unclear. The new wording explicitly tells the bot **do not raise the topic** unless the operator has explicitly mentioned a session-recap file. project-context is a fully standalone artifact; mentioning a null cross-reference created the false impression that something was missing.
- Generate mode's operator brief mentions `related_session_recap` only when it is populated. If `null`, the operator never hears the word "session-recap" — consistent with the standalone-by-default stance.
- `SKILL.md` frontmatter `version: 0.2.0` → `version: 0.3.0`.
- `references/org-config-template.md` example `config_version: v0.2.0` → `v0.3.0`. Schema unchanged; v0.1.0 and v0.2.0 configs remain forward-compatible.

### Notes
- Schema is unchanged in v0.3.0; generated files continue to declare `schema_version: v0.1.0`.
- Programmatic Project-file management (auto-add new, auto-remove superseded) discussed during planning was **deferred**. The skill remains a manual-file-management workflow. The operator brief is the v0.3.0 answer to that friction: detailed guidance instead of automation. Automation can return as a config block when Anthropic ships a Projects file-management API or a first-party MCP server.
- The operator-attribution-on-generated-SPDX flag from v0.1.0 remains open; carried forward to v0.4.0+.

## [0.2.0] — 2026-05-11

### Added
- Generate mode: intra-conversation supersession instruction (`modes/generate.md` step 3). When a topic, decision, constraint, or fact recurs across the current chat, the model prefers later statements over earlier ones — recording only the resolved position when supersession is clear, combining into a single trajectory record when ambiguous, or asking the operator when the stakes are material. Mirrors the cross-file supersession logic already present in consolidate mode (`modes/consolidate.md` step 5); the difference is generate mode applies it within a single session, between exchanges, while consolidate applies it across files.

### Changed
- `SKILL.md` description trimmed from 1090 to 906 characters to fit the claude.ai skill uploader's 1024-character description limit. All 19 trigger phrases from design spec §9 preserved verbatim; only the framing prose was tightened.
- `SKILL.md` SPDX/copyright comment pair relocated from lines 1–2 to the markdown body (after the frontmatter close) to satisfy the claude.ai uploader, which requires `---` on line 1. The other nine files retain SPDX on lines 1–2.
- `modes/generate.md` step 1: dropped a stale "in v0.1.0" version reference from the default-behavior sentence.
- `SKILL.md` frontmatter `version: 0.1.0` → `version: 0.2.0`.
- `references/org-config-template.md` example `config_version: v0.1.0` → `v0.2.0`. The skill still accepts v0.1.0 configs forward-compatibly (no config-schema fields changed).

### Notes
- Schema is unchanged in v0.2.0; generated files continue to declare `schema_version: v0.1.0`.
- The operator-attribution-on-generated-SPDX behavior flagged in v0.1.0's `### Notes` remains open; carried forward to v0.3.0+ for review alongside any other accumulated licensing questions.

## [0.1.0] — 2026-05-08

### Added
- Initial public release.
- Generate mode: produce a fresh project-context file from the current chat.
- Consolidate mode: merge multiple project-context files plus optional new content from the current chat into a single replacement file.
- Pre-flight check: scans the project's existing project-context files on every invocation, proposes mode with rationale.
- Three preservation tiers: full, summary, transient.
- Open category tags assigned by the model; multi-tag per record.
- File-level YAML frontmatter with optional governance metadata fields (sensitivity, audience, retention, governance_frameworks, custom_governance).
- Per-item governance overrides via inline brackets.
- Optional org-config.md customization layer (upstream-plus-org-config-layer architecture).
- Cross-skill awareness with session-recap via optional `related_session_recap` frontmatter field.
- Filename format: `YYYY-MM-DD-project-context[-{topic-slug}].md`.
- Same-day same-topic merge handling.
- Apache 2.0 license; published to github.com/TheNeuralCube/claude-skills.

### Notes

- Generated project-context files use operator attribution on the SPDX header (operator name plus year), or omit the SPDX header when the operator's attribution is unknown. See `modes/generate.md` step 8. This interpretation is flagged for review in v0.2.0+ as the design spec did not explicitly settle generated-output licensing.
