#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Raul J. Soto
"""Repository conformance checks for claude-skills.

Enforces the contract in CLAUDE.md. Run before every pull request and every
release; CI runs exactly this.

    python scripts/validate-repo.py

Exits 0 when the repository conforms, 1 otherwise. Every failure names the
file and the rule, so it can be fixed without reading this script.

Requires PyYAML for strict frontmatter parsing. Without it, the frontmatter
checks are skipped loudly rather than silently passing, because a lenient
parse is exactly the failure mode this script exists to catch.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    yaml = None

REPO = Path(__file__).resolve().parent.parent

REQUIRED_SKILL_FILES = ("SKILL.md", "README.md", "CHANGELOG.md", "ROADMAP.md", "USAGE.md")

ALLOWED_ROOT_FILES = {
    "README.md", "CLAUDE.md", "AGENTS.md", "CONTRIBUTING.md",
    "LICENSE", "NOTICE", ".gitignore", ".gitattributes",
}
ALLOWED_ROOT_DIRS = {"skills", "docs", "scripts", ".github", "_build_inputs", "dist", ".git",
                     ".claude"}  # local agent settings; globally gitignored, never committed

SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
VERSION_IN_NAME = re.compile(r"[-_]v?\d+[-._]\d+")
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
DESCRIPTION_LIMIT = 1024

failures: list[str] = []
notes: list[str] = []


def fail(path: object, rule: str) -> None:
    failures.append(f"{path}: {rule}")


def frontmatter(text: str) -> str | None:
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    return m.group(1) if m else None


def check_root() -> None:
    """The root holds only what CLAUDE.md permits. This is the no-stray-skill gate."""
    for entry in REPO.iterdir():
        name = entry.name
        if entry.is_dir():
            if name not in ALLOWED_ROOT_DIRS:
                fail(name + "/", "unexpected directory at the repository root; see CLAUDE.md layout contract")
        elif name not in ALLOWED_ROOT_FILES:
            if name.endswith((".skill", ".zip")) or name == "MANIFEST.sha256":
                fail(name, "build artifact committed at the root; build into dist/ and attach to the Release")
            elif name.endswith("release-notes.md"):
                fail(name, "release notes at the root; they belong in the Release body and the skill CHANGELOG")
            else:
                fail(name, "unexpected file at the repository root; see CLAUDE.md layout contract")


def check_no_stray_skills() -> None:
    """A SKILL.md may live only at skills/<name>/SKILL.md."""
    for path in REPO.rglob("SKILL.md"):
        if ".git" in path.parts or "dist" in path.parts or "_build_inputs" in path.parts:
            continue
        rel = path.relative_to(REPO)
        if len(rel.parts) != 3 or rel.parts[0] != "skills":
            fail(rel, "SKILL.md outside skills/<skill-name>/ -- never publish a skill to the repository root")


def check_skill(skill_dir: Path) -> str | None:
    """Validate one skill. Returns its declared version, or None."""
    rel = skill_dir.relative_to(REPO)
    name = skill_dir.name

    if not SKILL_NAME.match(name):
        fail(rel, "directory name must be lowercase kebab-case")
    if VERSION_IN_NAME.search(name):
        fail(rel, "version in the directory name; versions live only in the SKILL.md frontmatter")
    if name.startswith("nc3-"):
        fail(rel, "retired nc3- prefix in the directory name")

    for required in REQUIRED_SKILL_FILES:
        if not (skill_dir / required).is_file():
            fail(rel / required, "required file is missing")

    if (skill_dir / "LICENSE").exists():
        fail(rel / "LICENSE", "per-skill LICENSE; the root LICENSE and NOTICE cover every skill")

    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return None

    text = skill_md.read_text(encoding="utf-8")
    raw = frontmatter(text)
    if raw is None:
        fail(rel / "SKILL.md", "no YAML frontmatter block")
        return None

    if yaml is None:
        notes.append("PyYAML not installed: frontmatter checks skipped (pip install pyyaml)")
        return None

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        detail = str(exc).splitlines()[0]
        fail(rel / "SKILL.md", f"frontmatter is not valid YAML ({detail}); write description as a folded block scalar (>-)")
        return None

    if not isinstance(data, dict):
        fail(rel / "SKILL.md", "frontmatter is not a mapping")
        return None

    if data.get("name") != name:
        fail(rel / "SKILL.md", f"YAML name {data.get('name')!r} does not match directory {name!r}")

    version = data.get("version")
    if version is None:
        fail(rel / "SKILL.md", "no version field; declare dotted semver here and nowhere else")
    elif not SEMVER.match(str(version)):
        fail(rel / "SKILL.md", f"version {version!r} is not three-part dotted semver")

    description = data.get("description")
    if not description:
        fail(rel / "SKILL.md", "no description field")
    elif len(description) > DESCRIPTION_LIMIT:
        fail(rel / "SKILL.md", f"description is {len(description)} characters; the limit is {DESCRIPTION_LIMIT}")

    h1 = next((ln.strip() for ln in text.splitlines() if ln.startswith("# ")), None)
    if h1 is None:
        fail(rel / "SKILL.md", "no H1 heading")
    elif h1 != f"# {name}":
        fail(rel / "SKILL.md", f"H1 is {h1!r}; it must be '# {name}' with no version suffix")

    return str(version) if version else None


def check_readme_index(versions: dict[str, str]) -> None:
    """The README skill index must list every skill at its current version."""
    readme = REPO / "README.md"
    if not readme.is_file():
        fail("README.md", "missing")
        return
    text = readme.read_text(encoding="utf-8")
    for name, version in sorted(versions.items()):
        row = next((ln for ln in text.splitlines()
                    if ln.startswith("|") and f"[{name}]" in ln), None)
        if row is None:
            fail("README.md", f"skill index has no row for {name}")
            continue
        cells = [c.strip() for c in row.strip("|").split("|")]
        if version not in cells:
            fail("README.md", f"skill index lists {name} at a stale version; SKILL.md declares {version}")
        tag = f"{name}-v{version}"
        if f"releases/download/{tag}/{name}.skill" not in row:
            fail("README.md", f"{name} download link is not pinned to {tag}/{name}.skill")
        if "blob/main" in row:
            fail("README.md", f"{name} row links to blob/main; pin links to the release tag")


def main() -> int:
    check_root()
    check_no_stray_skills()

    skills_dir = REPO / "skills"
    if not skills_dir.is_dir():
        fail("skills/", "directory is missing")
        return report()

    versions: dict[str, str] = {}
    for skill_dir in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        version = check_skill(skill_dir)
        if version:
            versions[skill_dir.name] = version

    if not versions:
        fail("skills/", "no valid skills found")

    check_readme_index(versions)
    return report(versions)


def report(versions: dict[str, str] | None = None) -> int:
    for note in notes:
        print(f"NOTE  {note}")
    if versions:
        print(f"Checked {len(versions)} skills: " + ", ".join(f"{k} {v}" for k, v in sorted(versions.items())))
    if failures:
        print(f"\n{len(failures)} failure(s):\n")
        for f in failures:
            print(f"  FAIL  {f}")
        print("\nSee CLAUDE.md for the contract behind each rule.")
        return 1
    print("\nPASS: repository conforms to CLAUDE.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
