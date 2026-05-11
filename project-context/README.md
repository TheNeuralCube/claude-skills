<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context

> Forward-grounding context for AI sessions inside a project.

## What this skill does

The project-context skill captures the decisions, constraints, entities, terminology, external references, open items, and state snapshot from the current chat into a structured markdown file the operator adds to their Claude Project, ChatGPT Project, or Copilot M365 Project. Future chats inside the same project load that file as a project file and start grounded — without the operator re-explaining context they already established.

It ships with two modes: **generate** (the default — produce a fresh project-context file from the current chat) and **consolidate** (merge multiple existing project-context files plus optional new content from the current chat into a single replacement file). A pre-flight check runs on every invocation, scans the project's existing project-context files, and proposes a mode with rationale before either mode runs.

## Who this skill is for

AI-literate professionals who work inside projects spanning multiple chat sessions on a recurring topic — quarterly business reviews, multi-week investigations, long-running design work, ongoing audits. The user is comfortable with YAML frontmatter, structured markdown, the concept of preservation tiers, and the idea that the file's primary audience is future AI sessions, not human readers.

The skill is **explicitly not** for non-AI-literate users. Such users are downstream consumers of output from chats that were grounded by project-context — they should not be invoking the skill directly. The path to less-technical users is the agent layer (post-v0.1.0), not this skill.

## When to use this skill (and when not to)

| Use **project-context** when | Use **session-recap** instead when |
|---|---|
| You're inside a Claude Project / ChatGPT Project / Copilot M365 Project. | You want a portable, exhaustive recap that travels outside any specific project. |
| You want lightweight forward-grounding for future chats in the same project. | You want a rich, human-readable handoff document. |
| You want to consolidate accumulated project files when they start stacking up. | You want a single comprehensive session record. |
| The audience for the output is future AI sessions. | The audience includes human collaborators who will read the file. |

You can run **both** skills on the same conversation. They serve different purposes and each tolerates the presence of the other. project-context can optionally cross-reference a session-recap file via the `related_session_recap` frontmatter field.

## How to invoke

Use any of these phrases in your chat:

**Generate mode (the default):**
- "create project-context" / "create project context"
- "save project context" / "save the project context"
- "generate project-context"
- "snapshot project context"
- "ground this project" / "ground the project"
- "project-context this" / "project context this conversation"
- "build project-context file"

**Consolidate mode:**
- "consolidate project-context" / "consolidate project context"
- "consolidate project-context files"
- "merge project-context files"
- "compress project-context"

**Ambiguous (pre-flight will propose a mode and ask):**
- "run project-context"
- "project context"
- "project-context skill"

The pre-flight check runs first regardless of phrase. It identifies your project, lists the existing project-context files in it, assesses whether consolidation is warranted, and confirms a mode before generating anything.

## Output format

The skill produces a markdown file with:

- **YAML frontmatter** declaring file type, schema version, project name, session topic, sessions covered, source files (for consolidations), cross-references to related files including an optional session-recap pointer, and governance metadata (sensitivity, audience, retention, governance frameworks, custom governance keys). All governance fields are optional.
- **Seven body sections**, always in this order: Decisions, Constraints, Entities, Terminology, External references, Open items, State snapshot. Empty sections show a placeholder line; missing sections are not allowed.
- **Per-record metadata** in inline brackets: `[tier: full | summary | transient]` and `[categories: tag1, tag2]`. Section tier defaults reduce verbosity — most records omit the `[tier: ...]` bracket.
- **Three preservation tiers**: `full` (preserved verbatim through consolidation), `summary` (compressed when stale), `transient` (dropped on consolidation).
- **Open multi-tag categories** assigned by the model based on record content.

For the full schema, see [`references/schema.md`](references/schema.md). For governance metadata details, see [`references/governance.md`](references/governance.md). For complete examples, see [`references/examples/example-fresh-project-context.md`](references/examples/example-fresh-project-context.md) and [`references/examples/example-consolidated-project-context.md`](references/examples/example-consolidated-project-context.md).

## Filename convention

```
YYYY-MM-DD-project-context.md                          (no topic)
YYYY-MM-DD-project-context-{topic-slug}.md             (with topic)
YYYY-MM-DD-project-context-consolidated.md             (consolidate-mode output)
```

Same-day same-topic invocations merge into the existing file. Same-day different-topic invocations produce separate files.

## Customization with org-config.md

The skill follows an upstream-skill-plus-org-config-layer architecture. The upstream skill (this folder) works out of the box with safe-permissive defaults. Organizations that want to customize defaults — sensitivity floor, audience vocabulary, retention policy, category taxonomy, additional trigger phrases, downstream skill chaining — drop an `org-config.md` file alongside `SKILL.md`.

The template is at [`references/org-config-template.md`](references/org-config-template.md). Copy it, populate the values your organization needs, and the skill will load it on every invocation. The upstream skill ships with no populated `org-config.md`; if absent, upstream defaults apply unchanged.

What `org-config.md` can change:

- File-level governance defaults (sensitivity, audience, retention, frameworks).
- Whether the model is constrained to a fixed category vocabulary.
- Section-level tier defaults.
- Reminders or instructions printed after generate or consolidate completes.
- Additional trigger phrases.
- Default project name and filename topic behavior.

What it cannot change: the seven body sections, the schema fields, or anything that would break schema validity.

## Cross-skill awareness

project-context is aware of the session-recap skill via an optional `related_session_recap` frontmatter field. If you have run session-recap on the same conversation, you can reference its filename in this field; downstream AI sessions reading the project-context file can then optionally fetch the richer session-recap if they need more depth. The reverse pointer (session-recap referencing project-context) is owned by the session-recap skill, not this one.

The two skills do not depend on each other. Either can be run without the other. The cross-reference is metadata only.

## Troubleshooting

**Pre-flight detects the wrong project.** The skill identifies the project from the runtime's project-container signal. If the runtime exposes a different project name than expected, override at the prompt: state the project name explicitly and the skill will use it.

**Pre-flight is noisy on every invocation.** v0.1.0 does not allow skipping pre-flight. If the friction is real, file a feature request for a `--no-preflight` flag in v0.2.0+.

**Consolidation produces too-large output.** The skill warns when aggregate output approaches the project's file-size budget. Options: tighten compression on summary-tier records, drop borderline summary-tier records the operator confirms are stale, or split the consolidation into two output files. See [`modes/consolidate.md`](modes/consolidate.md) for the full list of failure-mode handlers.

**The model assigned categories the operator dislikes.** Either edit the file by hand (it is plain markdown), or set `categories.constrain_to_vocabulary: true` in `org-config.md` with the allowed list. Future invocations will respect the vocabulary.

**Generated file lands in an unexpected location.** The skill writes to whatever path the runtime exposes for generated artifacts and presents the file via the runtime's file-presentation mechanism. The exact path is environment-dependent. The operator downloads the file and adds it to the project manually; v0.1.0 does not have a programmatic path to add files to a Claude Project.

**Cross-platform invocation.** The Agent Skills standard means this folder works in any tool that supports it. Place the folder at the tool-specific skills location (e.g., `~/.claude/skills/project-context/` for Claude Code) and the skill is available.

## License

Apache 2.0. See the top-level `LICENSE` file in the repository.
