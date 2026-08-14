---
name: repo-sanitize
version: 0.1.0
description: >-
  Sanitize a cloned or forked repository into a safe, disconnected, frozen
  archive for research. Disconnects it from all git remotes, neutralizes CI/CD,
  replaces every real hostname, tenant/app GUID, cloud resource, database name
  and contributor identity with stable placeholders, detects and neutralizes
  credentials the original authors leaked, rewrites the entire git history so
  nothing survives in old commits, and freezes the result to a zip. Trigger
  phrases - sanitize this repo, scrub this clone, disconnect this from GitHub,
  make this repo safe to keep, freeze this repo, glacier archive, templatize
  this repo, strip identifiers, anonymize a repo, remove secrets from history,
  archive someone else's harness, safe fork for research, no connections to the
  outside. Use when keeping a third-party repo for study, or turning an internal
  repo into a shareable template.
---

# repo-sanitize

## Version history

| Version | Date | Changes |
|---|---|---|
| 0.1.0 | 2026-08-14 | Initial release. Extracted from the first full sanitization run (an enterprise AI harness frozen for research). Encodes the six-phase protocol, the binary/vendored/word-boundary failure modes found during that run, and the leaked-credential policy. |

## Purpose

Turn a repository you did not write — or one you did, but want to hand out — into
an archive that is **safe to keep, safe to read, and unable to reach anything**.

Three outcomes, in priority order:

1. **It cannot connect.** No remotes, no CI/CD, no pushes, no live endpoints.
2. **It carries no secrets or identities.** Including ones the original authors
   leaked by accident, and including everything buried in git history.
3. **It remains intelligible.** Placeholders are stable variables, not noise, so
   the architecture can still be studied and traced.

The third is what separates this from `rm -rf .git`. An archive nobody can learn
from has no reason to exist.

## Non-negotiable rules

1. **Never run the project's build, tests, or dev server.** Package managers
   fetch from the network; `*_live_test`-style suites attempt real connections
   to whatever the original authors pointed them at. Read the code instead. If
   the operator asks whether verification is safe, the answer is that running it
   is exactly the risk they are trying to avoid.
2. **Scrubbing the working tree alone is cosmetic.** Until history is rewritten,
   `git show HEAD:<path>` returns every original value. Say so plainly; do not
   report a working-tree scrub as done.
3. **Verify by extracting the finished archive**, never by inspecting the source
   directory. Bugs hide in packaging. See `references/pitfalls.md`.
4. **Never invent a replacement for a value you have not identified.** If you
   cannot classify a string, show it to the operator and ask.
5. **The private decoder never enters the archive.** Write it outside the repo.
6. **Real leaked credentials are reported to the operator, never silently
   dropped.** They may need rotating, and the upstream author may need telling.

## Phase 1 — Disconnect

Do this before anything else; it is the part that stops harm.

```bash
git remote -v && git branch -a && git config --local --list
```

- **Preserve remote-only branches first.** `git branch <name> origin/<name>` for
  each. Removing the remote otherwise orphans that history permanently.
- `git remote remove <each>`. Confirm `refs/remotes` is empty afterward.
- Install a `pre-push` hook that exits non-zero unconditionally, so a re-added
  remote still cannot push. **Test it against a local bare repo** — never against
  a network remote.
- Move `.github/workflows/` to `.github/workflows-archived/` and delete the
  original directory. Do not delete the files; CI/CD config is research material.
  Leave a README explaining what was disabled and why.
- Check for other automation that reaches out: `.mcp.json`, devcontainer
  `postCreateCommand`, git hooks already in `.git/hooks`, `Taskfile`/`Makefile`
  targets that curl or push. Report what you find.

## Phase 2 — Inventory

Run `scripts/inventory.py`. It reports, without changing anything:

- hostnames and FQDNs, split into first-party vs. known-public
- GUIDs, split into likely-real vs. obviously synthetic
- cloud resource names, storage accounts, database/role/warehouse names
- contributor names, emails, and handles — from files **and** `git log`
- credential-shaped strings and high-entropy blobs
- **binary blobs**, which text search cannot see

Classify every hit into: *sensitive*, *public constant*, or *test fixture*.
Do not proceed until each is classified. Bring ambiguous ones to the operator.

## Phase 3 — Leaked credentials

The operator's concern is other people's mistakes. Apply this policy:

**A real credential** — matches a known format (`sk-ant-`, `ghp_`, `AKIA…`,
`AIza…`, `xox[baprs]-`, PEM private keys, JWTs) or is a high-entropy string
assigned to a `password`/`secret`/`token`/`key` name, and is **not** referenced
by a redaction test.

→ Replace with an unmistakable placeholder: `REPLACE_ME_<TYPE>_PLACEHOLDER`.
→ Scrub it from history too.
→ **Report it to the operator explicitly**, with file and commit. It may be live.

**A deliberate test fixture** — secret-shaped by design because it is the input
that tests redaction or secret-detection code.

→ **Leave it alone.** `AKIAIOSFODNN7EXAMPLE` is AWS's own documentation example.
Sequential fakes like `ghp_1234567890abc…` are equally deliberate. Randomizing
these breaks the feature they test and makes it look like real keys were found.

Distinguish them by asking what breaks if the value changes. If a test asserts
on it, it is a fixture.

Also check history for credentials added then removed:

```bash
git log --all --oneline -S"<pattern>"
```

