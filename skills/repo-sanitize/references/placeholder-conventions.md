# Placeholder conventions

Placeholders are **variables, not redaction**. The same real value must become
the same placeholder everywhere — source, tests, docs, deploy config, commit
messages, and authorship alike. That is what lets someone trace the plumbing
afterward: if two files reference `<ENTRA_CLIENT_ID>`, they genuinely referred to
the same thing in the original system.

A one-way hash or a random token per occurrence destroys exactly the property
that makes the archive worth keeping.

## Forms

| Form | Use for | Why |
| --- | --- | --- |
| `*.invalid` | any hostname or domain | RFC 2606 reserves `.invalid`; it can never resolve in DNS, so nothing connects even by accident |
| `<UPPER_SNAKE>` | opaque identifiers an operator must supply — GUIDs, account locators, subscription IDs | visibly not a real value; greppable; reads as a template slot |
| one generic org name | company name, slug, domain, module path | keeps prose readable; pick something obviously fake (`Acme`, `Example Corp`) |
| stable pseudonyms | people (`dev-one` … `dev-n`) | same human always the same pseudonym, including across multiple identities |
| `REPLACE_ME_<TYPE>_PLACEHOLDER` | a **real** leaked credential | unmistakable; must never be confused with a working value |

## Rules

1. **One real value → exactly one placeholder.** Never map two distinct real
   values onto the same placeholder; it invents a relationship that did not
   exist.
2. **One human → one pseudonym**, even across several identities (work email,
   personal email, GitHub noreply, display name, handle, dotted username).
   Splitting them misrepresents the history as more contributors than there were.
3. **Order the map most-specific first.** `api.host.example` must be replaced
   before `host.example`, or you get `api.<already-replaced>`.
4. **Preserve semantic distinctions that carry security weight.** If two app
   registrations were deliberately separate — say, an SSO client and a database
   OAuth audience — they must get different placeholders, and the in-archive
   legend must say they cannot be collapsed. Merging them in a rehydrated system
   can turn a session token into a replayable database credential.
5. **Do not scrub public constants.** Microsoft's Azure CLI client ID
   `04b07795-8ddb-461a-bbee-02f9e1bf7b46` is the same for every tenant; RFC 4122
   example UUIDs and `example.com` are already placeholders. Replacing them
   destroys meaning and protects nothing.
6. **Fix prose collateral.** When the company name is also an ordinary English
   word, a blind map produces text like "a acme beacon". Add explicit
   phrase-level entries *before* the generic rules.

## The two legends

Always produce both. They are different documents with different audiences.

**In-archive** (`docs/TEMPLATE-PLACEHOLDERS.md` or similar) — placeholder →
*meaning*. What each variable stood for, which ones co-refer, and which must stay
distinct when rehydrating. Contains **no real values**. This is what makes the
archive researchable.

**Outside the archive** (`PRIVATE-LEGEND.md`) — real value → placeholder. The
decoder. Handed to the operator with an explicit instruction to store it apart
from the zip. If both ever sit in the same place, the sanitization is undone.
