<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Changelog

All notable changes to `repo-sanitize` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The skill is versioned on dotted semver declared in the SKILL.md frontmatter; it earns `1.0.0` after the conditions in `ROADMAP.md` are met.

## [0.1.0] - 2026-08-14

### Added

- **Initial release**, extracted from the first full sanitization run against a real enterprise AI harness frozen for research.
- **Six-phase protocol** in `SKILL.md`: disconnect, inventory, leaked-credential triage, working-tree scrub, history rewrite, verify and freeze. Phase 1 runs first because it is the part that stops harm.
- **Six non-negotiable rules**, each stated twice (operator-facing and agent-facing) because these are the ones that get skipped: never run the target's build or tests; a tree scrub is cosmetic until history is rewritten; verify by extracting the archive; never invent a replacement for an unclassified value; the private decoder stays outside the archive; real leaked credentials are reported, never silently dropped.
- **Leaked-credential policy** distinguishing a real leak from a deliberate secret-detection fixture by asking what breaks if the value changes. Published vendor examples such as `AKIAIOSFODNN7EXAMPLE` are preserved.
- **`references/pitfalls.md`** — 12 failure modes, every one observed on the first real run, each of which produced output that looked correct: substring collisions in ordinary words, vendored third-party data, binary blobs embedding absolute build paths, refs that content filters cannot see, filenames and directories, compounding re-runs, post-rewrite identity reintroduction, fixture destruction, `git log -S` false positives, packaging that drops empty directories, Windows `MAX_PATH`, and the stale working tree after `fast-import`.
- **`references/placeholder-conventions.md`** — placeholders as stable variables rather than redaction, the `.invalid` and `<UPPER_SNAKE>` forms, the one-human-one-pseudonym rule, most-specific-first ordering, the public-constants exemption, and the two-legend requirement.
- **`assets/example.map`** — annotated template map covering every directive.
- **Six stdlib-only, fully offline scripts**: `inventory.py` (read-only discovery including binary blobs and refs), `sanitize_map.py` (one shared map parser so the tree pass and the history pass cannot drift), `scrub_tree.py` (sources from pristine `HEAD`, restores excluded paths, dry-run by default), `scrub_history.py` (single streaming `fast-export` filter with an unmapped-identity report), `verify.py` (scans every object, with an over-scrub check), and `freeze.py` (generic archive root, preserved empty directories).

### Notes

This is a `0.1.0` initial release in this repository, not a re-release. The skill was previously packaged under a retired private naming convention; the payload it ships here is the same protocol with repository-conformant metadata, no dependency on any non-public skill, and neutralized examples.
