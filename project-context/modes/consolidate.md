<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Mode: consolidate

Consolidate mode merges multiple existing project-context files (and optionally new content from the current chat session) into **one new replacement file**. It is invoked when project-context files have accumulated in a project to the point where they are friction (file count, age distribution, topic redundancy, aggregate size).

This document is loaded by `SKILL.md` after pre-flight has identified the project, listed existing files, and confirmed consolidate as the chosen mode.

## Inputs (three sources)

Consolidate accepts three input sources, not two. A naive implementation that handles only existing files misses the third source.

1. **Operator-specified files.** Existing project-context files the operator has named at invocation time.
2. **Skill-suggested files.** Existing project-context files the skill proposes for inclusion based on pre-flight signals (overlapping topic slugs, age, redundancy). The operator can accept, modify, or override the proposal.
3. **Current chat content.** New records from the current conversation that the operator wants incorporated into the consolidated file. This third source makes consolidate a hybrid "merge-existing-plus-incorporate-new" operation rather than a pure file-merge.

The skill explicitly asks about source 3; do not assume the operator wants current-chat content included.

## Steps

### 1. Confirm or revise the source-file set

Pre-flight produced a candidate list. Show it to the operator and ask:

> The pre-flight identified these N files as candidates for consolidation: [list]. Use this set, modify it, or specify a different set?

If the operator modifies the set, accept the revision. If they specify their own set, use that instead. The minimum useful consolidation is two source files; offer to bail out and run generate mode if only one file is supplied.

### 2. Ask about current-chat content

After the source files are confirmed, ask:

> Do you want to include new records from the current chat session in the consolidated output?

- If **yes**: extract records from the current session using the same logic as generate mode steps 3–6, and treat them as an additional input to the merge.
- If **no**: proceed with only the source files.

Default: ask explicitly. Do not assume.

### 3. Read the source files

For each source file:

1. Parse its YAML frontmatter and body.
2. Validate that it conforms to the v0.1.0 schema (or a forward-compatible older version). If a file does not conform, surface the issue to the operator and ask whether to skip the file or stop consolidation.
3. Collect every record per section. Preserve each record's tier and category metadata.
4. Note the file's source filename for the consolidated frontmatter's `source_files` list.

### 4. Merge records by tier

Process the combined record set per the three preservation tiers:

- **`full`-tier records: deduplicate.** Use semantic deduplication, not just string-match. Two records that say the same decision in different words are one record, not two. Pick the clearer formulation, or merge into a single record that incorporates both. Preserve all categories from the source records (union the category sets). Preserve the strictest governance metadata when records conflict (e.g., if one source has `sensitivity: confidential` and another has `internal`, the merged record carries `confidential`).
- **`summary`-tier records: compress.** Compress into shorter formulations that preserve the gist. Stale summary records (e.g., a state snapshot from six months ago that has been superseded by newer state snapshots) can be dropped if the operator's project history shows clear supersession. Otherwise compress and keep.
- **`transient`-tier records: drop.** Transient records do not survive consolidation. Do not retain them under any tier.

### 5. Resolve conflicts

When two source records say contradictory things (e.g., one decision says "we will adopt X" and a later one says "we have reverted X"), the **later** record wins by default. Note the supersession in a single record that captures both positions:

> - Originally adopted approach X (April), reverted in June. Current direction: do not use X. [tier: full] [categories: decisions, history]

If the supersession order is ambiguous (e.g., two same-day source files conflict), surface the conflict to the operator and ask which is current.

### 6. Reassemble into the seven sections

Place merged records back into their original sections (Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot). A record never changes section during consolidation; if a record was in `Constraints` in its source file, it stays in `Constraints` in the consolidated file.

Within each section, sort records to put the most-currently-relevant records first when an obvious ordering exists (e.g., open items by priority, state snapshot by recency). Otherwise preserve the relative order from the source files, with later-source records following earlier-source records.

### 7. Construct the file

Do NOT add an `SPDX-License-Identifier` header to the consolidated output file. The consolidated content is the operator's work product; see `modes/generate.md` step 8 for rationale.

Assemble the consolidated file:

