---
name: project-context
version: 0.7.0
description: Capture forward-grounding context from the current chat into the three-file project-context system (active, entities, archive) so future chats start grounded. Use whenever the operator says "create project-context", "create project context", "save project context", "save the project context", "generate project-context", "snapshot project context", "ground this project", "ground the project", "project-context this", "project context this conversation", "build project-context file", "consolidate project-context", "consolidate project context", "consolidate project-context files", "merge project-context files", "compress project-context", "run project-context", "project context", "project-context skill", "compact this", "trim the project context", "rebuild", or "regenerate project context". v0.6.0 adds audit triggers (Hub projects only): "audit spoke projects", "audit the spokes", "which spokes are stale", "show me spoke staleness", "spoke inventory audit", "run spoke audit".
---

## Protocol

This skill operates under a mandatory pre-flight protocol. Before any output
is generated, before any other section of this skill applies, you MUST:

1. Complete the pre-flight check defined in references/preflight.md.
2. Emit the pre-flight report block (per references/preflight.md format) as
   the first content in your response to the operator.
3. Where the verdict requires operator confirmation (per the report's
   "To proceed" line), wait for the operator's confirmation token. Do not
   generate output, do not write to project knowledge, do not propose files
   until the matching token is received.

Failure to complete pre-flight before generation is a protocol violation,
not an optimization. Operator urgency, perceived skill execution context,
or any other condition does not license skipping pre-flight. If project
knowledge access fails and pre-flight cannot complete, refuse to proceed
and surface the failure to the operator.

All operations described in subsequent sections (default, merge_external,
compact, rebuild, migration, upgrade) are conditional on pre-flight
completion. Do not read further as actionable instruction until pre-flight
has emitted its report and any required confirmation has been received.

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# project-context (v0.7.0)

A thin-router skill. This file detects the invocation, runs the mandatory pre-flight protocol (`## Protocol` above), and delegates to one of four operation files. Operation logic lives in `operations/`. Schema, scoring, defaults, migration, governance, configuration interview mechanics, and the pre-flight / post-flight protocol live in `references/` (skill-owned). Operator-editable configuration lives in `config/` (`user-config.md`, `org-config.md`, `platform-specific-parameters.md`), read by base name.

v0.4.0 was a major architectural pivot from v0.1.x-v0.3.x: the dated single-file output was replaced by a three-file rolling system; the two modes became four operations (default, merge_external, compact, rebuild); the skill gained a five-op merge classifier (ADD, UPDATE, NOOP, DEMOTE, SUPERSEDE) with a hybrid brake. v0.5.0 closed the protocol-enforcement gap (the 2026-05-19 postmortem): pre-flight became a structural gate, schema bumped to "0.3" with a new REQUIRED `_managed_by: project-context-skill` field, and a symmetric post-flight summary. v0.6.0 added hub-spoke governance awareness: schema "0.4" with a REQUIRED `topology` block, an audit trigger (Hub projects), stale-spoke detection, and Scenario F migration. **v0.7.0 inherits all of that and adds:** versioned, prefix-unified file identity (`pc-NNNN-{context,entities,archive}.md` with a `generation` field; schema bumps to "0.5"; `update_count` is RETAINED as the separate scoring counter); an operation-start model advisory and a two-tier confirmation gate; the config/references separation convention; an expanded `platform-specific-parameters.md`; and Scenario G migration from v0.6.0 (schema 0.4) to v0.7.0 (schema 0.5). See `CHANGELOG.md` for the full change history.

**pc-NNNN recognition note.** The skill recognizes its managed context set by the `pc-NNNN-*` name pattern AND the `_managed_by: project-context-skill` marker together. `NNNN` is the shared-set `generation` counter; the first generation is `pc-0001-*`. Counter assignment, the confirmed-empty rule (never `0001` on absence of evidence), and the generation self-consistency check live in `references/preflight.md` sections 3.4 and 3.5.

