# Acceptance checks

The skill's acceptance checklist, brought in-repo at v0-2. Checks 1 through 12 reconstruct the genesis build spec's 12-check list (previously referenced from CHANGELOG.md but not available inside the repo); check 13 was added with the audit lens. The v1-0 promotion path in ROADMAP.md requires re-passing this full list.

Run checks marked "script" with `python scripts/core_sample_checks.py check <files>`; verify the rest by reading the named files.

| # | Check | Pass criterion | How to verify |
|---|---|---|---|
| 1 | Naming triad | Directory name, YAML `name` field, and SKILL.md H1 all carry the identical skill name and version | Manual: compare the three locations |
| 2 | Description length | YAML `description` is under 1024 characters | Script (`description` check) |
| 3 | Dash purity | No em dash (U+2014) or en dash (U+2013) in any skill file | Script (`dashes` check) across every file in the skill |
| 4 | Dual help | SKILL.md has a Help section with "For the Operator" and "For the Agent" subsections | Manual |
| 5 | Version history | SKILL.md carries a version history table whose top row matches the current version | Manual |
| 6 | Thin router | SKILL.md carries identity, posture, dispatch, spine, and help only; lens execution detail lives in modes/ | Manual: SKILL.md names no per-lens sections or schemas beyond dispatch |
| 7 | Single-source rule | Contracts live once each in references/; mode files reference them and never restate them | Manual: grep modes/ for restated contract rules |
| 8 | Effort-class purity | No vendor model names anywhere in the skill or its examples; effort classes only | Manual: grep for known model names |
| 9 | War-game mandate | Every mode file states its war-game applicability; review, security, plan, and audit mandate the full protocol | Manual: read the war-game section of each mode file |
| 10 | Filename convention | Output pattern is `{YYYY-MM-DD}_{target-slug}_{lens-tag}_core-sample.md` and conforms to the conventions skill | Script (`filename` command generates and validates) |
| 11 | One-question ceiling | Posture rule limits intake to at most one batched clarification | Manual: SKILL.md posture rule 5 |
| 12 | Scarcity and asymmetry rules | Posture states the scarcity rule (read everything, gap the rest) and the asymmetry rule (frontier reasoning in, execution-class consumability out) | Manual: SKILL.md posture rules 2 and 4 |
| 13 | Audit operator-class exception | audit is the sole lens with `consumer: operator-class`; the contract's `lens` enum and `consumer` values agree across SKILL.md, modes/audit.md, and references/deliverable-contract.md; the plain-language rules are confined to the audit lens | Manual: compare the three files |