1. YAML frontmatter per `references/schema.md`. Required additions for consolidated files:
   - `file_subtype: consolidated`.
   - `source_files: [list of every source filename merged in]`.
   - `sessions_covered: [date range, e.g. "2026-04-15 through 2026-08-14"]`.
   - `consolidation_summary` block with `source_file_count`, `records_after_dedup`, `records_dropped_transient`, `records_compressed_summary`.
2. The seven body sections, in the prescribed order, with the prescribed headers. Empty sections contain `_No records in this section._`.
3. After the body, an explicit recommendation block:

   ```markdown
   ---

   _Source files recommended for removal after operator review of this consolidated file:_
   - <filename 1>
   - <filename 2>
   - ...
   ```

   The skill **does not** auto-delete source files. The operator removes them manually after reviewing the consolidated output.

### 8. Choose the filename

Use:

```
YYYY-MM-DD-project-context-consolidated.md
```

If a consolidation has already run today (rare), disambiguate:

```
YYYY-MM-DD-project-context-consolidated-2.md
YYYY-MM-DD-project-context-consolidated-3.md
```

The date is **the consolidation date**, not the date of any source file.

### 9. Validate

Run the same validation checklist from `references/schema.md`. Additional consolidation-specific checks:

- `file_subtype: consolidated`.
- `source_files` is non-empty and lists every consumed source.
- `sessions_covered` is populated with a meaningful range.
- Populate `records_after_dedup`, `records_dropped_transient`, and `records_compressed_summary` honestly as non-negative integers. **Do not enforce an arithmetic identity** between these three fields and the input record count: `records_after_dedup` is an output count that already contains the records remaining after summary-tier compression, so `records_after_dedup + records_compressed_summary` double-counts those records. A strict input-records invariant requires fields the v0.1.0 schema does not track (records removed by dedup merging, records consumed by compression); deferred to a future schema revision. Treat the three fields as descriptive counters, not algebraic terms.

### 10. Produce the output

Write the consolidated file to the session's output location and present it via the available file-presentation mechanism. The operator downloads it and adds it to the project manually.

### 11. Print the operator brief

Print a two-part brief that combines a consolidation summary with **explicit, plain-language next-step instructions for the operator**. Assume the operator may be non-technical. Consolidation is higher-stakes than generation because multiple source files will be removed at the end — the brief must make review-before-remove unmistakable.

#### Part A — Consolidation summary

State briefly:

