<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to `session-orchestrator` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on dotted semver declared in the SKILL.md frontmatter; it earns `1.0.0` after real use and an eval pass.

## [0.2.0] - 2026-08-08

Reunites two lineages that had forked, and folds in the repository standardization.

### Added

- **Rule 10 — a gate encodes a branch model and a tool's real predicate, not a name and not your reading.** Codified from three incidents: a gate drafted under a retired branch model that routed records onto curated trunk; a remediation gate unsatisfiable on its own branch; and a `git branch -d` gate that encoded *merged-into-HEAD* while git tests *merged-into-UPSTREAM*, where a fail-closed refusal had been pre-drafted as proof of stranded work. That last one is the expensive misreading, because it argues for exactly the destructive override the refusal exists to prevent.
- **Rule 10b — the allowlisted invocation is part of the gate surface.** A permission allowlist naming `Bash(cmd /c …)` opened a shell and pushed nothing, while the same script from PowerShell pushed correctly. An agent *obeying the permission rule* selects the broken path, so the allowlist makes the wrong choice the compliant one, and it fails quietly.
- **`version` in the SKILL.md frontmatter.** It had existed only in the H1 heading and the version-history table, so nothing reading the frontmatter could determine it.
- **README.md, CHANGELOG.md, ROADMAP.md, and USAGE.md**, completing the repository's required per-skill document set.
- **A portability notice** in README.md, USAGE.md, and ROADMAP.md stating plainly that this skill is Hub-resident, references owners not published in this repository, and is slated to move to a private Hub-skills repository.

### Changed

- **Rules count 9 to 10**, with the `references/rules.md` intro line and quick-reference table updated rather than left to drift.
- **Removed two dead cross-references.** The "does not own" section routed session capture to `nc3-session-recap-skill` and skill naming to `nc3-meta-conventions-skill`. The first does not ship publicly; the second is retired and owns nothing. They now point to `session-handoff` and this repository's `CLAUDE.md`. The `handoff-settings-block` reference is deliberately retained — see the portability notice.
- **Version removed from the SKILL.md H1 heading**, per the repository's naming standard.

### Why 0.2.0 and not 0.1.1

**A `0.1.1` of this skill exists, and it is not this one.** On 2026-08-06 the operator's Hub tree added rule 10 in place and labelled it `v0.1.1`, on the recorded reasoning that the skill had no upstream to push to. That reasoning was wrong: this repository is its upstream, and released `session-orchestrator-v0.1.0` on 2026-08-04 byte-identical to the deployed copy. The check that concluded "no upstream" had asked only about a different, private repository.

So `0.1.1` was spent on different content in a tree this repository does not publish from. Reusing it here would put two different payloads behind one version number. `0.2.0` is correct on its own merits regardless — rule 10 is an additive capability, which is a MINOR bump.

This release brings the two trees back into agreement. `project-context` and `session-handoff` were compared at the same time across both trees and were already content-identical; this skill was the only fork.

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