Key references the router and operations consume: `references/preflight.md` (pre-flight algorithm, counter assignment, generation self-consistency, model advisory and two-tier gate, report block, token catalog, post-flight summary and set-integrity directive, topology validation, stale-spoke detection, audit trigger handler, role-declaration prompts), `references/schema.md` (data shape, `schema_version: "0.5"`, `generation`, naming contract, config-file frontmatter), `references/topology.md` (topology metadata schema, role definitions, spoke inventory, audit semantics, validation rules), `references/scoring.md` (formula and coefficients, keyed off the retained `update_count`), `references/operations.md` (classifier and post-pre-flight runtime steps), `references/migration.md` (legacy v0.1-era migration, Scenario E, Scenario F, and the new Scenario G generation/naming upgrade), `references/configure.md` (config interview mechanics; single owner), `references/schema-changelog.md` (version history and Supported Schemas matrix), `references/defaults.md` (single source of truth for tunables), `config/platform-specific-parameters.md` (per-platform capability and limit parameters, read by base name; consumed by the model advisory).

## Model-assumption disclosure

This skill is optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking, equivalents). The active-file token budgets (target 30K, soft warning 50K, hard ceiling 80K) assume substantial effective context. On lighter models, data integrity may degrade as files approach the hard ceiling.

## Files in this skill

```
project-context/
├── SKILL.md                                          (this file — router, ## Protocol gate, and surface guard)
├── README.md
├── CHANGELOG.md
├── ROADMAP.md
├── USAGE.md
├── operations/
│   ├── default.md                                   (default operation: parse conversation, classify, propose, write)
│   ├── merge_external.md                            (parse an attached file or external artifact instead of the conversation)
│   ├── compact.md                                   (aggressively demote weak active records)
│   └── rebuild.md                                   (rebuild active file from archive; mandatory pre-commit review)
├── references/                                       (skill-owned; convention P4)
│   ├── preflight.md                                 (pre-flight algorithm, counter assignment, generation self-consistency, model advisory + two-tier gate, report block, token catalog, post-flight + set-integrity directive, topology validation, stale-spoke detection, audit trigger handler, role-declaration prompts)
│   ├── schema.md                                    (file-level + per-record schema, schema_version "0.5", generation field, pc-NNNN naming contract, config-file frontmatter, _managed_by, topology block)
│   ├── schema-changelog.md                          (version-by-version schema history, Supported Schemas matrix, drift detection)
│   ├── topology.md                                  (topology metadata schema, role definitions, spoke inventory format, audit trigger semantics, hybrid topology rules, validation rules)
│   ├── scoring.md                                   (the formula, coefficients, demotion threshold; keyed off the retained update_count)
│   ├── operations.md                                (cross-operation runtime logic and post-pre-flight steps)
│   ├── migration.md                                 (legacy v0.1-era migration + Scenario E + Scenario F + Scenario G generation/naming upgrade)
│   ├── configure.md                                 (v0.7.0: single owner of config interview mechanics; batch, confirm, diff, write, compliance flag)
│   ├── defaults.md                                  (single source of truth for every configurable default; stays skill-owned)
│   ├── governance.md                                (governance metadata framework)
│   └── examples/
│       ├── example-project-context.md
│       ├── example-entities.md
│       ├── example-project-context-archive.md
│       └── example-user-config.md
└── config/                                           (operator-editable; convention P4; read by base name)
    ├── user-config.md.template                      (per-user override layer; cross-skill convention)
    ├── org-config.md.template                       (org-scope override layer)
    ├── platform-specific-parameters.md              (live per-platform capability and limit parameters; consumed by the model advisory and project-creator)
    └── platform-specific-parameters.md.template     (pristine shipped copy of the platform parameters)
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

   All 19 of the v0.1.0 trigger phrases preserved verbatim above. The v0.1.0 `consolidate` phrases route to v0.6.0 `compact` (the closest behavioral analog) — the operator can override during pre-flight if they intended `rebuild` instead. The six v0.6.0 audit trigger phrases (`audit spoke projects`, `audit the spokes`, `which spokes are stale`, `show me spoke staleness`, `spoke inventory audit`, `run spoke audit`) are registered in the description field above and route to the audit trigger handler in `references/preflight.md` section 12. The audit handler refuses on non-Hub projects.

3. **Loads the operation file** (`operations/<operation>.md`) and runs its body to completion.
4. **Applies configuration overrides** by loading `user-config.md` and `org-config.md` by base name if present in the project (`config/<name>.md` on filesystem platforms; `<name>.md` from flat project knowledge on web; never a hardcoded `config/` path). Resolution order is user > org > skill defaults from `references/defaults.md`. The configure flow (operator-driven regeneration of a config file) is owned by `references/configure.md`.

The router itself does not parse the conversation, classify records, write files, or apply scoring. It only detects intent, runs the surface guard, and hands off.

## Default behavior

When neither `user-config.md` nor `org-config.md` is present, the skill applies the upstream defaults documented in `references/defaults.md`. Highlights:

- `merge_policy: hybrid` (auto-apply ADD and NOOP; gate UPDATE, DEMOTE, SUPERSEDE).
- `proposal_cap_per_session: 10`.
- `active_file_token_target: 30000`, `soft_warning: 50000`, `hard_ceiling: 80000`.
- Scoring coefficients per `references/scoring.md` (`alpha: 1.5`, `beta: 1.0`, `gamma: 5.0`, `delta: 2.0`, `epsilon: 0.5`, `lambda: 0.0347`, `demotion_threshold: 5`).
- `sensitivity: internal`, `retention: standard` (active/entities) or `indefinite` (archive).
- Surface guard always on. Migration detection always on.

## Pre-flight surface guard

The authoritative pre-flight protocol (algorithm, report block, token catalog, completion criteria, infrastructure-failure handling, and the symmetric post-flight summary) lives in `references/preflight.md` and is gated structurally by the `## Protocol` section above. This section restates only the surface guard inline because it runs upstream of the schema-protocol gate and can terminate the operation immediately, before any `project_knowledge_search` is issued.

