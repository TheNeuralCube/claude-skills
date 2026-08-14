"""Phase 6 — freeze the sanitized repo into a zip.

    python freeze.py --src <repo> --out <file.zip> --root <generic-name>

Two things this handles that a plain `zip -r` does not:

1. The source directory is usually still named after the original project, so
   zipping it directly reproduces that name in every archive path. Entries are
   rewritten under --root instead.

2. Empty directories are preserved. After `git gc`, refs live in
   .git/packed-refs and .git/refs/ is left empty — and git's repository check
   requires refs/ to exist, so a files-only zip extracts into something git
   refuses to recognize. See references/pitfalls.md #10.
"""

import argparse
import os
import zipfile
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--root", required=True, help="generic top-level dir inside the zip")
    ap.add_argument("--taint", nargs="*", default=[],
                    help="terms that must not appear in any archive path")
    args = ap.parse_args()

    src, out, root = Path(args.src), Path(args.out), args.root.strip("/")
    files = raw = 0

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dirpath, dirnames, filenames in os.walk(src):
            dirnames.sort()
            rel_dir = Path(dirpath).relative_to(src).as_posix()
            if rel_dir != ".":
                z.writestr(zipfile.ZipInfo(f"{root}/{rel_dir}/"), b"")
            for fn in sorted(filenames):
                full = Path(dirpath) / fn
                if not full.is_file():
                    continue
                z.write(full, f"{root}/{full.relative_to(src).as_posix()}")
                files += 1
                raw += full.stat().st_size

    size = out.stat().st_size
    print(f"archive : {out}")
    print(f"root    : {root}/")
    print(f"files   : {files}")
    print(f"raw     : {raw/1048576:.1f} MB  ->  zipped {size/1048576:.1f} MB")

    with zipfile.ZipFile(out) as z:
        names = z.namelist()
    print(f".git included: {'yes' if any(n.startswith(root + '/.git/') for n in names) else 'NO — history missing!'}")

    bad = [n for n in names if any(t.lower() in n.lower() for t in args.taint)]
    print(f"paths carrying a tainted term: {len(bad)}")
    for b in bad[:10]:
        print("   !!", b)

    print("\nNow EXTRACT this zip to a SHORT path and verify that copy:")
    print("  git fsck / rev-list --count / branch / tag / remote -v")
    print("  git log --all --format='%an <%ae>' | sort -u")
    print("  python verify.py --repo <extracted> --needles ...")
    print("  attempt a push to a local bare repo and confirm the hook blocks it")
    print("(Windows MAX_PATH: extract somewhere shallow or extraction fails midway.)")


if __name__ == "__main__":
    main()