Beware: `-S` is a literal substring search, so hits inside longer words are
false positives. Confirm context before reporting a leak.

## Phase 4 — Scrub the working tree

Build an ordered replacement map, most-specific first, then run
`scripts/scrub_tree.py`.

**Source every file from its pristine `HEAD` blob, never from disk.** If the map
changes and you re-run over already-edited files, substitutions compound and
corrupt silently. This also lets you restore excluded paths to pristine if an
earlier pass damaged them.

Conventions in `references/placeholder-conventions.md`. In short: `*.invalid`
for hostnames (RFC 2606, cannot resolve), `<UPPER_SNAKE>` for opaque
identifiers, one generic org name throughout, stable pseudonyms for people.

Exclusions that matter:

- **Vendored third-party data** (`skills/`, `vendor/`, fixture corpora). Not the
  target's IP, and substitution corrupts real product names.
- **Public constants.** Microsoft's Azure CLI client ID
  `04b07795-8ddb-461a-bbee-02f9e1bf7b46` is identical in every tenant on earth.
  Replacing it destroys meaning and protects nothing.

Then handle what content substitution cannot reach: **filenames, directory
names, and branch names**. Rename them to match the scrubbed references.

## Phase 5 — Rewrite history

Commit the scrubbed tree first, then rewrite everything including that commit.

Use `git fast-export | scripts/scrub_history.py | git fast-import --force`.
Single pass, fully offline, no `git filter-branch` (hundreds of checkouts) and
no `git-filter-repo` install (network).

The filter handles blob contents, commit messages, author/committer identities,
and drops paths that should not exist at all. It **reports unmapped identities**
— always read that output; it catches contributors your file-based inventory
missed.

Afterward:

```bash
git reflog expire --expire=now --all
rm -rf .git/logs          # stale reflog paths can carry old branch names
git gc --prune=now
git reset                 # resync the index; fast-import does not touch it
```

Then **sync the working tree from the rewritten HEAD** — `fast-import` updates
refs and objects, not your files, so they are stale until you rewrite them.

Any commit you make *after* the final rewrite keeps your real identity. Set
`git config --local user.name/user.email` to a pseudonym, and re-run the filter
if you commit again.

## Phase 6 — Verify, then freeze

Run `scripts/verify.py`: it scans **every object in the repository, binary
included**, not just `HEAD`.

Then `scripts/freeze.py`, which writes the zip with a generic root directory —
the source folder is usually still named after the original project — and
preserves empty directory entries.

**Verification means extracting the zip and testing that copy**: `git fsck`,
commit count, branch and tag names, `git remote -v` empty, authors, a push
attempt against a local bare repo, and a re-run of the leak scan. Verifying the
source directory proves nothing about the artifact you shipped.

Finally, write two legends:

- **In-archive**: placeholder → meaning, and which placeholders must stay
  distinct when rehydrating. No real values.
- **Outside the archive**: real → placeholder. Hand it to the operator and tell
  them to store it separately.

Then delete any pre-rewrite backup, which holds exactly what you removed.

## Help

### For the Operator

This skill turns a repo you cloned — yours or someone else's — into a frozen
archive that is safe to keep and study. It cuts every connection (remotes, CI/CD,
pushes), swaps real hostnames, cloud IDs, database names and people for
consistent stand-in names, finds and neutralizes any passwords or API keys the
original authors left lying around, scrubs all of it out of the git history so
it cannot be recovered from old commits, and zips the result.

You get the architecture intact and readable, with none of the plumbing that
could expose you or anyone else. You also get a private decoder file — keep it
somewhere separate from the zip, or the whole exercise is undone.

Expect to be asked to confirm the naming scheme, the contributor mapping, and
anything ambiguous. Expect to be told if a real credential turns up; it may need
rotating, and the upstream author may deserve a heads-up.

### For the Agent

Execute phases in order. Phase 1 first — it is the part that stops harm.

Sequence: disconnect → inventory → credential policy → scrub tree (from pristine
HEAD) → rewrite history → verify from the extracted zip → legends → delete
backups.

Non-negotiables, repeated because they are the ones that get skipped:

1. Never run the target's build, tests, or dev server.
2. A working-tree scrub is cosmetic until history is rewritten. Never report it
   as complete.
3. Verify by extracting the finished archive, not by inspecting the source.
4. Report real leaked credentials to the operator; never silently drop them.
5. Preserve deliberate secret-detection fixtures.
6. The private decoder stays outside the archive.

Read `references/pitfalls.md` before Phase 4. It documents the failure modes
that produced silent, plausible-looking corruption on the first real run —
substring collisions in ordinary words, vendored data, binary blobs embedding
build paths, refs that content filters cannot see, and packaging that drops
empty directories. Each was invisible without deliberately checking for it.

Ask the operator to decide: the org/product stand-in names, the contributor
mapping, whether business-domain terms are in scope, and any string you cannot
confidently classify. Do not guess at identity mappings — a wrong one either
leaks a real person or misrepresents history by splitting one contributor into
two.

## Deliverables

A completed run produces four things. Name them explicitly when you report done:

1. The frozen zip, with a generic root directory.
2. The in-archive legend (`docs/TEMPLATE-PLACEHOLDERS.md` or similar) —
   placeholder → meaning, no real values.
3. The private decoder, written **outside** the repository and handed to the
   operator with instructions to store it apart from the zip.
4. A leaked-credential report, or an explicit statement that none were found.
