"""Shared parser for the sanitization map used by scrub_tree and scrub_history.

One map drives both the working-tree pass and the history rewrite, so the two
cannot drift. Pure stdlib.

Format — one directive per line, '#' starts a comment:

    OLD==>NEW                  literal replacement (most-specific first)
    regex:PATTERN==>REPL       regex replacement, applied after all literals
    protect:WORD               shielded from every rule, then restored
    ident:Name <email>==>New Name <new@email>
    droppath:REGEX             file paths matched are removed from history
    excludepath:PREFIX         paths restored pristine, never substituted

Ordering matters for literals and is preserved as written.
"""

import re
from pathlib import Path

# Private-use codepoint; cannot collide with real content.
_SENTINEL = ""


class SanitizeMap:
    def __init__(self):
        self.literals = []      # [(old, new)]
        self.regexes = []       # [(compiled, repl)]
        self.protect = []       # [word]
        self.identities = {}    # {(name, email): (name, email)}
        self.droppath = []      # [compiled]
        self.excludepath = []   # [prefix]

    # -- application -------------------------------------------------------

    def apply_text(self, text: str) -> str:
        shields = {}
        for i, word in enumerate(self.protect):
            token = f"{_SENTINEL}{i}{_SENTINEL}"
            if word in text:
                shields[token] = word
                text = text.replace(word, token)
        for old, new in self.literals:
            text = text.replace(old, new)
        for rx, repl in self.regexes:
            text = rx.sub(repl, text)
        for token, word in shields.items():
            text = text.replace(token, word)
        return text

    def apply_bytes(self, data: bytes) -> bytes:
        """UTF-8 text is scrubbed; anything else is returned untouched.

        Binary is deliberately not substituted — see references/pitfalls.md #3.
        Binary that leaks should be dropped by path, not rewritten.
        """
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            return data
        return self.apply_text(text).encode("utf-8")

    def map_identity(self, name: str, email: str):
        return self.identities.get((name, email))

    def is_excluded(self, path: str) -> bool:
        return any(path.startswith(p) for p in self.excludepath)

    def is_dropped(self, path: str) -> bool:
        return any(rx.search(path) for rx in self.droppath)

    # -- parsing -----------------------------------------------------------

    @classmethod
    def load(cls, path) -> "SanitizeMap":
        m = cls()
        for lineno, raw in enumerate(
            Path(path).read_text(encoding="utf-8").splitlines(), 1
        ):
            line = raw.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("protect:"):
                m.protect.append(line[len("protect:"):].strip())
                continue
            if line.startswith("droppath:"):
                m.droppath.append(re.compile(line[len("droppath:"):].strip()))
                continue
            if line.startswith("excludepath:"):
                m.excludepath.append(line[len("excludepath:"):].strip())
                continue

            if "==>" not in line:
                raise SystemExit(f"line {lineno}: expected '==>' in {raw!r}")
            lhs, rhs = line.split("==>", 1)

            if lhs.startswith("regex:"):
                m.regexes.append((re.compile(lhs[len("regex:"):]), rhs))
                continue
            if lhs.startswith("ident:"):
                a = _split_ident(lhs[len("ident:"):].strip())
                b = _split_ident(rhs.strip())
                if not a or not b:
                    raise SystemExit(f"line {lineno}: bad ident, want 'Name <email>'")
                m.identities[a] = b
                continue

            if not lhs:
                raise SystemExit(f"line {lineno}: empty search term")
            m.literals.append((lhs, rhs))
        return m


_IDENT_RE = re.compile(r"^(.*?)\s*<(.*?)>$")


def _split_ident(s):
    mt = _IDENT_RE.match(s)
    return (mt.group(1), mt.group(2)) if mt else None
