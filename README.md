<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Claude Skills from Neural Cube
Open-source Agent Skills for Anthropic Claude, published by Neural Cube under Apache 2.0.
## Why this repo exists
Each skill in this monorepo solves a real problem in working with Claude across long-running projects. Skills are designed to produce outputs that travel cleanly across AI surfaces (claude.ai Projects, ChatGPT Projects, Copilot M365 Projects) so the same context grounds future sessions wherever the operator works next.
## Skills
| Skill | Version | Description |
|---|---|---|
| [project-context](./project-context) | 0.3.0 | Captures forward-grounding context from a conversation inside an AI project (decisions, constraints, entities, terminology, open items, state) into a structured markdown file the operator adds back to the project. Future chats start grounded without re-explanation. Two modes: generate (default) and consolidate. |
| [nc3-data-core-sample-skill-v0-2](./skills/nc3-data-core-sample-skill-v0-2) | v0-2 | Frontier-class deep-analysis skill: one maximum-extraction pass over an artifact (codebase, repo, document set, website, architecture, product), emitting dense machine-readable deliverables for execution-class consumers. Six lenses (survey, craft, review, security, plan, audit); default survey + review. Every recommendation survives a war-game pass. |
## License
Apache 2.0. See [LICENSE](./LICENSE) and [NOTICE](./NOTICE).
## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md). Every skill folder must include SKILL.md, README.md, and CHANGELOG.md.
## Project status
Active. New skills land via reviewed pull requests.
