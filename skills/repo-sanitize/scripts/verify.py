"""Phase 6 — verify. Scans EVERY object in the repository, binary included.

    python verify.py --repo <path> --needles <file> [--expect-intact <file>]

--needles       one string per line; any hit is a failure
--expect-intact one string per line; any MISSING one is a failure, catching
                over-eager substitution (e.g. a font name or English word that
                collided with a contributor's name)

Exits non-zero if anything fails. Run this against the EXTRACTED archive, not
the source directory — see references/pitfalls.md #10.
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path


def git(repo, *args, binary=False):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--needles", required=True)
    ap.add_argument("--expect-intact")
    args = ap.parse_args()
    repo = args.repo

    needles = [l.strip() for l in Path(args.needles).read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")]
    intact = ([l.strip() for l in Path(args.expect_intact).read_text(encoding="utf-8").splitlines()
               if l.strip() and not l.startswith("#")] if args.expect_intact else [])

    leaks = {n: [] for n in needles}
    found_intact = {n: 0 for n in intact}

    listing = git(repo, "rev-list", "--all", "--objects").splitlines()
    scanned = 0
    for line in listing:
        parts = line.split(" ", 1)
        sha, path = parts[0], (parts[1] if len(parts) > 1 else "")
        if git(repo, "cat-file", "-t", sha).strip() != "blob":
            continue
        data = git(repo, "cat-file", "blob", sha, binary=True)
        scanned += 1
        for n in needles:
            if n.encode("utf-8") in data:
                leaks[n].append(path or sha)
        for n in intact:
            if n.encode("utf-8") in data:
                found_intact[n] += 1

    fail = False
    print(f"scanned {scanned} blobs (binary included)\n")

    print("--- LEAK CHECK ---")
    for n, where in leaks.items():
        if where:
            fail = True
            print(f"  !! LEAK  {n}  in {len(where)} blob(s), e.g. {where[0][:60]}")
    if not fail:
        print("  clean — no needle found in any object")

    if intact:
        print("\n--- OVER-SCRUB CHECK (these must still exist) ---")
        for n, c in found_intact.items():
            if c == 0:
                fail = True
                print(f"  !! LOST  {n}  — substitution damaged unrelated content")
            else:
                print(f"  ok       {n} ({c})")

    print("\n--- STRUCTURE ---")
    remotes = git(repo, "remote", "-v").strip()
    print(f"  remotes        : {remotes or '(none)'}" + ("   !! EXPECTED NONE" if remotes else ""))
    if remotes:
        fail = True
    hook = Path(repo) / ".git" / "hooks" / "pre-push"
    print(f"  pre-push hook  : {'present' if hook.exists() else '!! MISSING'}")
    fail = fail or not hook.exists()
    wf = Path(repo) / ".github" / "workflows"
    print(f"  .github/workflows: {'!! PRESENT' if wf.is_dir() else 'absent'}")
    fail = fail or wf.is_dir()
    print(f"  commits        : {git(repo, 'rev-list', '--all', '--count').strip()}")

    print("\n--- REFS (content filters never rewrite these) ---")
    for r in git(repo, "for-each-ref", "--format=%(refname)").splitlines():
        flag = ""
        for n in needles:
            if re.search(re.escape(n), r, re.I):
                flag = "   !! carries a scrubbed term"
                fail = True
        print(f"  {r}{flag}")

    print("\n--- IDENTITIES ---")
    for i in sorted(set(git(repo, "log", "--all", "--format=%an <%ae>").splitlines()) |
                    set(git(repo, "log", "--all", "--format=%cn <%ce>").splitlines())):
        print(f"  {i}")

    print("\nRESULT:", "FAIL" if fail else "PASS")
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
