# Contributing to claude-skills

Thank you for your interest in contributing. This is an open-source project under the Apache License 2.0, and contributions of all sizes are welcome.

> **Agents:** [`CLAUDE.md`](./CLAUDE.md) is the authoritative contract for layout, naming, versioning, and releases. Non-Claude agents start at [`AGENTS.md`](./AGENTS.md). This file is the human-facing summary; where the two differ, `CLAUDE.md` wins.

## Ways to contribute

- Reporting bugs or unexpected behavior in existing skills
- Suggesting improvements to existing skills
- Submitting new skills that fit the Neural Cube design philosophy
- Improving documentation
- Helping triage issues

## Before you start

If you are planning a substantial change such as a new skill or a major rework of an existing one, please open an issue first to discuss the approach. This avoids the situation where someone invests significant effort in a direction that does not align with the project.

For small changes (typo fixes, clarifications, minor bug fixes), feel free to open a pull request directly.

## Skill structure

Every skill lives in `skills/<skill-name>/` and carries all five required files:

```
skills/<skill-name>/
  SKILL.md           Required. Frontmatter and trigger logic.
  README.md          Required. What it is and how it is structured.
  CHANGELOG.md       Required. Version history, Keep a Changelog format.
  ROADMAP.md         Required. Deferred items, conditions for 1.0.0, known limitations.
  USAGE.md           Required. A walkthrough of actually using it.
  [modes/ references/ config/ scripts/ assets/]   Optional supporting files.
```

There is no grandfathering: all five are required on every skill.

Do not add a per-skill `LICENSE` file. The root `LICENSE` and `NOTICE` cover the whole repository.

### A skill directory never lives at the repository root

`skills/` is the only place a `SKILL.md` may appear. CI fails any pull request that puts one elsewhere.

## Naming and versioning

Skill directories are lowercase kebab-case, two or three words, with **no prefix and no version**: `deep-analysis`, not `nc3-data-core-sample-skill-v0-2`. The directory name, the YAML `name`, and the `SKILL.md` H1 must match exactly.

**Versions are dotted semver declared once, in the `SKILL.md` frontmatter `version` field.** They do not appear in directory names, headings, or filenames.

- **MAJOR** for breaking changes to triggers, output schema, or expected behavior
- **MINOR** for additive improvements that preserve existing behavior
- **PATCH** for fixes and housekeeping with no behavior change

If you change a skill's payload, bump its version and add a `CHANGELOG.md` entry in the same pull request.

## Frontmatter

```yaml
---
name: my-skill        # must equal the directory name
version: 0.1.0        # dotted semver, three parts
description: >-       # folded block scalar, 1024 characters maximum
  What the skill does and when to trigger it.
---
```

Always use the folded block scalar (`>-`) for `description`. Descriptions are full of colons, and a plain YAML scalar containing `": "` is invalid.

## Skills must be self-contained

This repository is public, and an installed skill cannot read it. So a skill may not:

- tell its reader to consult a file in this repository;
- route the reader to a skill that is not published publicly;
- reference private governance, internal org names, or private repositories.

State the convention inline instead. If a skill genuinely needs a private dependency, it belongs in a private repository rather than this one.

## Validate before you open a pull request

```bash
python scripts/validate-repo.py
```

This is the same check CI runs. It verifies layout, naming, frontmatter, required files, and the README index.

## The user-config.md cross-skill convention

Beginning with project-context v0.4.0, skills in this repository may publish a `user-config.md` file as a per-user override layer alongside the existing `org-config.md` per-organization layer. The file is a Linux-conf-style markdown document: a YAML body with every setting commented out by default, plus prose comments explaining what each does and the recommended values. The resolution order is `user-config.md` > `org-config.md` > skill defaults.

The canonical example lives at [`skills/project-context/config/user-config.md.template`](skills/project-context/config/user-config.md.template); new skills adopting the pattern should mirror its structure.

## Pull request process

1. Fork the repository
2. Create a branch named for the change (`feat/<slug>`, `fix/<slug>`, or `chore/<slug>`)
3. Make your changes
4. Update the affected skill's `CHANGELOG.md` and bump its version if the payload changed
5. Update the README skill index if you changed a version
6. Run `python scripts/validate-repo.py`
7. Open a pull request describing what changed and why
8. Address any review feedback

Pull requests are squash-merged. Keep changes scoped: one skill or one logical change per pull request. Multi-skill changes are harder to review and roll back if something goes wrong.

## License terms

By submitting a contribution, you agree that your contribution is licensed under the Apache License 2.0, the same license that covers the rest of the project. This is sometimes called "inbound equals outbound" licensing and is the standard practice for Apache 2.0 projects.

## Questions

For questions about contributing, open a GitHub issue with the `question` label.
