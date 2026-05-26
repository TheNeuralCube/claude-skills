---
file_role: skill-operation
operation: merge_external
schema_version_documented: "0.4"
skill_version: "0.6.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operation: merge_external

## Pre-flight prerequisite

The operations in this document apply only after pre-flight (`references/preflight.md`) has completed and operator confirmation (where required by the verdict) has been received. Operations described here assume a valid, classified project state. Do not execute these operations without pre-flight completion.

`merge_external` is a variant of the default operation. Instead of parsing the current conversation, it parses an attached file (or a named external artifact) and runs the same classify → propose → write → brief flow.

This operation is triggered when the operator:

- Attaches a file when invoking the skill, AND/OR
- Says "process this attached file", "merge this into project context", "import this session-recap", "merge this spec into the project context", or similar.

Routing is handled by `SKILL.md`. This file documents the operation's behavior; it deviates from `operations/default.md` only in step 2 (input parsing). Everything else is identical to default.

## 1. Pre-flight prologue

Identical to `operations/default.md` section 1 (surface guard → project detection → file discovery → schema verification → migration trigger if needed → configuration resolution). See `references/operations.md` section 4 for the full sequence.

## 2. Identify and read the external file

The operator's invocation provides one of:

- A literal file attachment in the chat (most common).
- A filename or path referring to a file already in the Project.
- A URL or external reference (handled by best-effort fetch; if unsupported by the runtime, halt with explanation).

Read the file. Determine its type:

| Detected type | Treatment |
|---|---|
| `session-recap` output (recognized by frontmatter `file_type: session-recap`) | Use session-recap-aware extraction: pull records from the "Decisions made," "Action items," "Key context" sections per session-recap's documented format. |
| Markdown with YAML frontmatter | Treat as structured. Parse YAML, then parse the body's section headers. |
| Plain markdown | Treat as unstructured. Extract records from section headers and bullet points; the parser does its best. |
| Vision document / spec / partner doc | Treat as unstructured. Focus extraction on Decisions, Constraints, Open Items, and Terminology sections if they exist; treat narrative prose as candidate Current State or External Reference records. |
| Unrecognized binary or unparseable | Halt; ask the operator for a text-based version or a different file. |

## 3. Parse for candidates

For each candidate extracted from the file:

- `content` — record text, self-contained.
- `source_quote` — verbatim text from the file.
- `source_kind: external_file`.
- `source_ref` — the filename plus a stable locator (section header or line range). Example: `"Q2-spec.md#section-3-decisions"` or `"Q2-spec.md:lines-45-58"`.
- `importance` — model-assigned per `references/scoring.md` section 6.
- Section / file routing — same table as `operations/default.md` section 2.

The skill is more conservative on `merge_external` than on `default`. External files often contain commentary, examples, and context that is not itself a candidate record. Skip:

- Quoted prior decisions that the file is just re-stating, unless they appear to be new constraints.
- Worked examples in technical specs (treat as External References instead).
- Author commentary that does not propose a decision, constraint, or open item.

When in doubt, prefer fewer ADDs and lean on the diff-and-approve flow to surface borderline candidates with `explain N` available.

## 4-9. Identical to `operations/default.md`

The classifier (step 3 in default), end-of-session DEMOTE pass (step 4 in default), hybrid brake (step 5 in default), diff-and-approve flow (step 6 in default), file writes (step 7 in default), auto-mode handling (step 8 in default), and operator brief (step 9 in default) are unchanged.

One adjustment in the diff-and-approve UI: every proposal's "source" field is the **filename** (with locator) rather than the conversation. The proposal block uses the same template but with file-aware source references:

```
🟡 **External merge proposals from Q2-spec.md.** I propose 4 updates:

  ➕  ADD      #1  (importance: 8) Tier-2 enterprise pricing methodology
                   (source: Q2-spec.md#section-3-decisions, line 42)
  ✏️  UPDATE   #2  (importance: 7) Constraint update: "all customer IDs
                   must use the v3 schema" (existing record con-005, first noted 2026-04-12)
  📦  DEMOTE   #3  Old constraint about v2 customer ID schema
                   (superseded by #2)
  ➕  ADD      #4  (importance: 6) New external reference: Q2 board deck
                   (linked from Q2-spec.md#references)
```

## 10. Failure handling

In addition to the failure modes in `operations/default.md` section 10:

| Failure | Handling |
|---|---|
| File cannot be read | Halt; report the read error. |
| File is too large to parse in one pass | Surface the size to the operator; offer to chunk by section header. |
| File contains internal contradictions | Treat each contradiction as a SUPERSEDE proposal where the **later** record (by file order or explicit date) supersedes the earlier; flag the contradiction in the proposal block with the 🔴 severity marker. |
| File references records by ID that do not exist in the current project files | Surface as suggestion in the brief ("This file references dec-099, which I do not see in your project. You may want to import it."). |

## 11. Cross-references

- Default operation (parent flow): `operations/default.md`.
- Common operation logic and classifier: `references/operations.md`.
- Schema: `references/schema.md`.
- Scoring formula and coefficients: `references/scoring.md`.
- Defaults: `references/defaults.md`.
- Migration from legacy files (invoked from pre-flight): `references/migration.md`.
- Configuration overrides: `references/user-config.md.template`, `references/org-config.md.template`.
- Other operations: `operations/compact.md`, `operations/rebuild.md`.
