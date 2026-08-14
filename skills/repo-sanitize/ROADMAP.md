<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Roadmap

Deferred items and future direction for `repo-sanitize`. Nothing here is committed; the list records intent and the conditions under which each item would be taken up.

## Deferred from 0.1.0

| Item | Disposition |
|---|---|
| **Binary content substitution** | Deliberately not done, and unlikely to change. `apply_bytes` returns non-UTF-8 data untouched; binary that leaks is dropped by path instead. Rewriting inside a `.pyc`, an office document, or an image container risks corrupting a file in a way no test would catch. Revisit only with format-aware handlers, one format at a time. |
| **EXIF, office-document, and `.DS_Store` scrubbing** | Named in `references/pitfalls.md` #3 as things to check, not yet automated. `inventory.py` flags binary blobs so a human can triage them; nothing strips their metadata. Candidate for 0.2.0 as a report-only extension first. |
| **Automatic branch, tag, and ref renaming** | Manual. `inventory.py` and `verify.py` both print refs and `verify.py` flags any ref carrying a scrubbed term, but the rename is a human `git branch -m`. Automating it means deciding what a scrubbed branch name should be, which is a naming judgment the skill is not allowed to make unsupervised. |
| **A generated needles file** | Manual. `verify.py` takes `--needles` and `--expect-intact` as operator-supplied lists. Deriving needles from the map's left-hand side would be a small script and would close the gap where a map entry exists but nobody thought to verify it. Strong candidate for 0.2.0. |
| **Map linting** | Partial. `scrub_tree.py` reports map entries that matched nothing, which catches typos. It does not check ordering, so a general rule placed before a specific one silently wins. A pre-flight ordering check is a candidate. |
| **Non-git version control** | Not planned. The entire history phase is `fast-export` and `fast-import`. Mercurial or Subversion would be a different skill. |
| **Verification of the leaked-credential report** | Manual. The skill reports what it found; confirming whether a credential is still live is the operator's call and would require a network request, which the skill is forbidden from making. |

## Conditions for 1.0.0

0.1.x stays at 0.x because the protocol is calibrated against a single real run.

1. Three complete runs against structurally different repositories — at minimum one polyglot monorepo, one repository with vendored third-party corpora, and one with a long multi-contributor history.
2. At least one run where `verify.py --expect-intact` catches a real over-scrub before the archive ships, proving the over-scrub check earns its place.
3. At least one run producing zero unmapped identities on the first `scrub_history.py` pass, proving the inventory is sufficient rather than merely a starting point.
4. A generated-needles path, so verification no longer depends on the operator remembering what they asked to be scrubbed.
5. No new entry added to `references/pitfalls.md` during a full run.

## Known limitations

- **Verification proves the absence of what you asked about.** `verify.py` scans every object for the needles it is given. A value nobody thought to list is a value nobody checked for. This is the structural limit of the approach, and the reason Phase 2 classification is not optional.
- **Binary blobs are dropped, not cleaned.** Anything with research value inside a binary is lost rather than sanitized. For build artifacts this is correct; for a fixture corpus it is a real cost.
- **The map is ordered by hand.** Most-specific-first is a documented rule, not an enforced one. A misordered map produces plausible-looking output.
- **One human, one pseudonym is asserted, not verified.** Nothing detects that two identities in the map belong to the same person. Splitting a contributor in two misrepresents the history and no check will notice.
- **Windows path length.** Deep package trees plus a deep extraction directory exceed `MAX_PATH` and fail partway through, which reads as archive corruption. Documented in `USAGE.md` and `pitfalls.md` #11; not worked around in code.
