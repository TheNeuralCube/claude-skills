---
name: project-context
version: 0.3.1
description: Capture forward-grounding context from the current chat into a markdown file the operator adds to a Claude/ChatGPT/Copilot project so future chats start grounded. Use whenever the operator says "create project-context", "create project context", "save project context", "save the project context", "generate project-context", "snapshot project context", "ground this project", "ground the project", "project-context this", "project context this conversation", "build project-context file", "consolidate project-context", "consolidate project context", "consolidate project-context files", "merge project-context files", "compress project-context", "run project-context", "project context", or "project-context skill". Two modes — generate (fresh file, default) and consolidate (merge existing files plus optional new chat content). Pre-flight scans existing files and proposes a mode on every invocation.
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# project-context

A thin-router skill: this file detects the invocation, runs pre-flight, and delegates to one of the two mode files. Mode logic lives in `modes/`. Schema and governance documentation live in `references/`.

## Files in this skill

```
project-context/
├── SKILL.md                                          (this file — router and pre-flight)
├── README.md                                         (user-facing documentation)
├── CHANGELOG.md
├── modes/
│   ├── generate.md                                   (generate-mode logic)
│   └── consolidate.md                                (consolidate-mode logic)
└── references/
    ├── schema.md                                     (file-level + per-item schema)
    ├── governance.md                                 (governance metadata framework)
    ├── org-config-template.md                        (empty template for org customizations)
    └── examples/
        ├── example-fresh-project-context.md
        └── example-consolidated-project-context.md
```

## Routing rules

When this skill is invoked:

1. **Run pre-flight** (below). Pre-flight is not skippable in v0.1.0.
2. **Pick a mode** based on the operator's invocation phrase plus pre-flight signals:
   - Phrases that clearly map to **generate**: "create project-context", "create project context", "save project context", "save the project context", "generate project-context", "snapshot project context", "ground this project", "ground the project", "project-context this", "project context this conversation", "build project-context file".
   - Phrases that clearly map to **consolidate**: "consolidate project-context", "consolidate project context", "consolidate project-context files", "merge project-context files", "compress project-context".
   - Ambiguous phrases ("run project-context", "project context", "project-context skill"): pre-flight proposes a mode based on assessment, then asks the operator to confirm.
3. **Load the relevant mode file** (`modes/generate.md` or `modes/consolidate.md`) and follow its instructions to completion.
4. **Apply org-config overrides** if `org-config.md` is present alongside this skill (see `references/governance.md` and `references/org-config-template.md`). If `org-config.md` is absent, the upstream defaults in `references/schema.md` apply unchanged.

The router itself does not write files, transform records, or merge content. It only detects intent, runs pre-flight, and hands off.

## Default behavior

When `org-config.md` is absent, the skill applies these upstream defaults:

- `sensitivity: internal`
- `retention: standard`
- no fixed audience
- no governance frameworks
- categories are model-inferred with no constrained vocabulary
- section tier defaults come from `references/schema.md`
- pre-flight runs on every invocation
- no downstream chaining instruction is added
- no org-specific terminology overrides are applied

## Pre-flight check

Pre-flight runs on **every** invocation, generate or consolidate. Steps:

1. **Identify the project container** the conversation is in. This is a Claude Project, ChatGPT Project, Copilot M365 Project, or analogous container. If the conversation is not inside a project container, warn the operator that the output will not have a natural home as a project file and ask whether to proceed anyway. If the operator declines, stop.

2. **List existing project-context files** in the project. Match the filename pattern `*-project-context*.md`. Note the date prefix and any topic suffix on each file. If the runtime cannot enumerate project files directly, ask the operator to paste the filenames or confirm none exist.

3. **Assess consolidation readiness** using these signals:
   - **File count.** More than 8 existing files is a flag.
   - **Age distribution.** Files older than 60 days mixed with recent files is a flag.
   - **Topic redundancy.** Multiple existing files with overlapping topic slugs is a flag.
   - **Aggregate size.** Combined file size approaching the project's file-size budget is a flag.

4. **Propose a mode** with a one-paragraph rationale. Examples:

   > Pre-flight: I see 3 project-context files in this project (oldest 2 weeks). Consolidation not warranted yet. Proposed mode: generate. Confirm?

   > Pre-flight: I see 12 project-context files in this project (oldest 4 months) with overlapping topics on `revenue` and `segmentation`. Consolidation is recommended. Proposed mode: consolidate, with these files: [list]. Or: generate (skip consolidation). Which?

5. **Wait for operator confirmation, override, or cancel.** Do not proceed to a mode file until the operator has confirmed.

If the operator's invocation phrase clearly maps to a mode (e.g., "consolidate project-context"), pre-flight still runs but skips the mode-selection question and proceeds directly to that mode after the project and existing-file scan.

## Output behavior

Both modes write a markdown file to the session's output location (whichever path the runtime exposes for generated artifacts) and present it via the available file-presentation mechanism so the operator can download or copy it. The operator manually adds the file to the project — the skill does not have a programmatic path to add files to a Claude Project, ChatGPT Project, or Copilot M365 Project in v0.1.0.

The skill does not commit, push, or transmit the output anywhere. Distribution is the operator's responsibility.

## Failure modes the router handles

- **Not in a project container.** Warn and ask before proceeding.
- **Cannot enumerate existing files.** Ask the operator to paste filenames or confirm none exist.
- **Operator cancels at pre-flight.** Stop without producing a file.
- **Both `generate` and `consolidate` triggers present in the same invocation.** Ask the operator to disambiguate.

All other failure modes (schema violations, deduplication ambiguity, oversized output) are handled by the mode files.
