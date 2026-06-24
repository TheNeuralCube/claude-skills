<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context — usage walkthrough

This file is a user-facing walkthrough of the three-file workflow (the three files use versioned `pc-NNNN-*` names at `schema_version: "0.5"`). It complements `README.md` (which explains what the skill does) and `operations/*.md` (which contain the operation logic) with concrete step-by-step usage. Read this if you are setting up the skill in a new Project for the first time, or returning after using the v0.1.x-v0.3.x version, or upgrading from v0.4.0 (see "Upgrading from v0.4.0" below), v0.5.0 (see "Upgrading from v0.5.0" below), or v0.6.0 (see "Upgrading from v0.6.0" below).

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
3. **The skill runs pre-flight.** It detects the Project (correctly identifying you are in one). It finds no existing project-context files, so it does NOT trigger migration. It auto-creates `user-config.md` and `org-config.md` from the templates if they are absent, with `[tbd]` placeholders for operator-supplied fields. Pre-flight emits the `✓ Fresh Project` verdict.
4. **The skill prompts for topology role declaration (NEW in v0.6.0).** Before generating output, the skill emits LOCKED TEXT 1 (per `references/preflight.md` section 13.1) asking you to declare the project's topology role: `hub` (owns a spoke inventory), `spoke-dev` (a development artifact like a skill referencing a hub), `spoke-solution` (a delivered solution referencing a hub), or `standalone` (no hub relationship). Reply with the role name. If you declare a spoke role, the skill also asks for `hub_reference` and `hub_version` via LOCKED TEXT 2.
5. **The skill parses the conversation.** It produces candidate records (decisions, constraints, current state, etc.).
6. **The skill applies the hybrid brake.** New records with no similar neighbors auto-apply. (On first run, every record has no neighbors, so they all auto-apply.)
7. **The skill writes three files.** All three are created with `generation: 1`, `update_count: 1`, `schema_version: "0.5"`, the `topology` block populated from your role declaration, and frontmatter populated. Records you generated populate the active file (`pc-0001-context.md`) and entities file (`pc-0001-entities.md`). The archive (`pc-0001-archive.md`) is created with one frontmatter checkpoint but no body records yet. For `role: hub`, an empty `## Spoke Inventory` section appears in the body of `pc-0001-context.md` immediately after frontmatter.
8. **The skill emits the operator brief.** A summary of what was created, plus instructions: download these three files, upload them to your Project.
9. **You download and upload.**

That's the bootstrap. From here on, every session continues against these three files.

## Routine session (after bootstrap)

The everyday workflow once you have the three files in place.

1. **Chat as normal.** Have a substantive exchange.
2. **Invoke the skill.** "create project-context", "save project context", or any equivalent.
3. **Pre-flight loads the existing files** and detects a `pc-NNNN-*` set at `schema_version: "0.5"` with `generation` and a `topology` block (the current contract). No migration. (If instead it finds old canonical names at `schema_version: "0.4"`, that is the v0.6.0 format and routes to Scenario G, the v0.6.0 to v0.7.0 upgrade, not a routine run.) Configuration loaded if `user-config.md` is present. If the project is `role: spoke-*` and the attached Hub instructions filename version differs from the spoke's declared `topology.hub_version`, pre-flight also emits the `⚠ Stale Spoke` informational verdict (not blocking; the operation proceeds and post-flight surfaces a one-line recommendation to use project-creator upgrade mode).
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

`rebuild` does not change the **content** of the entities file, but it re-stamps that file to the new `generation` and re-writes it under the new `pc-NNNN-entities.md` name so the canonical set stays at one counter (per `operations/rebuild.md`).

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
2. **Pre-flight detects the legacy dated files.** It also detects the absence of canonical three-file system (`project-context.md`, `entities.md`, `project-context-archive.md`).
3. **The skill triggers migration (Scenario D).** It parses every legacy file, stamps lifecycle fields with the legacy `created` date, infers `importance` from tier (`full` → 8, `summary` → 5, `transient` → DROPPED), scores everything, and partitions into active and archive.
4. **The skill solicits topology role declaration (NEW in v0.6.0).** Before any file write, the skill emits LOCKED TEXT 1 asking you to declare the project's topology role. Reply with `hub`, `spoke-dev`, `spoke-solution`, or `standalone`. If you declare a spoke role, the skill also asks for `hub_reference` and `hub_version` via LOCKED TEXT 2.
5. **The skill writes the three new files** at `schema_version: "0.4"` with `update_count: 0`, the operator-declared `topology` block, and a frontmatter `checkpoints` entry summarizing the migration. v0.6.0 retargets legacy migration to produce schema "0.4" directly; v0.1-era projects skip schemas "0.2" and "0.3" entirely. Then re-invoke for Scenario G (see "Upgrading from v0.6.0" below) to reach the current schema "0.5" and `pc-NNNN-*` naming.
6. **The skill emits a migration brief** listing each legacy file by exact filename with required order of operations:
   - **(a)** download the three new files,
   - **(b)** verify they look correct (and that the topology block reflects your declaration),
   - **(c)** delete the listed legacy files from the Project,
   - **(d)** upload the three new files.
