---
file_role: skill-mode
mode: retrofit
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Mode: retrofit

## Pre-flight prerequisite

This mode runs only after pre-flight (`references/preflight.md`) has completed. retrofit runs on the `⚠ Retrofit needed` verdict (schema-only upgrade, auto-proceeds or `confirm retrofit` per config) and on the batch case (`confirm retrofit`). Do not execute this mode without pre-flight completion.

retrofit upgrades an older-schema handoff to the current schema while **preserving the operator's content verbatim**. It is a mature core carried forward from the predecessor skill (v1.5) and adapted to the v0.1.0 schema. retrofit is also the reusable step that update composes when it is handed a stale-schema prior handoff (`modes/update.md`).

retrofit and update are distinct internal paths because their content rules are opposite: retrofit is lossless, update is intrinsically lossy (it curates to a budget). A single shared content-handling default between them would risk silently rewriting archival content. The operator-facing surface is unified anyway; pre-flight auto-routes (`references/preflight.md`).

Schema reference: `references/schema.md`. Supported Schemas and detection: `references/schema-changelog.md`.

## 1. Lossless is the hard rule

Content rewrite during a schema bump is a build-blocking defect. retrofit changes frontmatter shape only; it does not touch the resumption payload. This covers both zones (`references/schema.md` section 2): the Zone 1 tier-2 structured blocks (`project`, `artifacts`, `schemas`, `state_snapshot`, `decisions`, `known_issues`, `open_items`, `continuation`, `source_ingestion`, `changelog`) carry verbatim, including every `state_marker`, `metric`, and `safe_edit_rule`, and the Zone 2 narrative carries verbatim. Diff before-and-after content as a final check (section 4); any content change halts the operation.

## 2. Single-file retrofit

1. **Detect the source schema_version.** Consult `references/schema-changelog.md` Supported Schemas. At inception (v0.1.0) there is no older public schema to upgrade from; the mechanism is in place for the first future schema bump. If a file's schema is already current (`"0.1"`), report that no retrofit is needed.
2. **Upgrade the frontmatter to the current schema.** Add or rename fields, set defaults for newly required fields, and preserve all existing values. Map old field names to new ones per the relevant schema-changelog entry. Set `schema_version` to the current value and stamp `generated_by.generation_mode: retrofit`.
3. **Preserve the resumption payload and all content verbatim.** Do not summarize, curate, reorder, or rewrite. The payload is the operator's content.
4. **Preserve identity and lineage.** `handoff_id`, `handoff_version`, `supersedes`, `prior_handoffs`, `consolidation_depth`, and `derivative_of` are carried from the source unchanged. retrofit does not mint a new identity and does not increment the version; it upgrades the same artifact in place.

## 3. Batch retrofit

The files-only case: a folder of stale-schema handoffs, no live conversation.

1. Apply the single-file schema-only upgrade (section 2) to each file independently.
2. Content is preserved verbatim per file.
3. Report per-file outcomes in the post-flight summary (upgraded, already-current, or failed), so a partial batch is legible.

Batch retrofit keeps an explicit trigger because it is genuinely different I/O (N files, no live conversation); naming it is clearer than auto-detecting it.

## 4. Validate and write

1. Run the validation checklist (`references/schema.md` section 6) on each upgraded file.
2. **Content-preservation check:** diff the resumption payload before and after the upgrade across both zones (the Zone 1 tier-2 structured-block values and the Zone 2 narrative). Any difference beyond the tier-1 frontmatter-contract shape is a build-blocking defect; halt and report.
3. Write each upgraded file under its existing filename and version suffix (the version does not change on retrofit).
4. No SPDX header on the handoff (operator work product).

## 5. Post-flight

Emit the post-flight summary (`references/preflight.md` section 9): for each file, the source schema, the target schema, and the confirmation that content was preserved verbatim. For a batch, list per-file outcomes.

## 6. Composed retrofit (update on stale input)

When update is handed a stale-schema prior handoff, it composes retrofit first: this mode runs the schema-only upgrade (sections 2 and 4), then control returns to `modes/update.md` for the refresh. Post-flight reports the composition explicitly (deviation reporting, `references/preflight.md` section 9.3): the migration happened, then the refresh.

## 7. Failure handling

| Failure | Handling |
|---|---|
| Source schema unrecognized | Report; do not guess a mapping. Surface as `✗ Parse Error` or `✗ Mismatch and refuse` per `references/schema-changelog.md`. |
| Source schema newer than the skill writes | `✗ Mismatch and refuse`; reveal the expected schema. |
| Content differs before-and-after | Build-blocking defect; halt; do not write. |
| One file in a batch fails | Continue the rest; report the failure in post-flight; do not abort the whole batch silently. |

## 8. Cross-references

- Schema and the validation checklist: `references/schema.md`.
- Supported Schemas, detection, and the (forward-looking) retrofit paths: `references/schema-changelog.md`.
- The update path that composes retrofit: `modes/update.md`.
- Pre-flight verdicts and the retrofit token: `references/preflight.md`.
