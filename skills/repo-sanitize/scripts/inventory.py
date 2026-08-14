"""Phase 2 — discover what needs sanitizing. Read-only; changes nothing.

    python inventory.py --repo <path> [--history]

Reports hostnames, GUIDs, cloud resources, identities, credential-shaped
strings, and binary blobs. Classify every finding as sensitive / public
constant / test fixture before scrubbing anything.
"""

import argparse
import re
import subprocess
from collections import Counter, defaultdict

# Values that are public constants, not anyone's secret. Never scrub these.
PUBLIC_CONSTANTS = {
    "04b07795-8ddb-461a-bbee-02f9e1bf7b46",  # Microsoft Azure CLI client id
    "123e4567-e89b-42d3-a456-426614174000",  # RFC 4122 example
    "3f2504e0-4f89-11d3-9a0c-0305e82c3301",  # RFC 4122 example
}
PUBLIC_HOST_HINTS = (
    "example.com", "example.org", "example.net", "localhost", "127.0.0.1",
    "api.openai.com", "api.anthropic.com", "github.com", "githubusercontent.com",
    "npmjs.org", "pypi.org", "golang.org", "microsoft.com", "azure.com",
    "schemas.", "w3.org", "jsdelivr.net", "cloudflare.com", "posthog.com",
)
# Secret-shaped by design: inputs that test redaction code. Preserve them.
KNOWN_FIXTURES = {"AKIAIOSFODNN7EXAMPLE", "ghp_1234567890abcdefghijklmnopqrstuvwxyz"}

CRED_PATTERNS = [
    ("anthropic key",  re.compile(rb"sk-ant-[A-Za-z0-9_\-]{20,}")),
    ("openai key",     re.compile(rb"sk-[A-Za-z0-9]{32,}")),
    ("github token",   re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}")),
    ("github pat",     re.compile(rb"github_pat_[A-Za-z0-9_]{30,}")),
    ("slack token",    re.compile(rb"xox[baprs]-[A-Za-z0-9-]{10,}")),
    ("aws key id",     re.compile(rb"AKIA[0-9A-Z]{16}")),
    ("google api key", re.compile(rb"AIza[0-9A-Za-z_\-]{30,}")),
    ("private key",    re.compile(rb"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("jwt",            re.compile(rb"eyJ[A-Za-z0-9_\-]{15,}\.[A-Za-z0-9_\-]{15,}\.")),
    ("assigned secret", re.compile(
        rb"(?i)(password|passwd|secret|token|api[_-]?key|client[_-]?secret)"
        rb"\s*[:=]\s*[\"']?([A-Za-z0-9_\-./+=]{16,})")),
]
GUID_RE = re.compile(rb"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
HOST_RE = re.compile(rb"\b(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}\b")
EMAIL_RE = re.compile(rb"\b[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}\b")
WINPATH_RE = re.compile(rb"[A-Za-z]:\\Users\\[^\\\s\"']+")


def git(repo, *args, binary=False):
    r = subprocess.run(["git", *args], cwd=repo, capture_output=True)
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def synthetic_guid(g: str) -> bool:
    body = g.replace("-", "")
    if len(set(body)) <= 2:
        return True
    return bool(re.match(r"^(dead|beef|0{4}|1{4}|f{4})", body, re.I))


def iter_blobs(repo, history):
    """Yield (path, bytes). With --history, every blob ever committed."""
    if history:
        listing = git(repo, "rev-list", "--all", "--objects").splitlines()
        for line in listing:
            parts = line.split(" ", 1)
            sha, path = parts[0], (parts[1] if len(parts) > 1 else "")
            if git(repo, "cat-file", "-t", sha).strip() != "blob":
                continue
            yield path or sha, git(repo, "cat-file", "blob", sha, binary=True)
    else:
        for path in filter(None, git(repo, "ls-files", "-z").split("\0")):
            yield path, git(repo, "show", f"HEAD:{path}", binary=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--history", action="store_true",
                    help="scan every blob ever committed, not just HEAD")
    args = ap.parse_args()
    repo = args.repo

    hosts, guids, emails = Counter(), Counter(), Counter()
    creds = defaultdict(set)
    winpaths, binaries = set(), []

    for path, data in iter_blobs(repo, args.history):
        if b"\0" in data:
            binaries.append(path)
            for m in WINPATH_RE.findall(data):
                winpaths.add((path, m.decode("utf-8", "replace")))
            continue
        for m in HOST_RE.findall(data):
            hosts[m.decode()] += 1
        for m in GUID_RE.findall(data):
            guids[m.decode()] += 1
        for m in EMAIL_RE.findall(data):
            emails[m.decode()] += 1
        for m in WINPATH_RE.findall(data):
            winpaths.add((path, m.decode("utf-8", "replace")))
        for label, rx in CRED_PATTERNS:
            for m in rx.findall(data):
                val = (m[1] if isinstance(m, tuple) else m).decode("utf-8", "replace")
                if val in KNOWN_FIXTURES:
                    continue
                creds[label].add((path, val[:12] + "..."))

    def section(title):
        print(f"\n{'='*66}\n{title}\n{'='*66}")

    section("CREDENTIAL-SHAPED (triage each: real leak vs. test fixture)")
    if creds:
        for label, items in sorted(creds.items()):
            print(f"\n  [{label}]")
            for p, v in sorted(items)[:12]:
                print(f"      {v:<18} {p[:60]}")
        print("\n  Rule: if a test asserts on the value, it is a fixture — preserve it.")
        print("  Otherwise treat as REAL: placeholder it, purge history, TELL THE OPERATOR.")
    else:
        print("  none found")

    section("FIRST-PARTY HOSTNAMES (public/CDN/vendor filtered out)")
    for h, n in hosts.most_common():
        if any(k in h.lower() for k in PUBLIC_HOST_HINTS):
            continue
        if h.count(".") >= 1 and not h.lower().endswith((".md", ".ts", ".go", ".py", ".js", ".json", ".yml", ".tsx")):
            print(f"  {n:5d}  {h}")

    section("GUIDs — likely real (synthetic + public constants filtered)")
    for g, n in guids.most_common():
        if g in PUBLIC_CONSTANTS or synthetic_guid(g):
            continue
        print(f"  {n:5d}  {g}")

    section("EMAIL ADDRESSES")
    for e, n in emails.most_common(40):
        print(f"  {n:5d}  {e}")

    section("GIT IDENTITIES (authors + committers, all refs)")
    ids = Counter(git(repo, "log", "--all", "--format=%an <%ae>").splitlines())
    ids.update(git(repo, "log", "--all", "--format=%cn <%ce>").splitlines())
    for i, n in ids.most_common():
        print(f"  {n:5d}  {i}")

    section("ABSOLUTE USER PATHS (leak usernames / tenant names)")
    if winpaths:
        for p, w in sorted(winpaths)[:20]:
            print(f"  {w[:72]}\n      in {p[:60]}")
    else:
        print("  none found")

    section("BINARY BLOBS — text scrubbing cannot see inside these")
    if binaries:
        for b in sorted(set(binaries))[:25]:
            print(f"  {b}")
        print("\n  Build artifacts (.pyc/.pyo/__pycache__) embed absolute source")
        print("  paths. Prefer dropping them by path over rewriting them.")
    else:
        print("  none")

    section("REFS — not content; a history filter will NOT rewrite these")
    for r in git(repo, "for-each-ref", "--format=%(refname)").splitlines():
        print(f"  {r}")


if __name__ == "__main__":
    main()
