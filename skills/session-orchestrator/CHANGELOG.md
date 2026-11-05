<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to `session-orchestrator` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on dotted semver declared in the SKILL.md frontmatter; it earns `1.0.0` after real use and an eval pass.

## [0.2.1] - 2026-11-04

### Changed

- Remove fixed workspace paths and unpublished format dependencies; state minimum handoff fields inline.
- Source update only; a release asset has not been published for this version.

## [0.2.0] - 2026-08-08

Adds rule 10 and 10b and folds in the repository standardization.

### Added

- **Rule 10 — a gate encodes a branch model and a tool's real predicate, not a name and not your reading.** Codified from three incidents: a gate drafted under a retired branch model that routed records onto curated trunk; a remediation gate unsatisfiable on its own branch; and a `git branch -d` gate that encoded *merged-into-HEAD* while git tests *merged-into-UPSTREAM*, where a fail-closed refusal had been pre-drafted as proof of stranded work. That last one is the expensive misreading, because it argues for exactly the destructive override the refusal exists to prevent.
- **Rule 10b — the allowlisted invocation is part of the gate surface.** A permission allowlist naming `Bash(cmd /c …)` opened a shell and pushed nothing, while the same script from PowerShell pushed correctly. An agent *obeying the permission rule* selects the broken path, so the allowlist makes the wrong choice the compliant one, and it fails quietly.
- **`version` in the SKILL.md frontmatter.** It had existed only in the H1 heading and the version-history table, so nothing reading the frontmatter could determine it.
- **README.md, CHANGELOG.md, ROADMAP.md, and USAGE.md**, completing the repository's required per-skill document set.
- **A portability notice** describing configuration prerequisites; replaced with self-contained guidance in 0.2.1.

### Changed

- **Rules count 9 to 10**, with the `references/rules.md` intro line and quick-reference table updated rather than left to drift.
- **Removed dead cross-references** to unavailable session-capture and naming instructions.
- **Version removed from the SKILL.md H1 heading**, per the repository's naming standard.

### Version note

Version 0.2.0 adds a verification rule, warranting a minor bump. Deployment-specific history is omitted from this public changelog.

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
- **Handoff conventions** separated from issue-specific scope and acceptance criteria.
- **Unprefixed skill name** used for distribution.
