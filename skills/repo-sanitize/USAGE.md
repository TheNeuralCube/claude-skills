<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Usage

How to run `repo-sanitize` end to end. See `SKILL.md` for the protocol the agent follows, `references/pitfalls.md` for the failure modes, and `references/placeholder-conventions.md` for how to name things.

## Before you start

- **Work on a copy.** The process rewrites history irreversibly. Take a backup first, and delete it at the end — it holds exactly what you removed.
- **Never run the target's build, tests, or dev server.** Not once, not to "check it still works". Package managers reach the network and live-test suites connect to whatever the original authors pointed them at. The skill will refuse; do not talk it into it.
- **Decide who you are protecting.** The org and product stand-in names, the contributor mapping, and whether business-domain vocabulary is in scope are your calls. The skill will ask, and it will not guess.
- **Windows:** extract to a short path when verifying. `MAX_PATH` is 260 characters and a deep package tree fails partway through extraction, which looks exactly like archive corruption.

## The fastest path

Point the skill at a cloned repository and say what you want.

```
sanitize this repo — I want to keep it for study, no connections to the outside
```

It runs the six phases in order and stops to ask you about anything it cannot classify confidently.

## Phase 1 — disconnect

Do this first; it is the part that stops harm.

```powershell
git remote -v ; git branch -a ; git config --local --list
```

Preserve remote-only branches **before** removing the remote, or that history is orphaned permanently:

```powershell
git branch feature-x origin/feature-x
```

Then remove every remote, install a `pre-push` hook that exits non-zero unconditionally, and move `.github/workflows/` to `.github/workflows-archived/`. Do not delete the workflow files — CI/CD config is research material.

Test the hook against a **local bare repo**, never against a network remote.

## Phase 2 — inventory

Read-only. Changes nothing.

```powershell
python skills/repo-sanitize/scripts/inventory.py --repo <path-to-clone> --history
```

Without `--history` it scans `HEAD` only, which is faster and enough for a first look. With it, every blob ever committed.

You get seven sections: credential-shaped strings, first-party hostnames, likely-real GUIDs, email addresses, git identities, absolute user paths, binary blobs, and refs. Classify **every** hit as *sensitive*, *public constant*, or *test fixture* before you scrub anything.

## Phase 3 — triage credentials

The one judgment call that matters: **what breaks if the value changes?**

| Signal | Verdict | Action |
|---|---|---|
| A unit test asserts on it | fixture | leave it alone |
| Obviously sequential (`ghp_1234567890abc…`) | fixture | leave it alone |
| Published vendor example (`AKIAIOSFODNN7EXAMPLE`) | fixture | leave it alone |
| High entropy, assigned to a `password`/`secret`/`token` name, no test references it | real | placeholder it, purge history, **tell the operator** |

Real ones become `REPLACE_ME_<TYPE>_PLACEHOLDER` — unmistakable, never confusable with a working value.

To check history for credentials added then removed:

```powershell
git log --all --oneline -S"<pattern>"
```

`-S` is a **literal substring** search, so hits inside longer words are false positives. Confirm the surrounding context before reporting a leak.

## Phase 4 — scrub the working tree

Copy `assets/example.map`, adapt it, and keep the ordering: most-specific first.

Dry run first — it writes nothing:

```powershell
python skills/repo-sanitize/scripts/scrub_tree.py --repo <path> --map my.map
```

Read the output. The **`no matches`** list at the bottom is the useful part: a map entry that never fired is usually a typo, and a typo in the map is a value that ships unscrubbed.

Then apply:

```powershell
python skills/repo-sanitize/scripts/scrub_tree.py --repo <path> --map my.map --apply
```

Every file is sourced from its pristine `HEAD` blob, never from disk, so changing the map and re-running is a clean re-derivation rather than a compounding second edit.

Renames and deletions take JSON files:

```powershell
python skills/repo-sanitize/scripts/scrub_tree.py --repo <path> --map my.map --renames renames.json --delete drop.json --apply
```

Then handle what content substitution cannot reach: **filenames, directory names, and branch names.**

## Phase 5 — rewrite history

Commit the scrubbed tree first, then rewrite everything including that commit.

```powershell
git fast-export --all --signed-tags=strip --tag-of-filtered-object=rewrite -M |
  python skills/repo-sanitize/scripts/scrub_history.py --map my.map |
  git fast-import --force --quiet
```

**Always read the `UNMAPPED IDENTITIES` report on stderr.** It catches contributors your file-based inventory missed and prints ready-made `ident:` lines. Add them and re-run until the report is empty.

Then clean up, because none of this happens automatically:

```powershell
git reflog expire --expire=now --all
Remove-Item -Recurse -Force .git/logs
git gc --prune=now
git reset
```

`fast-import` updates refs and objects but not your files or your index, so the working tree is stale until you rewrite it from the new `HEAD`. Confirm `git status --porcelain` is empty before believing anything `git grep` tells you.

Set `git config --local user.name` and `user.email` to a pseudonym now. Any commit made after the final rewrite carries your real identity — including GitHub noreply addresses, which encode a user ID and a username.

## Phase 6 — verify, then freeze

```powershell
python skills/repo-sanitize/scripts/verify.py --repo <path> --needles needles.txt --expect-intact intact.txt
```

Two lists, two different failures:

- **`--needles`** — one string per line. Any hit is a leak.
- **`--expect-intact`** — one string per line. Any *missing* one is over-scrub. This is what catches `Romance` disappearing because you replaced `roman` without a word boundary.

Then freeze:

```powershell
python skills/repo-sanitize/scripts/freeze.py --src <path> --out archive.zip --root sanitized-repo --taint oldcorp acme-internal
```

`--root` matters: the source directory is usually still named after the original project, and zipping it directly reproduces that name in every archive path.

## Verify the artifact, not the source

This is the step most often skipped, and the one that catches packaging bugs. **Extract the zip to a short path and test that copy.**

```powershell
git fsck
git rev-list --all --count
git branch -a ; git tag
git remote -v                      # must be empty
git log --all --format="%an <%ae>" | Sort-Object -Unique
python skills/repo-sanitize/scripts/verify.py --repo <extracted> --needles needles.txt
```

Then attempt a push against a **local bare repo** and confirm the hook blocks it.

Verifying the source directory proves nothing about the artifact you shipped.

## Finishing

1. Write the **in-archive legend** — placeholder → meaning, no real values — and note which placeholders must stay distinct when rehydrating.
2. Write the **private decoder** outside the repository, hand it over, and say plainly that it must be stored apart from the zip.
3. Report any real leaked credentials, with file and commit. They may be live.
4. Delete the pre-rewrite backup.

## When to use something else

| You want | Use |
|---|---|
| to understand a repo before deciding to keep it | a deep-analysis pass, then this |
| to remove one secret from one recent commit | `git commit --amend` or an interactive rebase; this is heavy machinery |
| a shareable snapshot that keeps working links and CI | not this — the whole point is that nothing connects |
