<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to the nc3-data-core-sample-skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on the Neural Cube `v{MAJOR}-{MINOR}` scheme (dash, not dot), owned by the conventions skill; every new skill starts at `v0-1` and earns `v1-0` after real use and an eval pass.

## [v0-1] - 2026-07-07

Genesis release. Built cold from the 2026-07-07 build spec, which encodes the manual deep-dive workflow proved by that day's crescent-harness session.

### Added

- **Thin-router SKILL.md.** Identity, effort-class posture (six rules), lens dispatch table, seven-step protocol spine, non-negotiables, output-filename convention, ecosystem chaining, and a dual help section. Carries no lens execution detail beyond dispatch.
- **Five lens mode files.** survey (as-built design spec + build spec), craft (engineering craft study), review (prioritized findings), security (security review), plan (war-gamed execution plan). Default dispatch is survey + review; `full assay` runs all five; craft is opt-in; plan requires an operator objective or degrades into a review roadmap section.
- **Three single-source references files.** `deliverable-contract.md` (output frontmatter schema plus the operator document conventions and traceability rule), `war-game-protocol.md` (the mandatory five-step adversarial gate), and `evidence-protocol.md` (read discipline per artifact type). Mode files reference these; they never restate them.
- **The effort-class posture.** Declares `frontier-max` for the skill and never a model name. Scarcity rule (read everything, gap the rest), asymmetry rule (frontier reasoning in, execution-class consumability out), optimize-by-design spend with a single scope-anomaly flag, and a one-question intake ceiling.
- **The war-game mandate.** review, security, and plan run the full protocol; survey runs it against its recommendations; craft runs it against its collaboration predictions. Results are written into each deliverable.
- **INFORMATION GAP discipline.** No empty fields anywhere; unresolvable ambiguities become explicit, workable gap markers carrying the exact question a cheaper session or the operator should answer.
- **README, USAGE, ROADMAP.** Repo wrapper files per the contribution structure.

### Notes

- **No em dashes or en dashes** appear anywhere in the skill or its generated output, by design. Verified with a codepoint scan across all files at build time.
- **Effort classes only, never model names** in this skill or in any output it produces.
- **All 12 acceptance checks** from the build spec passed at genesis: naming triad, description length (977 chars, under the 1024 limit), dash purity, dual help, version history, thin router, single-source rule, effort-class purity, war-game mandate, filename convention, one-question ceiling, and scarcity + asymmetry rules.
- **Why v0-1 and not v1-0.** Unproven on real targets. v1-0 is earned after 2 or 3 real runs, operator feedback incorporated, and the eval checklist re-passed.

### Deviations from the build spec

- **H1 heading** is `Core Sample -- nc3-data-core-sample-skill-v0-1` per build spec section 2.3.1's literal, which the conventions skill's own H1 form (`Title -- name`) corroborates; acceptance check 1 (exact-name match) is satisfied by name containment.
- **Dash-check command** in `deliverable-contract.md` uses octal UTF-8 printf escapes rather than the build spec's literal em-dash grep form, which is not valid grep syntax on the build platform. The octal form was verified working and keeps the file dash-pure against its own check.
- **Mode files run 35 to 53 lines** against a 60-to-120 target; all required sections are present, and padding to a line count would violate the fluff-is-a-defect rule. No acceptance check gates length.
