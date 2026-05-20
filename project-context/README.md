<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context

> Forward-grounding context for AI sessions inside a project. Three rolling files, four operations, automatic decay and archival.

## What this skill does

The project-context skill captures the decisions, constraints, current state, open items, terminology, external references, and entities from your chats into a **three-file system** the operator adds to their Claude Project (or ChatGPT Project / Copilot M365 Project). Future chats inside the same project load those files and start grounded — without the operator re-explaining context they already established.

The three files:

- **`project-context.md`** — active grounding file. Decisions, constraints, current state, open items, terminology, external references. Soft ceiling 50K tokens, hard ceiling 80K.
- **`entities.md`** — stable reference data. People, places, things, organizations, datasets. Looked up by name. No automatic decay.
- **`project-context-archive.md`** — append-only history. Superseded and demoted records plus per-merge checkpoint log. Loaded selectively (rebuild, restore, historical lookup), not on every chat.

The skill ships with four named operations:

- **`default`** (no operation named) — parse the conversation, classify candidate records against the existing files, propose merges, write updated files. The everyday workflow.
- **`merge_external`** — same flow, but the input is an attached file (session-recap output, vision document, spec, partner doc) instead of the conversation.
- **`compact`** — score all active records, propose batch DEMOTE for records below the demotion threshold. Manual cleanup when the active file approaches the soft warning.
- **`rebuild`** — regenerate the active file from the archive using the current scoring algorithm. Recovery operation. Mandatory pre-commit review.

v0.4.0 was the architectural pivot from v0.1.x-v0.3.x (dated-single-file model and two modes replaced by the rolling three-file system and four operations). v0.5.0 inherits all of that and closes the protocol-enforcement gap: a mandatory pre-flight protocol structurally gates every operation, schema bumps to "0.3" with a new REQUIRED `_managed_by: project-context-skill` field, and a symmetric post-flight summary closes the audit loop. See `CHANGELOG.md`.

## Who this skill is for

AI-literate professionals who work inside projects spanning multiple chat sessions on a recurring topic — quarterly business reviews, multi-week investigations, long-running design work, ongoing audits. The user is comfortable with YAML frontmatter, structured markdown, the merge classifier vocabulary (ADD, UPDATE, NOOP, DEMOTE, SUPERSEDE), and the idea that the file's primary audience is future AI sessions, not human readers.

The skill is **explicitly not** for non-AI-literate users. Such users are downstream consumers of output from chats that were grounded by project-context — they should not be invoking the skill directly. The path to less-technical users is the agent layer (post-v1.0.0), not this skill.

**Model assumption.** This skill is optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking). Token budgets assume substantial effective context. On lighter models, data integrity may degrade as files approach the hard ceiling.

## When to use this skill (and when not to)

| Use **project-context** when | Use **session-recap** instead when |
|---|---|
| You're inside a Claude Project / ChatGPT Project / Copilot M365 Project. | You're in Claude Code or another filesystem-based surface. |
| You want forward-grounding for future chats in the same project. | You want a portable, exhaustive recap that travels outside any specific project. |
| You want the three-file system maintained automatically with a decay model. | You want a single rich, human-readable handoff document. |
| The primary audience for the output is future AI sessions. | The audience includes human collaborators who will read the file. |

You can run **both** skills on the same conversation. They serve different purposes and each tolerates the presence of the other. project-context can optionally cross-reference a session-recap file via the `related_session_recap` frontmatter field, and `merge_external` can ingest a session-recap output as input.

## How to invoke

The skill is triggered by phrases in your chat. The full list lives in `SKILL.md`; the most common:

**Default (everyday flow):**
- "create project-context", "save project context", "snapshot project context", "ground this project"
- "build project-context file"
- "run project-context", or just "project context"

**Compact (cleanup):**
- "compact this", "trim the project context"
- "consolidate project-context" (legacy phrase routes to compact)

**Rebuild (recovery):**
- "rebuild", "rebuild from archive", "reset from archive", "regenerate project context"

