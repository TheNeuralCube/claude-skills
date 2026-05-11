<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Mode: generate

Generate mode produces **one new project-context file** from the current chat session. It is the default mode and the path most invocations follow.

This document is loaded by `SKILL.md` after pre-flight has identified the project, listed existing files, and confirmed generate as the chosen mode.

## Inputs

- The current chat session's exchanges (everything visible to the model in the active conversation).
- The pre-flight summary (project name, list of existing project-context files in the project, age distribution).
- Optional org-config.md overrides loaded by the router.
- Optional related session-recap filename, if the operator has run the session-recap skill on the same conversation.

## Steps

### 1. Confirm or ask for a topic slug

If the operator's invocation included a topic phrase ("save project context for the segmentation work"), propose the kebab-case slug derived from it ("customer-segmentation") and ask the operator to confirm.

If the operator's invocation did not include a topic, choose one of:
- Skip the topic (file uses the bare `YYYY-MM-DD-project-context.md` form). Acceptable when the session covered the project broadly with no narrower focus.
- Propose a topic slug inferred from the dominant subject of the conversation, and ask the operator to confirm or provide a different slug.

Default behavior: ask. If `org-config.md` sets `filename_topic_required: true`, do not allow the operator to skip; require a slug.

### 2. Detect a same-day filename collision

Determine the **target filename** based on the topic decision from step 1:
- If the operator chose a topic slug: target = `YYYY-MM-DD-project-context-{topic-slug}.md`
- If the operator skipped the topic: target = `YYYY-MM-DD-project-context.md` (bare form)

Check the pre-flight file list for the **exact target filename**. The collision check uses the bare-vs-slugged form actually chosen in step 1 — do not mix them. Bare-form files do not collide with slugged files (and vice versa), so a bare run later the same day still collides with an earlier bare run, and a slugged run still collides with an earlier file of the same slug.

If a same-day file with the same target filename exists:
- Tell the operator and offer to **merge** the new content into the existing file rather than creating a duplicate.
- If the operator confirms merge: read the existing file, treat its records as the starting set, then proceed to step 3 incorporating the existing records and the current chat content. The output overwrites the existing file.
- If the operator declines merge: ask for a new topic slug that does not collide (or, if the original invocation was bare, ask for a slug to disambiguate this run from the existing bare file).

Same-day invocations whose target filenames differ (different slug, or bare vs. slugged) always produce a separate file (the filename difference is sufficient discriminator).

### 3. Extract records from the conversation

Scan the current chat session and extract records into the seven sections defined in `references/schema.md`:

- **Decisions** — choices made or commitments accepted during the session.
- **Constraints** — rules, limits, requirements, or standards the project must respect going forward.
- **Entities** — named people, systems, datasets, organizations, or artifacts that matter to future work.
- **Terminology** — definitions and shared vocabulary the project uses.
- **External references** — pointers to documents, links, datasets, or external artifacts the project depends on.
- **Open items** — unresolved questions, pending tasks, or in-flight work.
- **State snapshot** — point-in-time facts about the project's current status.

Each record is one or more sentences. Each record is **self-contained**: a reader who extracts a single record should understand it without reading the surrounding records. Avoid pronouns whose antecedents live in other records.

**Treat the conversation chronologically.** When a topic, decision, constraint, or fact recurs across the current chat, prefer the **later** expression. If a later statement clearly supersedes an earlier one (e.g., the session explored option A, then settled on option B), record only the resolved position — do not capture the earlier position as a separate decision. If the supersession is ambiguous — the later statement refines or scopes the earlier one rather than replacing it — record both as a single combined record that captures the trajectory (e.g., "Initially scoped to X; refined later in the session to X plus Y"), or ask the operator to disambiguate when the stakes are material. This mirrors the cross-file supersession logic that consolidate mode applies (`modes/consolidate.md` step 5); the difference is that generate mode applies it within a single session, between exchanges, while consolidate applies it across files. Do not hallucinate supersessions — only collapse records when the conversation provides clear evidence that a later statement was meant to override an earlier one.

### 4. Apply tier defaults and tier overrides

For each record, determine its tier. Apply the section default (see `references/schema.md`) unless the record's content suggests a different tier:

- **Promote to `full`** when the record is a definition, decision, or constraint that should never be lossy-compressed.
- **Demote to `summary`** when the record is a state snapshot, in-flight detail, or status note likely to go stale.
- **Demote to `transient`** when the record is conversational scaffolding, redundant restatement, or housekeeping that has no forward-grounding value but is worth recording for completeness.