Before proceeding, confirm you are running on a supported surface. project-context targets AI workspaces with persistent project contexts the operator can attach files to: Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects, and similar hosted AI surfaces.

project-context is **not** designed for Claude Code. Claude Code uses filesystem-based working directories, not hosted project contexts; the `session-recap` skill is the right tool for capturing context from Claude Code sessions.

**If you detect you are running in Claude Code** — signals include: filesystem-mutation tools (e.g., `Bash`, `Write`, `Edit`) are present in your toolbox; the working directory is filesystem-based; no Project-UI affordances are visible to the operator — politely decline and recommend `session-recap`:

> This skill is designed for AI workspaces with persistent project contexts (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects). For capturing context from a Claude Code session, the `session-recap` skill is the right tool. Would you like to invoke `session-recap` instead?

Once the surface guard passes, hand off to the pre-flight protocol in `references/preflight.md`. The post-surface-guard runtime steps (project detection, conflict detection, migration trigger handling, configuration resolution) are described in `references/operations.md` section 4.

### Scenario F (v0.5.0 to v0.6.0 upgrade)

v0.6.0 introduces a new pre-flight scenario for projects already running v0.5.0 (schema "0.3" with `_managed_by` present, but no topology block yet). Pre-flight detects this state and emits the `⚠ Upgrade Available (v0.5.0 to v0.6.0)` verdict, gating the upgrade on the operator's confirmation token `confirm v0.6.0 upgrade`. The upgrade rewrites the three canonical files in place: adds a `topology` block with `role: "unclassified"` default (all relationship fields null, `declared_by: "skill-default"`) and bumps `schema_version: "0.3"` → `schema_version: "0.4"`. All other frontmatter and body content is preserved unchanged. After the upgrade, the skill emits the role-declaration prompt (LOCKED TEXT 1 per `references/preflight.md` section 13.1) to solicit the operator's topology role. The full algorithm lives in `references/migration.md` section 10; the verdict glyph and example block live in `references/preflight.md` section 4.4.

Example pre-flight report block for Scenario F:

```
## Pre-flight Report ⚠ Upgrade Available (v0.5.0 to v0.6.0)

**Project:** [project name]
**Existing system:** project-context.md, entities.md, project-context-archive.md
  (schema 0.3, _managed_by present, generated by v0.5.0, no topology block)
**Executing skill:** v0.6.0
**Proposing:** in-place upgrade to schema 0.4 (adds topology metadata block
  with unclassified defaults, bumps schema_version, no content changes).
  After upgrade, operator will be prompted to declare topology role.

**To proceed:** type `confirm v0.6.0 upgrade`
```