7. **Do them in that order.** If you delete first and the migration is wrong, you lose the source. The skill cannot delete files itself.

Migration is one-time per legacy file. After you complete the brief's ordering, re-running the skill finds no legacy files. The resulting schema-0.4 set (`schema_version: "0.4"`, `_managed_by: project-context-skill`, a `topology` block, and no `pc-NNNN-*` files) is not the current contract: pre-flight emits `⚠ Upgrade Available (v0.6.0 to v0.7.0)` (Scenario G) and routes to the generation/naming upgrade (see "Upgrading from v0.6.0" below). Only a `pc-NNNN-*` set at `schema_version: "0.5"` skips migration and proceeds normally.

## Upgrading from v0.4.0

If your project already has the v0.4.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at `schema_version: "0.2"` with no `_managed_by` field), pre-flight detects this on first invocation and emits the verdict `⚠ Upgrade Available` (Scenario E) rather than proceeding with the requested operation.

To complete Scenario E, type the confirmation token `confirm upgrade`. The skill then rewrites the three canonical files with two frontmatter changes:

- Adds `_managed_by: project-context-skill` near `schema_version`.
- Changes `schema_version: "0.2"` → `schema_version: "0.3"`.

All record content — every `dec-`, `con-`, `csn-`, `opn-`, `trm-`, `ref-`, `ent-`, and `arc-` entry — is preserved verbatim. Lifecycle fields, audit metadata, timestamps, scores, links, the archive's `checkpoints` array: none are modified. The upgrade is frontmatter-only.

After Scenario E, the files are at schema "0.3" as an intermediate state. **Re-invoke the skill** to reach schema "0.4" via Scenario F (the next section), then re-invoke once more for Scenario G to reach the current schema "0.5" and `pc-NNNN-*` naming; pre-flight will detect the schema-0.3-without-topology state and emit `⚠ Upgrade Available (v0.5.0 to v0.6.0)`. Download and upload the schema-0.3 files between the invocations only if your platform requires file refresh between runs.

See `references/preflight.md` for the full pre-flight protocol and `references/migration.md` section 9 for the Scenario E upgrade migration algorithm.

## Upgrading from v0.5.0

If your project already has the v0.5.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at `schema_version: "0.3"` with `_managed_by: project-context-skill` but no `topology` block), pre-flight detects this on first invocation and emits the verdict `⚠ Upgrade Available (v0.5.0 to v0.6.0)` (Scenario F) rather than proceeding with the requested operation.

To complete Scenario F, type the confirmation token `confirm v0.6.0 upgrade`. The skill then rewrites the three canonical files with two frontmatter changes:

- Adds a `topology` block with `role: "unclassified"` default, all relationship fields null, `declared_by: "skill-default"`, and `declared_at: <current timestamp>`.
- Changes `schema_version: "0.3"` → `schema_version: "0.4"`.

All record content is preserved verbatim. Lifecycle fields, audit metadata, timestamps, scores, links, the archive's `checkpoints` array, the per-record audit block: none are modified. The upgrade is frontmatter-only.

After the file writes complete, the skill emits LOCKED TEXT 1 (per `references/preflight.md` section 13.1) asking you to declare the project's topology role. Reply with `hub`, `spoke-dev`, `spoke-solution`, or `standalone`. The skill then writes the declared role to `topology.role` in `project-context.md`, sets `declared_by: "operator"`, and (for `role: hub`) creates an empty `## Spoke Inventory` section in the body. If you declare a spoke role, the skill asks for `hub_reference` and `hub_version` via LOCKED TEXT 2; supply both and the skill stamps them onto the topology block.

If you decline to declare a role (no response or off-topic), the topology stays `unclassified` and the skill re-prompts on next invocation. No data corruption; the skill operates normally with an unclassified topology.

After Scenario F, download the three updated files from the chat and re-upload them to your Project, replacing the schema-0.3 versions. The filenames are unchanged, so the upload-replace flow handles file management — there is no legacy-file-deletion step. After uploading, re-invoke once more for Scenario G (next section) to reach the current schema "0.5" and `pc-NNNN-*` naming.

