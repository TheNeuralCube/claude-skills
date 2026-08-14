<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Claude Skills from Neural Cube

Open-source Agent Skills for Anthropic Claude, published by Neural Cube under Apache 2.0.

## Why this repo exists

Each skill in this monorepo solves a real problem in working with Claude across long-running projects. Skills are designed to produce outputs that travel cleanly across AI surfaces (claude.ai Projects, ChatGPT Projects, Copilot M365 Projects) so the same context grounds future sessions wherever the operator works next.

## Skills

| Skill | Version | Download | What it does |
|---|---|---|---|
| [project-context](./skills/project-context) | 0.7.1 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/project-context-v0.7.1/project-context.skill) | Captures forward-grounding context from a conversation into a three-file project memory (active, entities, archive) that future chats read to start grounded. Versioned file identity, decoupled data schema, and a mandatory pre-flight check before any write. |
| [session-handoff](./skills/session-handoff) | 0.1.1 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/session-handoff-v0.1.1/session-handoff.skill) | Captures a high-fidelity, machine-readable handoff of a working session that any agent on any platform can resume cold. Five modes (generate, update, consolidate, retrofit, share-sanitize) behind one auto-routed entry point. |
| [deep-analysis](./skills/deep-analysis) | 0.2.0 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/deep-analysis-v0.2.0/deep-analysis.skill) | Frontier-class deep-analysis: one maximum-extraction pass over an artifact (codebase, repo, document set, website, architecture, product), emitting dense machine-readable deliverables for execution-class consumers. Six lenses; default survey + review. Every recommendation survives a war-game pass. |
| [conversation-recap](./skills/conversation-recap) | 0.1.1 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/conversation-recap-v0.1.1/conversation-recap.skill) | Narrative "Previously On" recaps that re-immerse you in a stale thread rather than re-briefing you on it. 24 registers, three length tiers, and a fabrication rule that keeps the shaping honest. |
| [session-orchestrator](./skills/session-orchestrator) | 0.2.0 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/session-orchestrator-v0.2.0/session-orchestrator.skill) | A three-layer session model for multi-issue software work, where the session that decides is never the session that writes the code. Carries ten verification rules, each paid for by a real failure. **Hub-resident: see its README before installing.** |
| [repo-sanitize](./skills/repo-sanitize) | 0.1.0 | [`.skill`](https://github.com/TheNeuralCube/claude-skills/releases/download/repo-sanitize-v0.1.0/repo-sanitize.skill) | Turns a cloned repository into a frozen archive that cannot connect, carries no secrets or identities in its history, and stays intelligible. Six phases, twelve documented pitfalls, and six offline stdlib scripts. |

Each release also ships an identical `.zip` (some surfaces prefer it) and a `MANIFEST.sha256`.

> **Note on download links.** GitHub's `releases/latest` is repository-wide, and this repository tags per skill, so there is no per-skill "latest" URL. The links above are pinned to each skill's current release tag and are updated as part of every release.

## Installing a skill

Download the `.skill` file for the skill you want and add it to your Claude surface. The `.skill` file is a plain zip whose single top-level folder matches the skill's name, so if a surface wants a folder or a `.zip` instead, rename or unpack it.

## Versioning

Every skill is versioned independently on dotted semver, declared in the `version` field of its `SKILL.md` frontmatter. Directory names never carry a version. Tags are `<skill-name>-v<MAJOR>.<MINOR>.<PATCH>`.

Skills stay on `0.x` until proven in real use; each skill's `ROADMAP.md` states its own conditions for `1.0.0`.

## Repository layout

```
skills/<skill-name>/    one directory per skill; the only place a SKILL.md lives
docs/<skill-name>/      development documents, per skill
scripts/                build and validation tooling
```

Contributors and agents: see [CLAUDE.md](./CLAUDE.md) for the full layout, naming, versioning, and release contract, and [AGENTS.md](./AGENTS.md) if you are a non-Claude agent.

## License

Apache 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Every skill folder must include `SKILL.md`, `README.md`, `CHANGELOG.md`, `ROADMAP.md`, and `USAGE.md`.

## Project status

Active. New skills land via reviewed pull requests.
