<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# CLAUDE.md — governance for this repository

**This file is the authority for how this repository is structured, maintained, and released.** It is self-contained by design: it does not defer to any private tree, and it must never grow a dependency on one. Non-Claude agents read `AGENTS.md`, which defers here.

Read this file before your first write. If an instruction you were given conflicts with this file, say so and stop rather than guessing.

## What this repository is

`TheNeuralCube/claude-skills` — the Neural Cube **public** Agent Skills monorepo, Apache 2.0, remote `https://github.com/TheNeuralCube/claude-skills.git`.

Every skill here is published to strangers. Two consequences bind everything below:

1. **A skill must be self-contained.** An installed skill has no access to this repository, so it may not tell its reader to consult a repo file, and it may not route to a skill that ships nowhere public. State the convention inline instead.
2. **No private material, ever.** No internal governance paths, no org-internal names, no customer data, no private repository references. If a skill genuinely needs a private dependency, it does not belong in this repository.

## The layout contract

```
claude-skills/
  README.md CLAUDE.md AGENTS.md CONTRIBUTING.md LICENSE NOTICE
  .gitignore .gitattributes
  skills/<skill-name>/         one directory per skill; the ONLY place a SKILL.md may live
  docs/<skill-name>/           development documents, per skill
  scripts/                     build and validation tooling
  .github/workflows/           CI
  _build_inputs/               gitignored scratch (only README.md is tracked)
  dist/                        gitignored build output
```

**Anything else at the repository root is a defect.** Nothing else is permitted there without an edit to this file.

### 🚫 Never publish a skill to the repository root

A skill directory goes in `skills/`. Always. There is no exception, no "temporarily", and no "it is only one file".

This is written as a prohibition because it already happened: `conversation-recap` was published to the root and sat there across releases. `validate-repo.py` fails the build on any `SKILL.md` outside `skills/*/`, and CI fails the pull request. Do not work around the check — fix the layout.

Equally prohibited at the root: built `.skill` or `.zip` archives, `MANIFEST.sha256`, and release-notes files. Those are build outputs. They belong in `dist/` (gitignored) and on the GitHub Release.

## Naming

| Thing | Rule | Example |
|---|---|---|
| Skill directory | lowercase kebab-case, two or three words, **no prefix**, **no version** | `deep-analysis` |
| YAML `name` | byte-identical to the directory name | `deep-analysis` |
| SKILL.md H1 | byte-identical to the directory name, **no version suffix** | `# deep-analysis` |
| Git tag | `<skill-name>-v<MAJOR>.<MINOR>.<PATCH>` | `deep-analysis-v0.2.0` |
| Release title | `<skill-name> v<MAJOR>.<MINOR>.<PATCH>` | `deep-analysis v0.2.0` |
| Release asset | `<skill-name>.skill` — **stable, unversioned** | `deep-analysis.skill` |
| Dev document | `docs/<skill-name>/YYYY-MM-DD_<doctype>.md` | `docs/deep-analysis/2026-07-24_build-spec.md` |

Directory, `name`, and H1 move together or not at all. A rename is a `git mv` so history follows.

**Retired conventions.** The `nc3-` prefix, the `v{MAJOR}-{MINOR}` directory suffix, and dash-style versions (`v0-2`) are all retired. So is the `nc3-meta-conventions-skill` that once owned them; it governs nothing and must not be cited. Historical CHANGELOG entries describing past names stay as written, because a changelog records what happened.

## Versioning

**Dotted semver, three parts, declared once — in the SKILL.md frontmatter `version` field.**

The version appears nowhere else: not in the directory name, not in the H1, not in a filename. A skill's in-file version-history table and its CHANGELOG may of course cite versions; those are records, not declarations.

| Bump | When |
|---|---|
| MAJOR | breaking change to triggers, output schema, or expected behavior |
| MINOR | additive capability that preserves existing behavior |
| PATCH | fixes and housekeeping with no behavior change |

**If you change a skill's payload, you bump its version.** A payload edit shipped under an existing version makes the release asset disagree with its own tag. Touching only repository-level files (this file, `README.md`, CI, `docs/`) is not a payload change and bumps nothing.

Skills stay on `0.x` until proven; each skill's `ROADMAP.md` states its own conditions for `1.0.0`.

## Required files per skill

Every skill directory carries all five. There is no grandfathering.

| File | Holds |
|---|---|
| `SKILL.md` | frontmatter, trigger logic, the skill itself |
| `README.md` | what it is, what it does, how it is structured |
| `CHANGELOG.md` | Keep a Changelog format, newest first |
| `ROADMAP.md` | deferred items, conditions for `1.0.0`, known limitations |
| `USAGE.md` | a walkthrough of actually using it |

Optional, by convention: `modes/`, `references/`, `config/`, `scripts/`, `assets/`.

