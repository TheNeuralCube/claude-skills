<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context — usage walkthrough

This file is a user-facing walkthrough of the v0.4.0 three-file workflow. It complements `README.md` (which explains what the skill does) and `operations/*.md` (which contain the operation logic) with concrete step-by-step usage. Read this if you are setting up the skill in a new Project for the first time, or returning after using the v0.1.x-v0.3.x version.

## Prerequisites

You have:

1. A Claude Project (or ChatGPT Project / Copilot M365 Project) where this skill will live.
2. The `project-context` skill installed via Agent Skills (the `.skill` archive uploaded to your Claude tenant or placed in your `~/.claude/skills/` directory).
3. A chat session inside the Project where the skill can run.

If you are on Claude Code, this skill will decline and recommend `session-recap`. That is by design — see `SKILL.md` pre-flight section.

## First run (new Project)

The first time you invoke the skill in a new Project, it creates all three files eagerly with placeholder blocks.

1. **Start a chat in the Project.** Have at least one substantive exchange — a decision, a constraint, an entity mentioned by name, etc.
2. **Invoke the skill.** Any of these works:
   - "create project-context"
   - "save project context"
   - "ground this project"
   - "snapshot project context"
3. **The skill runs pre-flight.** It detects the Project (correctly identifying you are in one). It finds no existing project-context files, so it does NOT trigger migration. It loads any `user-config.md` or `org-config.md` you have in the Project (none on first run, so it uses upstream defaults).
4. **The skill parses the conversation.** It produces candidate records (decisions, constraints, current state, etc.).
5. **The skill applies the hybrid brake.** New records with no similar neighbors auto-apply. (On first run, every record has no neighbors, so they all auto-apply.)
6. **The skill writes three files.** All three are created with `update_count: 1`, `schema_version: "0.2"`, and frontmatter populated. Records you generated populate the active file (`project-context.md`) and entities file (`entities.md`). The archive (`project-context-archive.md`) is created with one frontmatter checkpoint but no body records yet.
7. **The skill emits the operator brief.** A summary of what was created, plus instructions: download these three files, upload them to your Project.
8. **You download and upload.**

That's the bootstrap. From here on, every session continues against these three files.

## Routine session (after bootstrap)

The everyday workflow once you have the three files in place.

1. **Chat as normal.** Have a substantive exchange.
2. **Invoke the skill.** "create project-context", "save project context", or any equivalent.
3. **Pre-flight loads the existing three files** and detects their `schema_version: "0.2"`. No migration. Configuration loaded if `user-config.md` is present.
4. **The skill parses the conversation** for candidates.
5. **The skill classifies each candidate** against existing records using the five-op merge classifier:
   - **ADD** — no similar neighbor → new record.
   - **UPDATE** — existing record's meaning evolves → revise in place, archive prior.
   - **NOOP** — duplicate or reinforcement → increment `times_seen`, update `last_seen_update`.
   - **DEMOTE** — record's score dropped below threshold → move to archive.
   - **SUPERSEDE** — new record contradicts an existing one → archive old, add new.
6. **The hybrid brake applies.** ADD-no-neighbor and NOOP auto-apply. UPDATE, DEMOTE, SUPERSEDE are gated for your approval.
7. **You see a proposal block** with the gated changes. Up to 10 proposals (configurable). Reply with:
   - `all` — approve everything.
   - `skip 3 4` — approve everything except #3 and #4.
   - `only 1 2` — approve only those.
   - `explain 5` — show the source quote and the existing record for proposal #5.
   - `set importance 7=9` — override the importance score on proposal #7 to 9.
   - `cancel` — abort the session.
8. **The skill writes the updated files.**
9. **You download, upload, replace.** The skill's brief lists which files changed and which were unchanged.

## Auto-mode session

When you are in a hurry and trust the skill's judgment.

Two ways to activate:

- Set `merge_policy: auto` in `user-config.md` (persists across sessions until you change it).
- Say "use auto-mode" or "enable auto-mode" at chat time (per-session only).

When auto-mode activates, the skill fires a published warning (`operations/default.md` section 8.1) explaining the trade-off and asking you to confirm. The warning fires once per session.

Three response options:

- **Explicit yes** ("yes", "proceed", "go ahead") — auto-mode active, every record stamped `audit.warning_response: acknowledged`.
- **Explicit no** ("no", "cancel", "use hybrid") — auto-mode cancelled, fall back to hybrid for this session.
- **Passive / silence / unclear** — auto-mode proceeds, records stamped `audit.warning_response: passive`. This is intentional: the operator chose this behavior in the workshop because explicit-acknowledgment-required would defeat the purpose of "I'm in a hurry."

Every record added under auto-mode carries:

- A literal `[AUTO]` prefix on `content` (visible in the file).
- `audit.approval_mode: auto`.
- `audit.approved_by`: your `user_identifier` from `user-config.md`, or `null` if unset.

The audit trail exists so quality issues can be diagnosed later. It is an audit feature, not a blame feature.

## Compact session

When the active file is getting bloated and you want to clean up.

1. **Notice the file size.** The operator brief mentions when `project-context.md` is over the soft warning (default 50K tokens). Or just notice that scrolling through it is unpleasant.
2. **Invoke compact.** "compact this", "trim the project context", or "consolidate project-context" (legacy phrase routes here).
3. **The skill scores every active record** using the formula in `references/scoring.md`.
4. **It proposes DEMOTE** for everything below the threshold (default `weight < 5`). The proposal cap may be raised because you explicitly asked for batch demotion.
5. **You review and approve.** Same grammar as routine sessions.
6. **The skill writes the updated active file and archive.**
7. **You download, upload, replace.**