Records that match the section default omit the `[tier: ...]` bracket. Records that diverge declare their tier explicitly.

If most records in a section diverge from the section default, prefer per-record tier brackets over rewriting the section default. Section defaults are stable across files; per-record overrides are the flex point.

### 5. Assign categories

Assign one or more open category tags per record. Tags are kebab-case or single lowercase words. Pick from the conversation's content; the model has latitude to invent new categories when none of the standard ones fit.

If `org-config.md` sets `categories.constrain_to_vocabulary: true`, restrict to the supplied vocabulary; do not invent new categories.

### 6. Apply governance metadata

File-level frontmatter governance values default to either:
- The org-config defaults if `org-config.md` is present, or
- The upstream defaults from `references/governance.md` (sensitivity: internal, retention: standard, audience empty, governance_frameworks empty, custom_governance empty).

Per-record governance overrides apply only when a record's content clearly diverges from the file-level baseline. Add inline brackets only for the divergent fields. Do not add governance brackets defensively.

If the conversation contained content the model judges to be more sensitive than the file-level default (legal advice, regulated data, contracts), promote the relevant records' sensitivity inline. Do not silently raise the file-level default.

### 7. Populate cross-skill awareness

If the operator has **explicitly** mentioned a session-recap file produced for the same conversation, populate `related_session_recap` in frontmatter with the recap's filename. Otherwise leave as `null` and **do not raise the topic** with the operator at any point — not before generation, not after, not in the operator brief. project-context is a fully standalone artifact; the cross-reference field exists for opt-in cross-skill awareness when both skills are deliberately in use together, not as a missing-piece prompt. Most operators will not have session-recap in play, and surfacing the question creates friction and the false impression that project-context is incomplete on its own.

If the operator has indicated this file builds on a prior project-context file, list those filenames in `related_files`. Otherwise leave the list empty `[]`.

### 8. Construct the file

Assemble in this order:

1. SPDX header (two lines, the same convention as the skill's own files):

   ```
   <!-- SPDX-License-Identifier: Apache-2.0 -->
   <!-- Copyright <year> <project-context-file-author> -->
   ```

   For files generated on behalf of the operator, use the operator's name and year if known; otherwise omit the SPDX header on generated outputs (the upstream skill's own files are Apache 2.0, but operator-authored content is theirs).

2. YAML frontmatter per `references/schema.md`. Validate the YAML before continuing.

3. The seven body sections, in the prescribed order, with the prescribed headers. Empty sections contain the literal placeholder `_No records in this section._`. Do not omit empty sections.

### 9. Validate

Before producing the file, run the validation checklist from `references/schema.md`:

1. Frontmatter is valid YAML and includes every required field.
2. `file_type: project-context`, `file_subtype: fresh`, `schema_version: v0.1.0`.
3. Body has exactly seven sections, in order, with prescribed headers.
4. Empty sections use the placeholder line.
5. Every record is a top-level bullet with content followed by zero or more bracketed metadata fields.
6. Tier values are limited to `full`, `summary`, `transient`.
7. The filename matches `YYYY-MM-DD-project-context.md` or `YYYY-MM-DD-project-context-{topic-slug}.md`.

If any check fails, fix the file content rather than producing invalid output.

### 10. Produce the output

Write the file to the session's output location (whichever path the runtime exposes for generated artifacts) with the chosen filename. Present it via the available file-presentation mechanism so the operator can download or copy it.

The skill does not add the file to the project programmatically. The operator does that step manually.

### 11. Print the operator brief

Print a two-part brief that combines a content summary with **explicit, plain-language next-step instructions for the operator**. Assume the operator may be non-technical and unfamiliar with managing Project files. The goal is that someone who has never used a Project file before can complete the workflow without asking a follow-up question.

#### Part A — Content summary

State briefly:

- Filename produced.
- Record count per section.
- Any governance flags applied at file level (e.g., elevated sensitivity, populated frameworks).
- Whether `org-config.md` was loaded and applied.
- The `related_session_recap` filename, **only if one was populated**. If the field is `null`, do not mention session-recap at all. project-context is a fully standalone artifact; mentioning a null session-recap field creates the false impression that something is missing.

#### Part B — Next-step instructions for the operator

Tell the operator exactly what to do next, in numbered steps and plain language. Avoid jargon (no "frontmatter," no "schema," no "artifact" — say "file"). Default the UI wording to **claude.ai Projects** terminology, since that is the primary surface for v0.3.0. If pre-flight identified a different platform, adapt the labels:

- Claude Projects → "Project knowledge" panel, "Add content" button.
- ChatGPT Projects → "Project files" section, "Add files" button.
- Copilot M365 Projects → "Files" or "Knowledge" section, organization-specific upload button.

Walk the operator through these steps:

**Step 1 — Download the file.** Tell the operator where the file is in the chat and how to save it. Sample wording:

> Your new project-context file is ready. Look for the file card just above this message and click the download icon on it. Save the file to a place you can find it again, like your Desktop or Downloads folder. The filename will be something like `<FILENAME>`.

**Step 2 — Open the Project and find where files live.** Sample wording:

> Now open the Project that this conversation belongs to. You can find the Project name at the top of the chat or in the left sidebar — click it to open the Project page. On the Project page, look for the "Project knowledge" section on the right side. That's where files attached to the Project live.

**Step 3 — Upload the new file.** Sample wording:

> In the "Project knowledge" section, click "Add content" (or the "+" button), choose "Upload from device," and pick the file you just downloaded. Wait until the upload finishes — you'll see the new file appear in the list.

**Step 4 — Handle older project-context files.** Branch on what pre-flight found:

- **If pre-flight found NO existing project-context files in the Project:** Omit this step entirely. The operator only needs to upload the new file. Skip to the closing line.

- **If pre-flight found an existing project-context file on the SAME topic with an OLDER date** (i.e., same topic slug, earlier date prefix): Tell the operator to remove the older file *after* reviewing the new one. Name the older file explicitly. Sample wording:

  > You already have an older project-context file on this same topic in the Project: `<OLD_FILENAME>`. The new file you just uploaded replaces it. To keep the Project's context current and avoid the AI seeing stale information:
  >
  > a. **First, review the new file.** In the "Project knowledge" section, click the new file `<NEW_FILENAME>` to open it. Skim through and confirm everything looks right. If anything is wrong or missing, **do NOT remove the old file yet** — close this and either re-run the skill or fix the new file by hand. The old file is your safety net until you're confident in the new one.
  >
  > b. **Once you're confident the new file is correct, remove the old file.** Find `<OLD_FILENAME>` in the "Project knowledge" list, click the "×" or "Remove" button next to it, and confirm the removal. The old file stays in your chat history if you ever need to look back at it — removing it from the Project just means future chats in this Project won't see it anymore.

- **If pre-flight found existing project-context files on DIFFERENT topics:** Tell the operator to leave those alone. Sample wording:

  > Your Project already has project-context files on other topics — for example, `<OTHER_FILENAME>`. Leave those in place. Different topics live as separate project-context files and complement, not replace, the new one you just added.

**Step 5 — Confirm you're done.** Sample wording:

> That's it. The next conversation you start in this Project will automatically have access to the new context. You don't need to do anything in this chat — you can close it whenever you're ready.

The wording above is a sample script. The model paraphrases per conversation context and adapts the UI labels for the detected platform. Filenames must be concrete (substituted from the actual pre-flight and generation results); do not leave `<FILENAME>` style placeholders in the brief shown to the operator.

### 12. Apply downstream chaining

If `org-config.md` includes `downstream_chaining` entries with trigger `after_generate` or `after_either`, print each entry's `instruction` string as the final lines of the response.

The upstream skill ships with no downstream chaining; this step is a no-op unless org-config.md provides entries.

## Quality checks the model performs internally

- **Self-containment.** Each record can be read alone. Pronouns are resolved.
- **No leakage.** No internal vocabulary from the operator's tooling ecosystem appears in record content unless the operator put it there. The public item-level terms are `record` and `entry`; do not substitute synonyms drawn from any internal ecosystem.
- **No hallucination.** Records reflect content actually in the conversation. Do not synthesize decisions, entities, or constraints that were not stated or clearly implied.
- **Predictable structure.** All seven sections present, in order, even if empty. The downstream AI session reading the file should be able to jump directly to a known section without searching.

## Failure modes

- **Empty conversation.** If the session has produced almost no substantive content, ask the operator whether to proceed; a near-empty file is rarely worth its name.
- **Topic slug collision.** Same-day same-topic file already exists; offer merge or new slug (step 2).
- **Operator cancels mid-generation.** Stop and produce no file.
- **Schema validation fails after generation.** Fix the content and re-validate before output. Do not produce invalid files.