Do **not** add a per-skill `LICENSE`. The root `LICENSE` and `NOTICE` cover the whole repository.

## SKILL.md frontmatter contract

```yaml
---
name: deep-analysis          # required; == directory name
version: 0.2.0               # required; dotted semver, three parts
description: >-              # required; <= 1024 characters
  A folded block scalar. Use this form always.
---
```

**Always write `description` as a folded block scalar (`>-`).** A plain scalar containing `": "` is invalid YAML, and descriptions are full of colons. Two skills in this repository shipped invalid frontmatter for months because the platform loader is lenient; leniency is not a spec. `validate-repo.py` parses strictly, so the loader's tolerance is no longer the gate.

Additional fields are permitted where a skill needs them (`owner`, `sensitivity`, `lifecycle`, `effort-class`, `tags`). Keep them purposeful.

## Release procedure

Releases are **per skill**. One skill, one tag, one release. Never batch skills into a shared tag.

```bash
python scripts/validate-repo.py
```

1. **Validate.** Fix everything it reports. It is the same check CI runs.
2. **Bump** the `version` in the skill's SKILL.md, add its `CHANGELOG.md` entry, and update its in-file version-history table if it has one.
3. **Update the README skill index** — version column and download link both. This is not optional; a stale index is the defect this repository has shipped most often.
4. **Branch, PR, squash-merge.** `feat/<slug>`, `fix/<slug>`, `chore/<slug>` cut from `main`. Merge with `gh pr merge --squash --delete-branch`.
5. **Build from merged `main`:**
   ```bash
   pwsh -File scripts/build-skill.ps1 -Skill deep-analysis
   ```
   This emits `dist/<skill-name>.skill`, `dist/<skill-name>.zip`, and `dist/MANIFEST.sha256`. The `.skill` is a plain zip whose single top-level folder matches the skill's YAML `name`.
6. **Tag and release:**
   ```bash
   git tag deep-analysis-v0.2.0 && git push origin deep-analysis-v0.2.0
   gh release create deep-analysis-v0.2.0 --title "deep-analysis v0.2.0" --notes-file <notes> dist/deep-analysis.skill dist/deep-analysis.zip dist/MANIFEST.sha256
   ```

### Release-note links must be pinned to the release's own tag

Never link to `blob/main` from a release note or a README download column. Use `blob/<tag>` or `releases/download/<tag>/`. A later rename breaks every `main`-pinned link, which is exactly how the `nc3-data-core-sample-skill-v0-1` release notes broke.

### Why there is no per-skill "latest" URL

GitHub's `releases/latest` is **repository-wide**, and this repository tags per skill. There is therefore no working `releases/latest/download/<skill>.skill` URL, and inventing one produces a link that silently serves the wrong skill.

The README download table carries tag-pinned URLs instead, and step 3 above keeps them current. That manual step is the price of per-skill tagging; do not "fix" it with a latest-URL.

## Tooling

| Command | Does |
|---|---|
| `python scripts/validate-repo.py` | full conformance check; exits non-zero on any failure |
| `pwsh -File scripts/build-skill.ps1 -Skill <name>` | packages one skill into `dist/` |
| `pwsh -File scripts/build-skill.ps1 -All` | packages every skill |

`validate-repo.py` enforces: no `SKILL.md` outside `skills/*/`; directory name equals YAML `name` equals H1; `version` present and three-part semver; no version string in any directory name; strictly-parseable frontmatter; `description` present and at most 1024 characters; all five required files present; no per-skill `LICENSE`; no build artifacts at the root; and a README index row per skill with a matching version.

**Portability note.** The em-dash check written as `grep -P '\x{2014}'` fails on the operator's Windows host. Use `python skills/deep-analysis/scripts/deep_analysis_checks.py check <files>`, which is portable, and treat the grep as a fallback only.

## Working conventions

- **Operator shell is PowerShell.** Write every command you hand the operator in PowerShell, whatever shell you are holding.
- **Branch before writing.** Never commit directly to `main`.
- **Squash-merge**, delete the branch.
- **Commit or push only when asked.** Do not open a pull request, push a tag, or publish a release on your own initiative.
- **One skill or one logical change per pull request.**
- **`_build_inputs/` is gitignored scratch.** Drop reference documents there during a build; clean it out afterward. Only its `README.md` is tracked, so the folder survives a fresh clone.
- **Development documents go in `docs/<skill-name>/`,** never in the skill directory and never at the root.

## Maintenance checklist

Run this when you touch anything in `skills/`:

- [ ] `python scripts/validate-repo.py` passes
- [ ] Version bumped if the payload changed
- [ ] `CHANGELOG.md` entry written
- [ ] README index row current: version **and** download link
- [ ] No reference to a skill that ships nowhere public
- [ ] No private paths, internal names, or private repository references
- [ ] Nothing new at the repository root
