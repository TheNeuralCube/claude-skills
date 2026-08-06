<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to `session-orchestrator` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on dotted semver declared in the SKILL.md frontmatter; it earns `1.0.0` after real use and an eval pass.

## [0.1.1] - 2026-08-06

Housekeeping release. No behavior change: the layers, the mode dispatch, the nine rules, and the gates are unchanged.

### Added

- **`version: 0.1.0` in the SKILL.md frontmatter**, then bumped to `0.1.1` for this release. The version had previously existed only in the H1 heading and the version-history table, so no machine reading the frontmatter could determine it.
- **README.md, CHANGELOG.md, ROADMAP.md, and USAGE.md**, completing the repository's required per-skill document set.
- **A portability notice** in README.md and ROADMAP.md stating plainly that this skill is Hub-resident, references owners not published in this repository, and is slated to move to a private Hub-skills repository.

### Changed

- **Removed two dead cross-references.** The "does not own" section routed session capture to `nc3-session-recap-skill` and skill naming to `nc3-meta-conventions-skill`. The first does not ship publicly; the second is retired and owns nothing. They now point to `session-handoff` and this repository's `CLAUDE.md` respectively. The `handoff-settings-block` reference is deliberately retained — see the portability notice.

## [0.1.0] - 2026-08-03

### Added

- **Initial release.** Distilled from the four-day quarterback run of 2026-07-31 to 2026-08-03: five waves, sixteen issues closed or filed, zero rollbacks.
- **The three-layer session model** (quarterback, orchestrator, builder) plus the optional independent auditor, with the operator as the sole merge authority.
- **`references/rules.md`:** the nine verification rules, each anchored to the real failure that produced it.
- **Two modes** (`modes/quarterback.md`, `modes/orchestrator.md`) dispatched from a thin router.
- **`references/wave-selection.md`:** the concurrency-collision procedure, its blind spot, and what a false collision costs.
- **`references/artifacts.md`:** the package and report-back templates.

### Operator decisions at authoring time

- **One skill, two modes** over two skills sharing a rules reference, chosen specifically so the rules cannot drift apart.
- **Method stated generally, incidents cited.** Every rule is repo-agnostic and anchored by the failure that produced it; no project appendix.
- **Handoff format delegated** to `handoff-settings-block`, which wins any format disagreement.
- **Hub-resident, unprefixed.** First packaged as `nc3-session-orchestrator-v0-1` for account install, then corrected the same day. The account form was wrong on evidence: `handoff-settings-block` is Hub-resident only, so an account-installed copy pointed at a format owner that does not exist outside a Hub session, which is the skill's own rule 3.