**Merge external file:**
- Attach a file in the chat (the skill detects the attachment).
- Or: "merge this into project context", "process this attached file", "import this session-recap".

All 19 trigger phrases from v0.1.0 are preserved verbatim in v0.5.0 and route to the closest behavioral equivalent.

The pre-flight check runs first regardless of phrase. In v0.5.0 pre-flight is a structural gate (`## Protocol` section of `SKILL.md`): the skill emits an operator-visible pre-flight report block (verdicts: `✓ Compatible`, `✓ Fresh Project`, `⚠ Legacy`, `⚠ Upgrade Available`, `⚠ Partial State`, `✗ MISMATCH`, `✗ Parse Error`, `✗ Infrastructure Failure`) and waits for a confirmation token (e.g., `confirm merge`, `confirm migration`, `confirm upgrade`) before generating output. See [`references/preflight.md`](references/preflight.md) for the full protocol. A symmetric post-flight summary closes the audit loop after writes complete.

## Output format

The skill writes three markdown files with YAML frontmatter and structured-YAML records under each section header. The schema is documented in `references/schema.md`.

Highlights:

- Every file carries `schema_version: "0.3"` (the data-shape contract — decoupled from the skill version).
- Every file carries `_managed_by: project-context-skill` (registry marker introduced in schema "0.3"; makes pre-flight detection reliable).
- Every file carries an `id_prefix_legend` map so a reader has the full eight-prefix legend regardless of which file is loaded.
- Every record carries lifecycle fields (`first_seen_update`, `last_seen_update`, `first_seen_at`, `last_seen_at`, `times_seen`), a numeric `importance` (1-10), a `status` (`active`, `superseded`, `archived`), provenance (`source_quote`, `source_kind`, `source_ref`), `links`, and an `audit` block.
- The archive's `checkpoints` array lives in frontmatter (per-merge log); its body is a flat `## Records` list discriminated by `status`.
- Auto-approved records (under `merge_policy: auto`) carry a literal `[AUTO]` prefix on their `content` field plus `audit.approval_mode: auto`.

For complete examples, see [`references/examples/example-project-context.md`](references/examples/example-project-context.md), [`references/examples/example-entities.md`](references/examples/example-entities.md), [`references/examples/example-project-context-archive.md`](references/examples/example-project-context-archive.md).

## Filename convention

Rolling filenames (no date in the filename — date lives in `last_merged` frontmatter):

```
project-context.md
entities.md
project-context-archive.md
user-config.md          (optional, per-user overrides)
org-config.md           (optional, org-scope overrides)
```

## Customization with user-config.md and org-config.md

The skill follows a **three-layer configuration model** (introduced in v0.4.0, preserved in v0.5.0):

| Layer | Source | Scope | Priority |
|---|---|---|---|
| User | `user-config.md` | This user, this project | Highest |
| Org | `org-config.md` | All users in the org | Middle |
| Skill | `references/defaults.md` | Universal | Lowest |

- The user layer was new in v0.4.0. The template is at [`references/user-config-template.md`](references/user-config-template.md). Drop it in your Project, uncomment the settings you want to override, and the skill will pick them up. This is the canonical example of the **`user-config.md` cross-skill convention** that future skills in the monorepo will adopt.
- The org layer is unchanged from v0.1.0. The template is at [`references/org-config-template.md`](references/org-config-template.md). Copy it to `org-config.md` in your Project's deployment if you want org-scope governance defaults, scoring tweaks, trigger-phrase additions, or downstream chaining reminders.
- The skill layer is the source of truth for unset values, documented in [`references/defaults.md`](references/defaults.md).

What the config layers can change: merge policy, proposal cap, token budgets, scoring coefficients and threshold, governance defaults, user identifier (for audit trail), brief format, additional trigger phrases, downstream chaining.

