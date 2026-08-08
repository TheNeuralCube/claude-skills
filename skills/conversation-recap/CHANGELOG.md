<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to `conversation-recap` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on dotted semver declared in the SKILL.md frontmatter; it earns `1.0.0` after real use and an eval pass.

## [0.1.1] - 2026-08-08

Housekeeping release. No behavior change: the pipeline, the register catalog, the tier bands, and every doctrine are byte-identical in effect.

### Fixed

- **Invalid YAML frontmatter.** The `description` was an unquoted plain scalar containing `": "`, which a strict YAML parser rejects. Converted to a folded block scalar (`>-`), matching `session-handoff`. The skill loaded before only because the platform loader is lenient.

### Changed

- **Moved from the repository root** to `skills/conversation-recap/`, where every other skill lives. Publishing a skill to the repo root was a packaging error, not a layout choice.
- **Removed references to skills that ship nowhere public.** Routing lines naming `nc3-session-recap-skill` and `per-jrn-journal-entry` sent a reader after skills they cannot obtain; they now describe the capability and defer to whatever the operator has installed. The filename convention formerly deferred to `nc3-meta-conventions-skill-v0-2` is now stated inline, because an installed skill cannot read a repo file either.

### Added

- **README.md, CHANGELOG.md, ROADMAP.md, and USAGE.md**, completing the repository's required per-skill document set.

## [0.1.0] - 2026-07-17

### Added

- **Initial build** per the 2026-07-17 design spec (`docs/conversation-recap/2026-07-17_design-spec.md`).
- **Seven-step pipeline:** TRIGGER, SOURCE, INTERVIEW, TIER CALL, GENERATE, DEBRIEF, OPTIONAL SAVE, with a collapse rule that skips interview steps for parameters given at invocation.
- **24-register catalog** (`references/register-catalog.md`) across the literary, comedy, and cinematic families, each defined across six fields and governed by the register-integrity law.
- **Three tiers** (Teaser, Cold Open, Season Recap) as reading-time and word-budget contracts, with the judgment-call doctrine and the thin-source rule.
- **Three-part output contract:** title card, register-native body, and the mandatory `WHERE WE LEFT OFF` block.
- **Honesty constraints:** the fabrication rule, the interiority clause, and the emotionally-heavy-thread bias.
- **Calibration anchor:** the 2026-07-17 Seinfeld-register run "The Command" (656 words) is the ratified gold standard for Medium feel.