See `references/preflight.md` for the full pre-flight protocol (including topology validation in section 10, stale-spoke detection in section 11, audit trigger handler in section 12, and role-declaration prompts in section 13) and `references/migration.md` section 10 for the Scenario F upgrade migration algorithm.

## Upgrading from v0.6.0

If your project already has the v0.6.0 three-file system (`project-context.md`, `entities.md`, `project-context-archive.md` at `schema_version: "0.4"` with `_managed_by: project-context-skill` and a `topology` block, and no `pc-NNNN-*` files), pre-flight detects this on first invocation and emits the verdict `⚠ Upgrade Available (v0.6.0 to v0.7.0)` (Scenario G). This is a destructive operation: pre-flight confirms model setup before proceeding (run on the strongest thinking-capable model with extended thinking).

To complete Scenario G, type the confirmation token `confirm v0.7.0 upgrade`. The skill rewrites the three context files under versioned names:

- Renames `project-context.md` to `pc-0001-context.md`, `entities.md` to `pc-0001-entities.md`, and `project-context-archive.md` to `pc-0001-archive.md`.
- Adds `generation: 1`.
- Changes `schema_version: "0.4"` to `schema_version: "0.5"`.
- Preserves `update_count`, every per-record counter, the audit metadata, and the `topology` block verbatim. No record content changes; the `generation` identity counter is distinct from the retained `update_count` scoring counter.
- Applies the config treatment to `user-config.md`, `org-config.md`, and `platform-specific-parameters.md` (adds the `config_editable`/`configure_with` header, bumps their schema to "0.5"; relocates them to `config/` on filesystem platforms).

After the writes, download the `pc-0001-*` set, verify it, upload it to your Project, then delete the old-named files (`project-context.md`, `entities.md`, `project-context-archive.md`) per the set-integrity directive in the post-flight summary.

See `references/migration.md` section 11 for the Scenario G algorithm and `references/preflight.md` section 4.6 for the destructive-tier model-setup gate.

## Setting up `user-config.md`

The skill auto-creates `user-config.md` from [`config/user-config.md.template`](config/user-config.md.template) on first invocation if absent, with `[tbd]` placeholders for operator-supplied required fields. The skill reads it by base name (in `config/` on filesystem platforms; from flat project knowledge on web). To populate it (or reconfigure it via the interview in `references/configure.md`):

1. **Open the auto-created `user-config.md`** in your Project knowledge.
2. **Edit the `[tbd]` placeholders** for the three required fields (`operator.primary_name`, `defaults.hub_project_name`, `defaults.preferred_platform`) and any other fields you want to override.
3. **Re-upload it to your Project**, replacing the auto-created version.
4. **Next invocation picks it up.**

Pre-flight notes if any required fields still read `[tbd]` so you know what remains to populate.

If your settings conflict with `org-config.md` (when `org-config.md` sets `allow_user_auto: false` and your `user-config.md` sets `merge_policy: auto`), the skill warns you in the brief and falls back to the org policy.

## Setting up `org-config.md`

The skill auto-creates `org-config.md` from [`config/org-config.md.template`](config/org-config.md.template) on first invocation if absent. If you administer the skill for an organization:

1. **Open the auto-created `org-config.md`** (or copy the template directly if you want to deploy ahead of first invocation).
2. **Edit it.** Populate the required `[tbd]` fields (`org.name`, `org.type`, `org.tenant`, `compliance.default_sensitivity`) and govern at the org level: governance defaults, scoring tweaks, additional trigger phrases, downstream chaining reminders.
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
- The topology schema, role definitions, spoke inventory format, audit trigger semantics, hybrid topology rules, validation rules: `references/topology.md`.
- The scoring algorithm: `references/scoring.md`.
- The full operation logic: `operations/*.md`.
- Default values: `references/defaults.md`.
- Schema history: `references/schema-changelog.md`.
- Migration details (all four paths: Scenario D legacy, Scenario E v0.4.0 upgrade, Scenario F v0.5.0 to v0.6.0 topology upgrade, Scenario G v0.6.0 to v0.7.0 generation/naming upgrade): `references/migration.md`.
- Governance metadata: `references/governance.md`.
- Configuration templates (operator-editable, in `config/`): `config/user-config.md.template`, `config/org-config.md.template`. Interview mechanics: `references/configure.md`.
- Multi-platform parameters (read by the model advisory; also consumed by project-creator): `config/platform-specific-parameters.md`.
- Examples: `references/examples/`.
- What's on the radar: `ROADMAP.md`.
