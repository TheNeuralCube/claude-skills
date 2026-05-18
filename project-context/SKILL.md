---
name: project-context
version: 0.4.0
description: Capture forward-grounding context from the current chat into the three-file project-context system (active, entities, archive) so future chats start grounded. Use whenever the operator says "create project-context", "create project context", "save project context", "save the project context", "generate project-context", "snapshot project context", "ground this project", "ground the project", "project-context this", "project context this conversation", "build project-context file", "consolidate project-context", "consolidate project context", "consolidate project-context files", "merge project-context files", "compress project-context", "run project-context", "project context", "project-context skill", "compact this", "trim the project context", "rebuild", or "regenerate project context". v0.4.0 uses four operations (default, merge_external, compact, rebuild) and a five-op merge classifier. Optimized for top-tier thinking models.
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# project-context (v0.4.0)

A thin-router skill. This file detects the invocation, runs the surface guard and pre-flight, and delegates to one of four operation files. Operation logic lives in `operations/`. Schema, scoring, defaults, migration, governance, and configuration documentation live in `references/`.

v0.4.0 is a major architectural pivot from v0.1.x-v0.3.x. The dated single-file output is replaced by a three-file rolling system (`project-context.md`, `entities.md`, `project-context-archive.md`). The two modes (generate, consolidate) become four operations (default, merge_external, compact, rebuild). The skill applies a five-op merge classifier (ADD, UPDATE, NOOP, DEMOTE, SUPERSEDE) with a hybrid brake by default. See `CHANGELOG.md` for the full v0.4.0 change list.

Key references the router and operations consume: `references/schema.md` (data shape, `schema_version: "0.2"`), `references/scoring.md` (formula and coefficients), `references/operations.md` (classifier and common pre-flight), `references/migration.md` (v0.1.x-v0.3.x detection and migration), `references/defaults.md` (single source of truth for tunables).

## Model-assumption disclosure

This skill is optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking, equivalents). The active-file token budgets (target 30K, soft warning 50K, hard ceiling 80K) assume substantial effective context. On lighter models, data integrity may degrade as files approach the hard ceiling.

## Files in this skill

```
project-context/
├── SKILL.md                                          (this file — router and pre-flight)
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── USAGE.md
├── operations/
│   ├── default.md                                   (default operation: parse conversation, classify, propose, write)
│   ├── merge_external.md                            (parse an attached file or external artifact instead of the conversation)
│   ├── compact.md                                   (aggressively demote weak active records)
│   └── rebuild.md                                   (rebuild active file from archive; mandatory pre-commit review)
└── references/
    ├── schema.md                                    (file-level + per-record schema, schema_version "0.2")
    ├── schema-changelog.md                          (version-by-version schema history + drift detection)
    ├── scoring.md                                   (the formula, coefficients, demotion threshold, worked examples)
    ├── operations.md                                (cross-operation logic, classifier pseudocode, pre-flight)
    ├── migration.md                                 (v0.1.x-v0.3.x dated files → v0.4.0 three-file system)
    ├── defaults.md                                  (single source of truth for every configurable default)
    ├── governance.md                                (governance metadata framework)
    ├── user-config-template.md                      (per-user override layer; cross-skill convention)
    ├── org-config-template.md                       (org-scope override layer)
    └── examples/
        ├── example-project-context.md
        ├── example-entities.md
        ├── example-project-context-archive.md
        └── example-user-config.md
```

## Routing rules

When the skill is invoked, the router:

1. **Runs the surface guard.** Detects whether the skill is running on Claude Code. If so, declines and recommends `session-recap` (see Pre-flight section below). The surface guard is not skippable.
2. **Picks an operation** from the operator's invocation phrase. Routing table:

   | Operation | Trigger phrases |
   |---|---|
   | `default` (no-op-named) | "create project-context", "create project context", "save project context", "save the project context", "generate project-context", "snapshot project context", "ground this project", "ground the project", "project-context this", "project context this conversation", "build project-context file", "run project-context", "project context", "project-context skill" (ambiguous; route to default; pre-flight may suggest another operation) |
   | `merge_external` | "merge this into project context", "process this attached file", "import this session-recap", "merge this spec into the project context", any invocation with an explicit file attachment |
   | `compact` | "compact", "compact this", "compact the project context", "trim the project context", "consolidate project-context", "consolidate project context", "consolidate project-context files", "merge project-context files", "compress project-context" |
   | `rebuild` | "rebuild", "rebuild from archive", "reset from archive", "reset project context", "regenerate project context" |

   All 19 of the v0.1.0 trigger phrases preserved verbatim above. The v0.1.0 `consolidate` phrases route to v0.4.0 `compact` (the closest behavioral analog) — the operator can override during pre-flight if they intended `rebuild` instead.

