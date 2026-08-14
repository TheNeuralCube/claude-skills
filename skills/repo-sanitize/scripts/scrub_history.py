"""Phase 5 — rewrite the whole history in one streaming pass.

    git fast-export --all --signed-tags=strip --tag-of-filtered-object=rewrite -M \
      | python scrub_history.py --map <file> \
      | git fast-import --force --quiet

Filters blob contents, commit/tag messages, and author/committer identities, and
drops paths matching `droppath:` rules. Offline; no git-filter-repo install and
no filter-branch checkout-per-commit.

Always read the UNMAPPED IDENTITIES report on stderr: it catches contributors a
file-based inventory missed. Re-run until it is empty.

Afterward you must still:
    git reflog expire --expire=now --all && rm -rf .git/logs && git gc --prune=now
    git reset            # fast-import does not touch the index
    <rewrite working-tree files from the new HEAD>
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sanitize_map import SanitizeMap  # noqa: E402

IDENT_RE = re.compile(rb"^(author|committer|tagger) (.*?) <(.*?)> (.*)$")
FILEMOD_RE = re.compile(rb"^M \d+ [^ ]+ (.*)$")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True)
    args = ap.parse_args()
    smap = SanitizeMap.load(args.map)

    src, dst = sys.stdin.buffer, sys.stdout.buffer
    stats = {"blobs": 0, "changed": 0, "msgs": 0, "idents": 0, "dropped": 0}
    unknown = set()
    pending = None  # 'blob' | 'message'

    while True:
        line = src.readline()
        if not line:
            break

        if line.startswith(b"blob"):
            pending = "blob"
            dst.write(line)
            continue

        if line.startswith(b"commit ") or line.startswith(b"tag "):
            pending = "message"
            dst.write(line)
            continue

        if line.startswith((b"author ", b"committer ", b"tagger ")):
            stripped = line.rstrip(b"\n")
            m = IDENT_RE.match(stripped)
            if m:
                kind, name, email, when = m.groups()
                key = (name.decode("utf-8", "replace"), email.decode("utf-8", "replace"))
                mapped = smap.map_identity(*key)
                if mapped:
                    stats["idents"] += 1
                    dst.write(b"%s %s <%s> %s\n" % (
                        kind, mapped[0].encode(), mapped[1].encode(), when))
                    continue
                unknown.add(key)
            dst.write(line)
            continue

        # Drop unwanted paths (build artifacts that embed absolute paths, etc.)
        m = FILEMOD_RE.match(line.rstrip(b"\n"))
        if m and smap.is_dropped(m.group(1).decode("utf-8", "replace")):
            stats["dropped"] += 1
            continue

        if line.startswith(b"data "):
            n = int(line[5:].strip())
            payload = src.read(n)
            if pending == "blob":
                stats["blobs"] += 1
                new = smap.apply_bytes(payload)
                if new != payload:
                    stats["changed"] += 1
                payload = new
            elif pending == "message":
                stats["msgs"] += 1
                payload = smap.apply_bytes(payload)
            dst.write(b"data %d\n" % len(payload))
            dst.write(payload)
            pending = None
            continue

        dst.write(line)

    dst.flush()
    print(
        f"[scrub_history] blobs={stats['blobs']} changed={stats['changed']} "
        f"messages={stats['msgs']} identities={stats['idents']} "
        f"paths_dropped={stats['dropped']}",
        file=sys.stderr,
    )
    if unknown:
        print("[scrub_history] UNMAPPED IDENTITIES — add these and re-run:", file=sys.stderr)
        for n, e in sorted(unknown):
            print(f"    ident:{n} <{e}>==>dev-N <dev-N@example.invalid>", file=sys.stderr)


if __name__ == "__main__":
    main()