- Number of source files consumed.
- Per-section record counts in the output.
- Number of records deduplicated (full-tier merges).
- Number of records compressed (summary-tier compressions).
- Number of records dropped (transient-tier removals).
- The list of source files recommended for removal (the same list that appears in the consolidated file's removal block).
- Any conflicts the operator resolved during step 5.

#### Part B — Next-step instructions for the operator

Tell the operator exactly what to do next, in numbered steps and plain language. Avoid jargon (no "frontmatter," no "schema" — say "file"). Default the UI wording to **claude.ai Projects** terminology; adapt for ChatGPT Projects ("Project files") or Copilot M365 Projects ("Files" / "Knowledge") if pre-flight identified one of those.

Walk the operator through these steps:

**Step 1 — Download the consolidated file.** Sample wording:

> Your consolidated project-context file is ready. Look for the file card just above this message and click the download icon to save `<CONSOLIDATED_FILENAME>` to your computer.

**Step 2 — Open the Project and find where files live.** Sample wording:

> Now open the Project that this conversation belongs to. You can find the Project name at the top of the chat or in the left sidebar — click it to open the Project page. On the Project page, look for the "Project knowledge" section on the right side. That's where files attached to the Project live.

**Step 3 — Upload the new consolidated file.** Sample wording:

> In the "Project knowledge" section, click "Add content" (or the "+" button), choose "Upload from device," pick `<CONSOLIDATED_FILENAME>` from where you saved it, and wait until the upload finishes. You'll see the new file appear in the list, alongside the older project-context files that are still there for now.

**Step 4 — Review the consolidated file before removing anything.** This is the most important step. Sample wording:

> **Stop and review before you remove anything.** Consolidation can make subtle mistakes — a decision merged incorrectly, an open item dropped that should have been kept, a date misread. The source files in the Project are your safety net until you're confident the consolidated file is correct.
>
> a. In the "Project knowledge" section, click `<CONSOLIDATED_FILENAME>` to open it.
> b. Read through it section by section. Don't just skim. Look for:
>    - Decisions that should be there but aren't.
>    - Decisions that look wrong, garbled, or made up.
>    - Open items that should be marked closed (or vice versa).
>    - The "recommended for removal" block at the bottom — confirm those filenames match the source files you expected to consolidate.
> c. If anything looks wrong, **stop here.** Do not remove the source files. Either re-run consolidation with a corrected source set, or edit the consolidated file by hand before continuing. The source files in the Project are still your single source of truth.

**Step 5 — Remove the source files (only after the review passes).** Tell the operator exactly which files to remove. Pull the filenames from the consolidated file's "recommended for removal" block. Sample wording:

> Once you've reviewed the consolidated file and you're confident it's correct, remove the source files it replaces. The consolidated file lists them at the bottom under "Source files recommended for removal." For this consolidation, those are:
>
> - `<SOURCE_FILENAME_1>`
> - `<SOURCE_FILENAME_2>`
> - `<SOURCE_FILENAME_3>` *(continue for as many source files as the consolidation consumed)*
>
> For each one:
> a. Find the file in the "Project knowledge" list.
> b. Click the "×" or "Remove" button next to it.
> c. Confirm the removal.
>
> The files stay in your chat history if you ever need to look back at them — removing them from the Project just means future chats in this Project won't see them.

**Step 6 — Confirm you're done.** Sample wording:

> That's it. Your Project now has a single consolidated project-context file that captures everything from the source files. Future chats in this Project will see the consolidated context and won't be confused by the older fragmented files.

If pre-flight identified existing project-context files on **different topics** that were NOT part of this consolidation, mention them briefly so the operator knows not to touch them:

> Note: your Project may have other project-context files on different topics (for example, `<OTHER_FILENAME>`). Leave those in place — they cover different topics and are not part of what was consolidated here.

The wording above is a sample script. The model paraphrases per conversation context and adapts the UI labels for the detected platform. Filenames must be concrete (substituted from the actual pre-flight and consolidation results); do not leave `<FILENAME>` style placeholders in the brief shown to the operator.

### 12. Apply downstream chaining

If `org-config.md` includes `downstream_chaining` entries with trigger `after_consolidate` or `after_either`, print each entry's `instruction` string as the final lines of the response.

The upstream skill ships with no downstream chaining; this step is a no-op unless org-config.md provides entries.

## Quality checks the model performs internally

- **No silent loss.** A `full`-tier record from a source file appears in the consolidated output (possibly merged with siblings) unless the operator has explicitly approved its removal.
- **Strictest-governance-wins.** When source records conflict on governance metadata, the merged record carries the strictest values. Do not downgrade sensitivity during consolidation.
- **Frontmatter declares provenance.** The `source_files` list is the audit trail. Every file consumed is listed.
- **No hallucinated supersessions.** A "later record wins" call requires actual evidence of supersession in the source files (or in the current chat content if source 3 is included). Do not invent supersessions.
- **Vocabulary discipline.** The consolidated content uses `record` or `entry` for items; do not substitute synonyms drawn from any internal ecosystem.

## Failure modes

- **Single source file supplied.** Offer to switch to generate mode using that file as `related_files` input rather than running a degenerate consolidation.
- **Source file fails schema validation.** Ask the operator whether to skip the file or stop. Do not silently drop bad sources.
- **Operator cancels mid-merge.** Stop and produce no file. Do not partially consolidate.
- **Aggregate output exceeds project file-size budget.** Surface the issue to the operator before producing the file. Options: tighten compression on summary-tier records, drop borderline summary-tier records that the operator confirms are stale, or split the consolidation into two output files (each with its own consolidated frontmatter and source_files list).
- **Operator opts to remove source files before reviewing the consolidated output.** Decline to assist and remind them that the recommendation block is contingent on their review of the consolidation; the safety net is the operator's review, not the skill's.