`compact` does not parse the conversation. It operates on the existing active file only.

## Rebuild session

When the active file got corrupted, manually mis-edited, or you want to apply new scoring coefficients retroactively.

1. **Invoke rebuild.** "rebuild", "rebuild from archive", "reset from archive", or "regenerate project context".
2. **The skill scores every archive record** using the current scoring algorithm.
3. **It builds a candidate active file** from archive records whose weight is at or above threshold.
4. **MANDATORY: it shows you the rebuilt file BEFORE committing.** Auto-mode does not bypass this gate. The reason: rebuild is destructive to the active file, and getting it wrong replaces good data with stale archive records.
5. **You type `approve` (or `accept`, `yes`)** to commit, or anything else to cancel.
6. **The skill writes the rebuilt active file and updates the archive's checkpoint log.**
7. **You download, upload, replace.**

`rebuild` does not touch `entities.md`.

## Merge-external session

When you want to import context from a file rather than the conversation.

1. **Attach the file in the chat** (e.g., a session-recap output, a vision document, a spec).
2. **Invoke the skill.** "merge this into project context", "process this attached file", "import this session-recap", or any variation. The skill also auto-routes to `merge_external` if a file is attached, even with a generic invocation phrase.
3. **The skill identifies the file type.** Recognized structured artifacts (like session-recap output) get structure-specific extraction; unstructured markdown gets best-effort parsing by section header.
4. **The skill parses the file for candidates and classifies them** (same as default operation).
5. **You see the proposal block** with file-aware source references (the source quote field includes the filename and locator).
6. **You approve.** Same grammar as routine sessions.
7. **The skill writes the updated files.** Download, upload, replace.

## Migration session (one-time, after upgrading from v0.1.x-v0.3.x)

If you used project-context v0.1.x through v0.3.2 in this Project, you have dated files (`2026-04-15-project-context.md`, etc.) accumulated.

1. **Invoke the skill** with any phrase.
2. **Pre-flight detects the legacy dated files.** It also detects the absence of v0.4.0 files (`project-context.md`, `entities.md`, `project-context-archive.md`).
3. **The skill triggers migration.** It parses every legacy file, stamps lifecycle fields with the legacy `created` date, infers `importance` from tier (`full` → 8, `summary` → 5, `transient` → DROPPED), scores everything, and partitions into active and archive.
4. **The skill writes the three new files** with `update_count: 0` and a frontmatter `checkpoints` entry summarizing the migration.
5. **The skill emits a migration brief** listing each legacy file by exact filename with required order of operations:
   - **(a)** download the three new files,
   - **(b)** verify they look correct,
   - **(c)** delete the listed legacy files from the Project,
   - **(d)** upload the three new files.
6. **Do them in that order.** If you delete first and the migration is wrong, you lose the source. The skill cannot delete files itself.

Migration is one-time. Re-running the skill on a migrated Project skips migration (it detects `schema_version: "0.2"` and proceeds normally).

## Setting up `user-config.md`

If you want to override defaults for your personal workflow:

1. **Copy** [`references/user-config-template.md`](references/user-config-template.md) as a starting point.
2. **Edit it.** Uncomment the settings you want to change. Every setting has a prose comment explaining what it does.
3. **Upload it to your Project** as `user-config.md`.
4. **Next invocation picks it up.**

If your settings conflict with `org-config.md` (when `org-config.md` sets `allow_user_auto: false` and your `user-config.md` sets `merge_policy: auto`), the skill warns you in the brief and falls back to the org policy.

## Setting up `org-config.md`

If you administer the skill for an organization:

1. **Copy** [`references/org-config-template.md`](references/org-config-template.md).
2. **Edit it.** Govern at the org level: governance defaults, scoring tweaks, additional trigger phrases, downstream chaining reminders.
3. **Distribute it.** Each user uploads it to their Project alongside the skill folder, or your tenant administrator drops it in the org-level skill deployment if supported.

Org-config is loaded after the skill defaults and before user-config. User overrides win for everything except the `allow_user_auto` veto.

## When things go wrong

- **Surface guard fires (Claude Code).** Use session-recap instead. project-context is not for Claude Code.
- **Pre-flight detects the wrong Project.** State the project name explicitly at the prompt.
- **You don't see all your records in the active file.** Some may have decayed past the demotion threshold and moved to the archive. Check `project-context-archive.md`. Use `rebuild` if many records were demoted incorrectly.
- **A demoted record needs to come back.** Look up its `arc-NNN` ID in the archive. Run `restore arc-NNN` in a future session.
- **The skill keeps proposing the same record over and over.** It probably should have been merged into an existing record but the classifier is missing the match. Either reinforce the existing record by mentioning it more explicitly in chat, or override at proposal time.
- **Auto-mode produced records you would have rejected.** Filter the active file by `audit.approval_mode: auto` (or the `[AUTO]` prefix on `content`) to find them. Edit or DEMOTE the bad ones. Reconsider whether auto-mode is right for your workflow.

## Where to learn more

- The schema contract: `references/schema.md`.
- The scoring algorithm: `references/scoring.md`.
- The full operation logic: `operations/*.md`.
- Default values: `references/defaults.md`.
- Schema history: `references/schema-changelog.md`.
- Migration details: `references/migration.md`.
- Governance metadata: `references/governance.md`.
- Configuration templates: `references/user-config-template.md`, `references/org-config-template.md`.
- Examples: `references/examples/`.
- What's on the radar: `ROADMAP.md`.
