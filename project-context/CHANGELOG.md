<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to the project-context skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The skill version (e.g., `0.4.0`) tracks releases. Beginning with v0.4.0, the **schema version** (`schema_version` in every file's frontmatter) is **decoupled** from the skill version. The schema version bumps only when the shape of stored data changes; the skill version bumps on every release. See `references/schema-changelog.md` for the version-by-version history of the data schema.

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
