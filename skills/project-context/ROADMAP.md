<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# project-context — roadmap

This file tracks parking-lot items, planned work, and external platform dependencies for the project-context skill. It is not a commitment to deliver any specific item by any specific date; it is the public record of what is on our radar and why.

Items are grouped by milestone label:

- **v0.5.x** — may surface during the v0.5.0 iteration window. Patch-release work.
- **v0.6.0** — deferred to the next minor release.
- **post-v1** — items that depend on platform features or that we want to settle before declaring API stability.

Each item is intended to map to a GitHub issue once the operator opens issues for tracking (per build-spec section 9).

## Delivered in v0.5.0

The v0.5.0 release closed the protocol-enforcement gap documented in the 2026-05-19 postmortem:

- **Mandatory pre-flight protocol** as a structural gate in `SKILL.md` (`## Protocol` section).
- **`references/preflight.md`** (new file): pre-flight algorithm, report block format, token catalog, post-flight summary.
- **Schema "0.3"** with new REQUIRED `_managed_by: project-context-skill` field for reliable detection.
- **Upgrade migration** (v0.4.0 → v0.5.0): in-place schema upgrade with frontmatter-only changes, content preserved verbatim. Token: `confirm upgrade`.
- **Post-flight summary** symmetric with pre-flight; closes the audit loop.
- **Pre-flight prerequisite gating notes** at the top of every `operations/*.md` file.

## Milestone: v0.5.x

These items may land in patch releases during v0.5.0's iteration window. Patch criteria: schema unchanged, no breaking change to operator-facing behavior.

- **Section-specific half-lives.** Single global `lambda` applies in v0.5.0. Per-section overrides may be useful if usage data shows that Decisions decay at a different rate than Open Items. Track usage; revisit. (Carried from v0.4.x.)
- **Restore command.** Archive records carry a `restore_command: "restore arc-NNN"` field. v0.5.0 documents the field; the actual handler for the `restore` invocation is partially implemented and may need a patch if operators report friction. (Carried from v0.4.x.)
- **Migration robustness.** The migration logic in `references/migration.md` handles the common cases; edge cases (malformed legacy frontmatter, mixed-schema-version legacy files in one project, legacy `consolidation_summary` with non-numeric values, partial-upgrade-then-re-invoke scenarios) may need patching as real migrations and upgrades reveal corner cases. (Carried from v0.4.x; v0.5.0 added the upgrade-migration path which has its own edge-case surface in `references/migration.md` section 9.8.)
- **Auto-mode coaching surface.** The audit trail captures enough information to coach users on auto-mode quality. v0.5.x may add a `references/audit-review.md` document that explains how to spot quality degradation patterns from the audit fields. (Carried from v0.4.x.)
- **Pre-flight habituation mitigation.** Operator may grow habituated to typing `confirm merge` and similar tokens. Possible v0.5.x patches: occasional verdict-line variation, randomized confirmation tokens, or other low-cost friction differentials. Deferred per design spec §16; track usage and revisit.
- **`--no-preflight` escape hatch (AI-09).** Whether to support a no-pre-flight invocation flag for expert operators. Design spec §16 explicitly defers this; inverse argument is "friction is the feature." Revisit if operators report substantial friction.
- **Diff-before-write (AI-10).** Whether the skill should summarize the proposed file diff before writing, in addition to the existing diff-and-approve flow for gated proposals. Design spec §16 explicitly defers; substantial UX redesign.
- **Spec correction.** Design spec §15 (v0.4.0) has a historical inaccuracy about what `schema_version` string v0.1.0-v0.3.2 wrote (claimed `"0.1"`, actual was `v0.1.0`). Operator will revise the design spec in a doc-only follow-up release. Tracked here so it does not get lost. (Carried from v0.4.x.)

## Milestone: v0.6.0

Deferred to the next minor release.