### Scenario G (v0.6.0 to v0.7.0 upgrade)

v0.7.0 introduces a pre-flight scenario for projects already running v0.6.0 (old canonical names at schema "0.4" with `_managed_by` and a topology block, no `pc-NNNN-*` files). Pre-flight detects this state and emits the `⚠ Upgrade Available (v0.6.0 to v0.7.0)` verdict. This is a destructive operation and gates on model setup per `references/preflight.md` section 4.6; the operator's confirmation token is `confirm v0.7.0 upgrade`. The upgrade renames the three files to `pc-0001-{context,entities,archive}.md`, adds `generation: 1`, bumps `schema_version: "0.4"` → `"0.5"`, RETAINS `update_count` and all per-record counters verbatim (the `generation` identity counter is distinct from the `update_count` scoring counter), carries the topology block verbatim, and applies the config treatment (header plus relocation to `config/` on filesystem platforms). Post-flight renders the set-integrity directive and instructs deletion of the old-named files. The full algorithm lives in `references/migration.md` section 11; the verdict and example block live in `references/preflight.md` section 4.4.

### Platform support and Cowork deferral

Per-platform behavior is data, not code: `config/platform-specific-parameters.md` holds the model the operation-start advisory names (`strongest_thinking_model`), whether the active model can be changed from a skill, file-inventory enumerability (which drives counter assignment), config read location, and output bundling. Profiled platforms: `claude-ai`, `codex`, `chatgpt-enterprise` (with `m365-copilot` carrying conservative defaults pending validation). **Claude Code is a declined platform** (the surface guard redirects to the companion skill). **Cowork is deferred:** v0.7.0 does not implement a Cowork profile. The anti-autonomous-decision guardrail must continue to fire on Cowork (it did in testing); the Cowork profile is a v0.7.x or v0.8.0 follow-on once the operator-enumerated behavior modifications are in hand. Do not implement autonomous Cowork behavior in v0.7.0.

### Stale Spoke verdict (informational)

On `role: spoke-*` projects, pre-flight performs stale-spoke detection (per `references/preflight.md` section 11): it reads `topology.hub_version` from `pc-NNNN-context.md` frontmatter and compares it against the version parsed from an attached `ai-engineering-hub-instructions-v*.md` file. When the file version is newer than the spoke's declared version, pre-flight emits the `⚠ Stale Spoke` informational verdict. The verdict is not blocking; the proposed operation proceeds normally. Post-flight surfaces a one-line note recommending project-creator upgrade mode. Two adjacent informational verdicts handle related edge cases: `⚠ Hub Source Behind` (file version is older than the spoke's declared version, rare) and `⚠ Hub Source Missing` (no Hub instructions file is attached). All three are informational; none block operation.

The skill never auto-upgrades the Hub reference. The upgrade flow lives in the project-creator skill (Workstream 3); v0.6.0 surfaces the staleness signal but does not act on it.

## Output behavior

Operations write the three markdown files of the current generation (`pc-NNNN-{context,entities,archive}.md`) to the session's output location and present them via the available file-presentation mechanism so the operator can download and upload them to the Project, then prune lower-numbered sets per the post-flight set-integrity directive. The skill does not have a programmatic path to add files to a Claude Project in v0.7.0 (awaiting platform API capability; tracked in `ROADMAP.md`).

The skill does not commit, push, or transmit output anywhere. Distribution is the operator's responsibility.

## Failure modes the router handles

- **Claude Code surface detected.** Decline; recommend `session-recap`.
- **Not in a Project container.** Warn and ask before proceeding.
- **Multiple ambiguous trigger phrases in one invocation.** Route to the most specific operation; if still ambiguous, ask the operator.
- **Legacy files detected.** Route through migration (operations preserve this in their pre-flight).
- **`user-config.md` malformed.** Warn; fall back to org-config / upstream defaults.

All other failure modes (schema violations, classifier ambiguity, oversized output, validation errors) are handled by the operation files.
