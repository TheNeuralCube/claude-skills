<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# repo-sanitize

Turns a repository you cloned — someone else's or your own — into an archive that is **safe to keep, safe to read, and unable to reach anything**. It cuts every outbound connection, replaces real hostnames, cloud identifiers, database names and contributor identities with stable placeholders, finds and neutralizes credentials the original authors leaked, rewrites the entire git history so none of it survives in old commits, and freezes the result to a zip.

The distinguishing constraint is the third outcome: **the archive stays intelligible.** Placeholders are variables, not redaction, so the same real value becomes the same placeholder everywhere and the architecture can still be traced. An archive nobody can learn from has no reason to exist, which is what separates this from `rm -rf .git`.

- **License:** Apache 2.0 (SPDX headers on the repo wrapper files; the scripts and the skill payload carry none).
- **Skill version:** 0.1.0, declared in the SKILL.md frontmatter.
- **Provenance:** extracted from one full sanitization run against a real enterprise AI harness. Every entry in `references/pitfalls.md` is a failure that actually occurred on that run.

## The three outcomes, in priority order

1. **It cannot connect.** No remotes, no CI/CD, no pushes, no live endpoints.
2. **It carries no secrets or identities.** Including the ones the original authors leaked by accident, and including everything buried in git history.
3. **It remains intelligible.** Stable placeholders, a legend, and a documented rule for which placeholders must stay distinct when rehydrating.

## The six phases

| Phase | Does | Tooling |
|---|---|---|
| 1. Disconnect | preserve remote-only branches, remove remotes, install a refusing `pre-push` hook, archive CI/CD workflows, find other outbound automation | manual `git` |
| 2. Inventory | report hostnames, GUIDs, cloud resources, identities, credential-shaped strings, absolute user paths, binary blobs, and refs — changing nothing | `scripts/inventory.py` |
| 3. Leaked credentials | separate real leaks from deliberate secret-detection fixtures; placeholder the former, preserve the latter, report the former to the operator | policy in SKILL.md |
| 4. Scrub the tree | apply an ordered replacement map, sourcing every file from its pristine `HEAD` blob; then rename files, directories, and branches | `scripts/scrub_tree.py` |
| 5. Rewrite history | one streaming `fast-export` to `fast-import` pass over blobs, messages, identities, and dropped paths | `scripts/scrub_history.py` |
| 6. Verify and freeze | scan every object including binaries, then zip under a generic root with empty directories preserved | `scripts/verify.py`, `scripts/freeze.py` |

## The rules that keep it honest

These are load-bearing. Each exists because skipping it produced output that looked correct and was not.

- **Never run the target's build, tests, or dev server.** Package managers fetch from the network and `*_live_test`-style suites attempt real connections to whatever the original authors pointed them at. Running the code is exactly the risk the operator is trying to avoid.
- **A working-tree scrub is cosmetic until history is rewritten.** Until then `git show HEAD:<path>` still returns every original value. The skill is forbidden from reporting a tree scrub as done.
- **Verify by extracting the finished archive**, never by inspecting the source directory. Bugs hide in packaging — see pitfall #10, where the source repo worked perfectly and the extracted copy was not a git repository at all.
- **Never invent a replacement for a value you have not identified.** Unclassifiable strings go to the operator.
- **The private decoder never enters the archive.** If the decoder and the zip ever sit in the same place, the sanitization is undone.
- **Real leaked credentials are reported, never silently dropped.** They may be live, and the upstream author may need telling.
- **Deliberate secret-shaped fixtures are preserved.** `AKIAIOSFODNN7EXAMPLE` is AWS's own documentation example. Randomizing it breaks the redaction feature it tests and misleads the operator into thinking a real key was found.

## Two legends, always both

| Legend | Direction | Lives | Contains |
|---|---|---|---|
| In-archive | placeholder → meaning | inside the zip | what each variable stood for, which ones co-refer, which must stay distinct. **No real values.** |
| Private decoder | real value → placeholder | outside the zip, handed to the operator | the decoder, stored separately or the exercise is undone |

## Scripts

Pure stdlib Python, no installs, fully offline. One shared map (`sanitize_map.py`) drives both the working-tree pass and the history rewrite, so the two cannot drift.

```
repo-sanitize/
  SKILL.md                            the six-phase protocol and the non-negotiable rules
  assets/
    example.map                       annotated template map; copy and adapt
  references/
    pitfalls.md                       12 failure modes, each observed on a real run
    placeholder-conventions.md        placeholder forms, ordering rules, the two legends
  scripts/
    inventory.py                      phase 2, read-only discovery
    sanitize_map.py                   shared map parser for both passes
    scrub_tree.py                     phase 4, working-tree scrub from pristine HEAD
    scrub_history.py                  phase 5, fast-export stream filter
    verify.py                         phase 6, every-object leak and over-scrub check
    freeze.py                         phase 6, zip with a generic root
```

## Map format

One directive per line, ordered most-specific first; `#` starts a comment.

| Directive | Effect |
|---|---|
| `OLD==>NEW` | literal replacement, applied in written order |
| `regex:PATTERN==>REPL` | regex replacement, applied after all literals |
| `protect:WORD` | shielded from every rule, then restored |
| `ident:Name <email>==>New <email>` | commit authorship, history rewrite only |
| `droppath:REGEX` | matching paths removed from history entirely |
| `excludepath:PREFIX` | matching paths restored pristine, never substituted |

## Known limitations

Binary content is deliberately **not** substituted — it is dropped by path instead. Verification is read-only and cannot prove absence of a secret it was not given as a needle. See `ROADMAP.md` for the full list.
