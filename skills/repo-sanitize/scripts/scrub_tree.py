"""Phase 4 — scrub the working tree.

    python scrub_tree.py --repo <path> --map <file> [--apply]

Sources every file from its pristine HEAD blob, never from disk, so re-running
with a changed map is a clean re-derivation rather than a compounding second
edit (see references/pitfalls.md #6).

Supports path remapping (renames) and pristine restoration of excluded paths.
Without --apply this is a dry run and writes nothing.
"""

import argparse
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sanitize_map import SanitizeMap  # noqa: E402

SKIP_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".pdf", ".woff", ".woff2",
    ".ttf", ".eot", ".zip", ".gz", ".xlsx", ".docx", ".pptx", ".mp4", ".mov",
}


def git_bytes(repo, *args):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    return r.stdout if r.returncode == 0 else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--map", required=True)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--renames", help='JSON {"old/path": "new/path"} applied to outputs')
    ap.add_argument("--delete", help="JSON list of HEAD paths to omit entirely")
    args = ap.parse_args()

    repo = Path(args.repo)
    smap = SanitizeMap.load(args.map)
    renames = json.loads(Path(args.renames).read_text()) if args.renames else {}
    drop = set(json.loads(Path(args.delete).read_text())) if args.delete else set()

    listing = git_bytes(repo, "ls-tree", "-r", "HEAD", "--name-only", "-z")
    files = [p for p in listing.decode("utf-8").split("\0") if p]

    changed = restored = skipped = 0
    hits = Counter()

    for rel in files:
        if rel in drop:
            continue
        raw = git_bytes(repo, "show", f"HEAD:{rel}")
        if raw is None:
            print(f"WARN: no HEAD blob for {rel}", file=sys.stderr)
            continue

        out_path = repo / renames.get(rel, rel)
        excluded = smap.is_excluded(rel)
        binary = b"\0" in raw
        skip_ext = Path(rel).suffix.lower() in SKIP_SUFFIXES

        if excluded or binary or skip_ext:
            # Restore pristine bytes: an earlier pass may have damaged these.
            if args.apply:
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(raw)
            restored += excluded
            skipped += (binary or skip_ext) and not excluded
            continue

        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            if args.apply:
                out_path.write_bytes(raw)
            skipped += 1
            continue

        for old, _ in smap.literals:
            n = text.count(old)
            if n:
                hits[old] += n
        new = smap.apply_text(text)

        if args.apply:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            # newline="" preserves the file's original line endings exactly.
            with open(out_path, "w", encoding="utf-8", newline="") as fh:
                fh.write(new)
        if new != text:
            changed += 1

    print(f"=== {'APPLIED' if args.apply else 'DRY RUN'} ===")
    print(f"files changed         : {changed}")
    print(f"excluded (restored)   : {restored}")
    print(f"binary/asset skipped  : {skipped}")
    print(f"literal replacements  : {sum(hits.values())}\n")
    for old, n in hits.most_common(20):
        print(f"  {n:6d}  {old}")
    unused = [o for o, _ in smap.literals if o not in hits]
    if unused:
        print(f"\nno matches ({len(unused)}): {', '.join(unused[:15])}")
    print("\nNext: rename files/dirs/branches (content rules cannot reach those),")
    print("then commit, then run scrub_history.py.")


if __name__ == "__main__":
    main()
