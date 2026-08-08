<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# AGENTS.md — entry point for non-Claude agents

**Read [`CLAUDE.md`](./CLAUDE.md). It governs this repository for every agent, including you.**

That file is the single source of truth for layout, naming, versioning, required files, the frontmatter contract, the release procedure, and the tooling. This file does not restate it. Where the two appear to disagree, `CLAUDE.md` wins; report the discrepancy rather than resolving it yourself.

Everything below is what is **specific to non-Claude agents** and therefore has no home in `CLAUDE.md`.

## The three rules most often broken here

Read `CLAUDE.md` in full, but these are the ones that get violated by agents unfamiliar with the tree:

1. **A skill directory goes in `skills/`, never at the repository root.** This has already happened once. CI fails the pull request.
2. **The version lives only in the SKILL.md frontmatter** — not in a directory name, not in the H1, not in a filename.
3. **`description` is always a folded block scalar (`>-`).** A plain scalar containing `": "` is invalid YAML.

Run `python scripts/validate-repo.py` before you hand anything back. It is the same check CI runs.

## Codex

### Git is permitted here

**Codex may run git in this repository** (operator decision, 2026-08-06). This is a deliberate exception to the operator's standing no-git posture for their private working tree, and it applies to this repository only. Do not generalize it to any other tree.

Follow the working conventions in `CLAUDE.md`: branch before writing, never commit directly to `main`, squash-merge, and commit or push only when asked.

### You do not authorize merges

The operator merges. A session that built or audited a change never authorizes that change's merge, and never turns a recommendation into an execution without being told to. Write the recommendation with its evidence and stop.

### Second-model independence

When you audit, **you must not be the model that built the artifact.** That independence is the entire value of the role; an audit by the builder is a self-review wearing a different hat.

### Audit output format

Findings only. Never apply fixes during an audit pass.

- Every finding carries a **severity**.
- The report closes with exactly one verdict: **MERGE**, **MERGE WITH FIXES**, or **DO NOT MERGE**.
- Anything you could not verify is stated as unverified, in those words. Never report a verification you did not perform, and where you verified something weaker than what was asked, say which.

### Context budget

Codex auto-loads roughly 32 KiB. `CLAUDE.md` fits well inside that and is meant to be read whole. Larger material — a skill's `references/`, the development documents under `docs/` — is read on demand as a working step, not auto-injected. Do not assume anything beyond this file and `CLAUDE.md` is already in your context.

## All agents: operator environment

- **Operator shell is PowerShell** on a Windows host. Write every command you surface to the operator in PowerShell, regardless of the shell you are running in. The two are frequently different, which is why this is stated rather than inferred.
- **The `grep -P '\x{2014}'` dash check does not work on this host.** Use `python skills/deep-analysis/scripts/deep_analysis_checks.py check <files>`.

## What this repository is not

Public, Apache 2.0, published to strangers. Do not add private governance paths, internal org names, customer data, or references to private repositories. Do not make a skill depend on a file that ships only in this repository — an installed skill cannot read it.

If a task would require any of the above, stop and tell the operator. It is a signal that the work belongs somewhere else.
