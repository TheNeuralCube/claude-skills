# Contributing to claude-skills

Thank you for your interest in contributing. This is an open-source project under the Apache License 2.0, and contributions of all sizes are welcome.

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

Skills in this repository follow a consistent layout:

```
skill-name-vX-Y/
  SKILL.md           Required. Skill metadata and trigger logic.
  README.md          Required. User-facing documentation for this skill.
  CHANGELOG.md       Required. Version history for this skill.
  [supporting files] Optional. Templates, examples, or helpers.
```

Each skill is independently versioned using the `vMAJOR-MINOR` suffix on the folder name. Versions follow the spirit of semantic versioning: MAJOR for breaking changes to skill triggers, output schema, or expected behavior; MINOR for additive improvements that preserve existing behavior.

## The user-config.md cross-skill convention

Beginning with project-context v0.4.0, skills in this repository may publish a `user-config.md` file as a per-user override layer alongside the existing `org-config.md` per-organization layer. The file is a Linux-conf-style markdown document — a YAML body with every setting commented out by default, plus prose comments explaining what each does and the recommended values. The resolution order is `user-config.md` > `org-config.md` > skill defaults. The canonical example of this convention lives at [`project-context/references/user-config-template.md`](project-context/references/user-config-template.md); new skills adopting the pattern should mirror its structure. A future release of the `nc3-meta-skill-forge` skill (working name) will absorb the convention as its canonical home.

## Pull request process

1. Fork the repository
2. Create a branch named after the change you are making (for example `add-meeting-recap-skill` or `fix-session-recap-trigger-bug`)
3. Make your changes
4. Update the relevant CHANGELOG.md inside the affected skill folder
5. Open a pull request describing what changed and why
6. Address any review feedback

Pull requests should keep changes scoped: one skill or one logical change per PR. Multi-skill changes are harder to review and roll back if something goes wrong.

## License terms

By submitting a contribution, you agree that your contribution is licensed under the Apache License 2.0, the same license that covers the rest of the project. This is sometimes called "inbound equals outbound" licensing and is the standard practice for Apache 2.0 projects.

## Questions

For questions about contributing, open a GitHub issue with the `question` label.
