<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to the project-context skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this skill adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