3. **Loads the operation file** (`operations/<operation>.md`) and runs its body to completion.
4. **Applies configuration overrides** by loading `user-config.md` and `org-config.md` if present in the project; resolution order is user > org > skill defaults from `references/defaults.md`.

The router itself does not parse the conversation, classify records, write files, or apply scoring. It only detects intent, runs the surface guard, and hands off.

## Default behavior

When neither `user-config.md` nor `org-config.md` is present, the skill applies the upstream defaults documented in `references/defaults.md`. Highlights:

- `merge_policy: hybrid` (auto-apply ADD and NOOP; gate UPDATE, DEMOTE, SUPERSEDE).
- `proposal_cap_per_session: 10`.
- `active_file_token_target: 30000`, `soft_warning: 50000`, `hard_ceiling: 80000`.
- Scoring coefficients per `references/scoring.md` (`alpha: 1.5`, `beta: 1.0`, `gamma: 5.0`, `delta: 2.0`, `epsilon: 0.5`, `lambda: 0.0347`, `demotion_threshold: 5`).
- `sensitivity: internal`, `retention: standard` (active/entities) or `indefinite` (archive).
- Surface guard always on. Migration detection always on.

## Pre-flight check (common prologue)

Every operation begins with the same pre-flight prologue. The full sequence is in `references/operations.md` section 4. The surface guard is restated inline in each operation file because it can terminate the operation immediately.

### Surface compatibility check

Before proceeding, confirm you are running on a supported surface. project-context targets AI workspaces with persistent project contexts the operator can attach files to: Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects, and similar hosted AI surfaces.

project-context is **not** designed for Claude Code. Claude Code uses filesystem-based working directories, not hosted project contexts; the `session-recap` skill is the right tool for capturing context from Claude Code sessions.

**If you detect you are running in Claude Code** — signals include: filesystem-mutation tools (e.g., `Bash`, `Write`, `Edit`) are present in your toolbox; the working directory is filesystem-based; no Project-UI affordances are visible to the operator — politely decline and recommend `session-recap`:

> This skill is designed for AI workspaces with persistent project contexts (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects). For capturing context from a Claude Code session, the `session-recap` skill is the right tool. Would you like to invoke `session-recap` instead?

### Other pre-flight steps

After the surface guard passes:

1. **Project detection.** Identify the Project container. If the conversation is not in a Project, warn and ask before proceeding.
2. **File discovery.** Scan for the three canonical filenames (`project-context.md`, `entities.md`, `project-context-archive.md`), legacy dated filenames (`*-project-context*.md`), and configuration files (`user-config.md`, `org-config.md`).
3. **Schema verification.** Parse the frontmatter of every file found and confirm `file_role` matches the filename.
4. **Conflict detection.** If multiple files claim the same `file_role`, prompt the operator to identify the canonical one.
5. **Migration trigger.** If legacy v0.1.x-v0.3.x files exist (whether alone or alongside v0.4.0 files), initiate migration per `references/migration.md`. The migration brief's required `download → verify → delete old → upload new` ordering is the review gate; pre-flight does not add a separate coexistence question. Only the pure-current state (v0.4.0 files present, no legacy files) skips migration.
6. **Configuration resolution.** Load `user-config.md` and `org-config.md` if present; apply layered defaults.

Pre-flight produces a state snapshot used by the operation body. Detailed pre-flight per operation lives in the operation file.

## Output behavior

Operations write three markdown files to the session's output location and present them via the available file-presentation mechanism so the operator can download and re-upload them to the Project. The skill does not have a programmatic path to add files to a Claude Project in v0.4.0 (awaiting platform API capability; tracked in `ROADMAP.md`).

The skill does not commit, push, or transmit output anywhere. Distribution is the operator's responsibility.

## Failure modes the router handles

- **Claude Code surface detected.** Decline; recommend `session-recap`.
- **Not in a Project container.** Warn and ask before proceeding.
- **Multiple ambiguous trigger phrases in one invocation.** Route to the most specific operation; if still ambiguous, ask the operator.
- **Legacy files detected.** Route through migration (operations preserve this in their pre-flight).
- **`user-config.md` malformed.** Warn; fall back to org-config / upstream defaults.

All other failure modes (schema violations, classifier ambiguity, oversized output, validation errors) are handled by the operation files.
