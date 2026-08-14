# Pitfalls

Every entry here actually happened on the first full run. Each produced output
that looked correct. That is the danger: a bad sanitization does not throw an
error, it just quietly ships something wrong — either a leak you reported as
clean, or corruption you reported as faithful.

Check for each one deliberately. None will announce itself.

## 1. Names are substrings of ordinary words

A blind replace of contributor names mangles unrelated text.

Real collisions found in one mid-size repo:

| Replacing | Also matches | Result of a naive replace |
| --- | --- | --- |
| `justin` | `adjusting` | `ad<dev-three>g` |
| `sam` | `Sample`, `Samsung` | `<dev-two>ple` |
| `roman` | `Romance`, `Romanesco`, `Romantic` | `<dev-four>ce` |
| `Bao` | an npm `sha512-…` integrity hash | corrupted lockfile |
| `Luna` | `Lunasima` (a real Google Font) | invented font name |

**Fix:** anchor bare first names with `\b` word boundaries. Then add explicit
entries for camelCase identifiers (`baoGame`, `romanGame`), because `\b` will
*not* match inside them — that is the point.

**Verify:** after scrubbing, assert the collision words still exist. If
`Romance` disappeared, you corrupted it.

## 2. Vendored third-party data is not the target's IP

Skill bundles, `vendor/`, font catalogs, design-token corpora, fixture datasets.
Substituting into them corrupts real product names and protects nothing.

**Fix:** exclude those path prefixes and restore them to pristine `HEAD` bytes,
in case an earlier pass already damaged them.

**Watch for:** history filters that cannot see paths. A `fast-export` stream
emits blobs before the `M <mode> <ref> <path>` line that names them, so
path-based exclusion is awkward there. Prefer precise word-boundary rules that
are safe everywhere over path exclusions you cannot enforce in both passes.

## 3. Binary blobs leak, and text search cannot see them

Compiled Python caches (`.pyc`) embed the absolute source path in `co_filename`.
One real example:

```
C:\Users\<username>\OneDrive - <Company Name>\Documents\GitHub\<repo>\...
```

That is a username, a corporate tenant name, and a directory tree — in a file no
text-mode `grep -I` will ever show you, and which UTF-8 decoding in a scrubber
skips as binary.

**Fix:** scan *every* blob as raw bytes. For build artifacts with no research
value (`__pycache__/`, `*.pyc`, `*.pyo`, compiled output), drop the path from
history entirely rather than trying to rewrite it.

**Also check:** office documents, images with EXIF, `.DS_Store`, IDE caches,
`.zip`/`.jar` fixtures.

## 4. Refs are not content

A history filter rewrites blobs, messages, and identities. It does **not** touch
branch names, tag names, or reflog paths.

Real example: branch `dev/luna-image-paste-300` survived a full content rewrite
untouched, and reappeared as a file path inside `.git/logs/`.

**Fix:** `git branch -m`, `git tag` rename, then `rm -rf .git/logs` after
expiring reflogs. Enumerate `git for-each-ref` and read the names.

## 5. Filenames and directories are not content either

`oldcorpTheme.ts`, `LunaLogo.tsx`, `oldcorp-energy-logo.webp`, and the
repository directory itself. The archive root path is the one most often missed —
zipping `./the-original-name/` reproduces it in every entry.

**Fix:** rename files to match already-scrubbed import statements, and write the
zip with an explicit generic root.

## 6. Re-running a changed map over already-edited files compounds

If pass 1 maps `oldcorp → example` and the operator then asks for `acme`, you
cannot simply map `example → acme`: the tree now contains pre-existing
`example.com`, `.env.example`, and the English word "example" that were never
the company.

**Fix:** always source file content from the pristine `HEAD` blob, never from
disk. Then a map change is a clean re-derivation instead of a second edit.

## 7. Commits made after the final rewrite keep your real identity

Fixing a doc *after* rewriting history reintroduces your name and email — and
GitHub noreply addresses (`12345678+username@users.noreply.github.com`) carry a
user ID and username.

**Fix:** set `git config --local user.name/user.email` to a pseudonym inside the
archive, and re-run the filter if you commit again. Always read the filter's
unmapped-identity report.

## 8. Deliberate secret-shaped fixtures must survive

`AKIAIOSFODNN7EXAMPLE` is AWS's published documentation example.
`ghp_1234567890abcdefghijklmnopqrstuvwxyz` is obviously sequential. These exist
to test redaction and secret-detection code.

Randomizing them breaks the feature they test **and** misleads the operator into
thinking real keys were found.

**Test:** if a unit test asserts on the value, it is a fixture, not a leak.

## 9. `git log -S` is a literal substring search

`-S"Roman"` matches `Romance`. `-S"bao"` matches a base64 hash. A leak scan
built on `-S` alone produces false positives that waste a review cycle — and
worse, trains you to dismiss real hits.

**Fix:** confirm every hit's surrounding context before reporting it. Report
counts *with* context, never counts alone.

## 10. Packaging drops empty directories

After `git gc`, refs are packed into `.git/packed-refs` and `.git/refs/` is left
as empty directories. A files-only zip omits them — and git's repository check
requires `refs/` to exist, so the extracted copy fails with *"not a git
repository"* while the source works perfectly.

**Fix:** write explicit directory entries. **Verify by extracting**, not by
inspecting the source.

## 11. Deep paths break extraction on Windows

Windows `MAX_PATH` is 260 characters. A repo with deep package trees extracted
into an already-deep directory fails partway with `FileNotFoundError`, leaving a
half-extracted tree that looks like archive corruption.

**Fix:** extract to a short path when verifying. Mention the constraint to the
operator rather than letting them hit it later.

## 12. The working tree is stale after `fast-import`

`fast-import` updates refs and objects. Your files on disk and your index are
untouched, so `git status` and `git grep` report the *old* content and mislead
your verification.

**Fix:** after importing, `git reset` to resync the index and rewrite every file
from the new `HEAD` blob. Confirm `git status --porcelain` is empty.