- **Archive infinite growth.** The archive grows monotonically over time. v0.5.0 has no compaction, cold-storage tiering, or hard limit. v0.6.0 will design a cold-storage tier for archive records older than N updates / older than a wall-clock threshold, with a clean separation so the active scoring algorithm does not have to consider records past a certain age. (Carried from v0.4.0 v0.5.0 deferred list.)
- **A-MEM-style link evolution.** Records can link to each other via the `links` field, but links are static (set on creation, not auto-evolved). v0.6.0 will add a link-evolution pass that detects when a record's relationships should change based on new records. (Carried.)
- **Zep-style bi-temporal model.** v0.5.0 tracks `last_seen_update` (event time) and `last_seen_at` (wall-clock) but does not separately track ingest time vs validity time. v0.6.0 will add `valid_from` / `valid_to` fields to records that have time-bounded validity (e.g., "Q3 plan is X" only valid during Q3). (Carried.)
- **MCP server packaging.** v0.5.0 ships only as an Agent Skill `.skill` archive. v0.6.0 will add an MCP server wrapper for environments that prefer MCP over Agent Skills. (Carried.)
- **Entity decay.** v0.5.0 entities never decay (people, places, things stay forever once added). v0.6.0 will add an optional `entity_decay` policy in `user-config.md` for users who want unused entities archived. (Carried.)
- **Cross-project context sharing.** v0.5.0 scopes to a single project. v0.6.0 may add a `related_projects` frontmatter field for users who work on multiple related projects. (Carried.)
- **Team-level analytics.** Aggregate usage analytics across users of the same org (proposal acceptance rate, auto-mode quality trends, scoring-coefficient effectiveness). Deferred until the audit trail accumulates enough data to be useful. (Carried.)
- **Cross-skill formalization of `_managed_by`.** v0.5.0 declares the field for project-context only. Formal cross-skill convention work happens in the future nc3-meta-skill-forge skill (see post-v1 below) but the field shape may be standardized informally across other skills in the v0.6.0 cycle.

## Milestone: post-v1

Items dependent on platform features or that we want to settle before declaring API stability at v1.0.0.

- **Programmatic Project-file management.** The skill cannot add or remove files from a Claude Project in v0.5.0 — no platform API exists. The manual upload-and-replace flow is the dominant friction in the workflow. When Anthropic ships a Projects file-management API (or a first-party MCP server with file-management capability), the operator brief is replaced by automated file management with operator approval.
- **Multi-collaborator audit.** `audit.approved_by` is nullable in v0.5.0 pending platform identity API. When the platform exposes authenticated user identity to skills, the field is populated automatically and team-level audit becomes meaningful.
- **nc3-meta-skill-forge** (working name; current `nc3-meta-conventions-skill` is being rescoped). The proprietary skill-builder skill will codify the cross-skill conventions introduced here — decoupled schema versioning, build-time schema-drift detection, `user-config.md` per-user override layer, and the `_managed_by` registry-marker convention introduced in v0.5.0 — as a standard pattern for all skills in the monorepo. The `user-config.md` convention introduced in v0.4.0 of project-context will be documented in whichever version of the meta-conventions / forge skill is current at v0.5.0 release, with repo-root `CONTRIBUTING.md` pointing to `references/user-config.md.template` as the canonical example until then.
- **Stability commitments.** v1.0.0 will represent the first stability commitment. Schema changes after v1.0.0 are MAJOR-version bumps with explicit migration paths and deprecation notices. Until then, breaking changes are allowed but documented in `references/schema-changelog.md` with migration logic.
- **Less-technical user agent layer.** The skill is for AI-literate professionals; less-technical users are downstream consumers of output. A future agent layer wrapping the skill could expose a friendlier surface to less-technical users without compromising the underlying schema or workflow.

## How items move between milestones

- An item starts in the milestone it's first identified in.
- During an iteration window, operator may promote items into v0.5.x if a patch warrants it.
- Items in v0.6.0 may slip to post-v1 if they prove harder than expected, or accelerate to v0.5.x if a patch can carry them.
- post-v1 items move to v0.6.0 or earlier when their platform dependency is removed.

The roadmap is updated whenever an item's milestone changes, a new tracked item is added, or an item is delivered (with a `### Delivered` link to the version that landed it).

## Cross-references

- Open items the skill writes into project files (in `## Open Items` of `project-context.md`) are project-scope, not skill-scope. They do not belong here.
- Design-spec parking-lot items (design spec §16) seeded this roadmap. As items are completed, this file is updated; the design spec is not.
- The CHANGELOG.md captures what shipped; this file captures what may ship.