What they cannot change: schema validity. The three files, eight ID prefixes, six body sections of `project-context.md`, five sub-sections of `entities.md`, archive's `status`-discriminated body, the `audit` block, and the `_managed_by` registry marker are all part of the `schema_version: "0.3"` contract.

## Migration from v0.1.x-v0.3.x (legacy) or v0.4.0 (upgrade)

v0.5.0 supports two migration paths, both routed by pre-flight:

- **Legacy migration** (v0.1.x-v0.3.x dated files → schema "0.3"). Pre-flight detects legacy `*-project-context*.md` files and emits `⚠ Legacy`. Confirmation token: `confirm migration`. The skill parses legacy records, stamps lifecycle fields, scores them, partitions into active and archive, and writes the three new files directly at schema "0.3" (skipping schema "0.2" entirely). The operator brief lists each legacy file by exact filename for manual deletion (the skill cannot delete Project files in v0.5.0 — no platform API). Required order of operations: download new → verify → delete old → upload new.
- **Upgrade migration** (v0.4.0 schema "0.2" files → schema "0.3", NEW in v0.5.0). Pre-flight detects canonical filenames with `schema_version: "0.2"` and no `_managed_by` field and emits `⚠ Upgrade Available`. Confirmation token: `confirm upgrade`. The skill rewrites the three canonical files adding `_managed_by: project-context-skill` and bumping `schema_version: "0.2"` → `"0.3"`. All record content preserved verbatim — frontmatter-only modification. No legacy-file deletion (filenames are unchanged).

See [`references/migration.md`](references/migration.md) for the full algorithm and [`references/preflight.md`](references/preflight.md) for the pre-flight protocol that routes between the two paths.

## Cross-skill awareness

project-context is aware of session-recap via the optional `related_session_recap` frontmatter field. v0.4.0 added first-class support for session-recap files as input to the `merge_external` operation: when you attach a session-recap output, the skill recognizes the format and extracts records using session-recap's known structure.

The two skills do not depend on each other. The `user-config.md` convention introduced in v0.4.0 is intended for cross-skill adoption — future skills follow the same pattern. v0.5.0 also implicitly establishes the `_managed_by` frontmatter field as a cross-skill convention; other skills that write to project knowledge can use the same field shape with their own identifiers.

## Troubleshooting

**The skill declined and recommended session-recap.** You are on a Claude Code or filesystem-based surface. The surface guard is intentional. Use session-recap for Claude Code; come back to project-context when you are in a Project.

**Pre-flight detects the wrong project.** State the project name explicitly at the prompt; the skill will use what you provide.

**The active file is approaching 50K tokens.** Invoke `compact` to demote weak records to the archive. If the file is over 80K, the skill will push harder on DEMOTE proposals in the default operation, but you should be running `compact` proactively.

**A demoted record was needed after all.** It lives in `project-context-archive.md` with a `restore_command` field. Invoke `restore arc-NNN` in a future session.

**The active file got corrupted or manually mis-edited.** Invoke `rebuild` to regenerate from the archive. The rebuild has a mandatory pre-commit review gate.

**Auto-mode is making changes I would have caught manually.** Turn off `merge_policy: auto` in `user-config.md` or chat-time. The audit trail (`audit.approval_mode: auto` on every auto record) lets you find what was created and review it later.

**Cross-platform invocation.** The Agent Skills standard means this folder works in any tool that supports it. Place the folder at the tool-specific skills location (e.g., `~/.claude/skills/project-context/` for Claude Code — though the surface guard will decline there).

## Roadmap

Parking-lot items, post-v0.5.0 plans, and platform dependencies are tracked in `ROADMAP.md`. Highlights: programmatic Project-file management (awaiting platform API), multi-collaborator audit, archive compaction / cold-storage tier, A-MEM-style link evolution, Zep-style bi-temporal tracking, MCP server packaging, the nc3-meta-skill-forge skill that will absorb the user-config and `_managed_by` conventions.

## License

Apache 2.0. See the top-level `LICENSE` file in the repository.
