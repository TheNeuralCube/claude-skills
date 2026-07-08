#!/usr/bin/env python3
"""Deterministic conformance checks for Core Sample skill files and deliverables.

Usage:
  python core_sample_checks.py check <file> [<file> ...]
  python core_sample_checks.py filename --date YYYY-MM-DD --slug <target-slug> --lens <lens-tag>

The check command runs every applicable check on each file and exits nonzero on
any failure. Checks applied per file:
  dashes       every file: no em dash (U+2014) or en dash (U+2013) anywhere
  description  files with a YAML frontmatter description field: under 1024 chars
  gap_count    files with a YAML frontmatter gap_count field: value matches the
               count of [INFORMATION GAP: markers in the body

The filename command prints a deliverable filename conforming to
{YYYY-MM-DD}_{target-slug}_{lens-tag}_core-sample.md and validates its parts.
"""
import argparse
import re
import sys
from pathlib import Path

EM_DASH = chr(0x2014)
EN_DASH = chr(0x2013)
DESCRIPTION_LIMIT = 1024
LENS_TAGS = ["design-spec", "build-spec", "craft-study", "review", "security-review", "plan", "audit"]
GAP_MARKER = "[INFORMATION GAP:"


def split_frontmatter(text):
    """Return (frontmatter_text, body_text); frontmatter_text is None if absent."""
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n(.*)\Z", text, re.S)
    if m:
        return m.group(1), m.group(2)
    return None, text


def check_dashes(path, text):
    problems = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for ch, label in ((EM_DASH, "em dash U+2014"), (EN_DASH, "en dash U+2013")):
            col = line.find(ch)
            if col != -1:
                problems.append(f"{path}:{lineno}:{col + 1}: {label}")
    return problems


def check_description(path, frontmatter):
    m = re.search(r'^description:\s*"(.*?)"\s*$', frontmatter, re.M | re.S)
    if not m:
        m = re.search(r"^description:\s*(.+)$", frontmatter, re.M)
    if not m:
        return []
    length = len(m.group(1))
    if length >= DESCRIPTION_LIMIT:
        return [f"{path}: description is {length} chars; must be under {DESCRIPTION_LIMIT}"]
    return []


def check_gap_count(path, frontmatter, body):
    m = re.search(r"^gap_count:\s*(\S+)\s*$", frontmatter, re.M)
    if not m:
        return []
    declared = m.group(1)
    if not declared.isdigit():
        return [f"{path}: gap_count is not an integer: {declared!r}"]
    actual = body.count(GAP_MARKER)
    if int(declared) != actual:
        return [f"{path}: gap_count says {declared} but body has {actual} {GAP_MARKER} markers"]
    return []


def cmd_check(args):
    problems = []
    for name in args.files:
        path = Path(name)
        if not path.is_file():
            problems.append(f"{path}: not a file")
            continue
        text = path.read_text(encoding="utf-8")
        problems.extend(check_dashes(path, text))
        frontmatter, body = split_frontmatter(text)
        if frontmatter is not None:
            problems.extend(check_description(path, frontmatter))
            problems.extend(check_gap_count(path, frontmatter, body))
    if problems:
        print("\n".join(problems))
        print(f"FAIL: {len(problems)} problem(s)")
        return 1
    print(f"OK: {len(args.files)} file(s) clean")
    return 0


def cmd_filename(args):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", args.date):
        print(f"date must be YYYY-MM-DD, got {args.date!r}")
        return 1
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        print(f"slug must be lowercase kebab-case, got {args.slug!r}")
        return 1
    if args.lens not in LENS_TAGS:
        print(f"lens must be one of {', '.join(LENS_TAGS)}, got {args.lens!r}")
        return 1
    print(f"{args.date}_{args.slug}_{args.lens}_core-sample.md")
    return 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    p_check = sub.add_parser("check", help="run conformance checks on files")
    p_check.add_argument("files", nargs="+")
    p_check.set_defaults(func=cmd_check)
    p_name = sub.add_parser("filename", help="generate a conforming deliverable filename")
    p_name.add_argument("--date", required=True)
    p_name.add_argument("--slug", required=True)
    p_name.add_argument("--lens", required=True)
    p_name.set_defaults(func=cmd_filename)
    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
