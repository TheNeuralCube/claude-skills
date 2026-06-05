<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Usage

Per-mode walkthroughs for session-handoff. Every invocation begins with a pre-flight report; the operator confirms the proposed route with a token before any destructive write. See `references/preflight.md` for the protocol and `SKILL.md` for the router.

## Before you start

- session-handoff works on every surface, including Claude Code and Cowork. It never declines a surface; on filesystem surfaces the model-identity provenance is higher and the skill notes it.
- On first invocation the skill auto-creates `config/user-config.md`, `config/org-config.md`, and `config/redaction-policy.md` from their templates with placeholder defaults, and tells you. Populate them for full personalization (see "Configuring" below); the skill works with defaults if you do not.
- **A handoff has two zones.** Zone 1 is structured YAML: the metadata contract plus machine-parseable payload blocks (artifact state with verifiable markers, schemas, a state snapshot, decisions, open items, and a cold-start continuation playbook). Zone 2 is dense narrative prose that expands on Zone 1. The structured zone is what lets a resuming agent confirm it has the right files and pick up exactly where you left off. See the worked examples in `references/examples/`.

## generate: capture this session as a new handoff

Say "handoff this", "save this session", or "make this portable".

1. Pre-flight finds no prior handoff and returns `✓ Fresh`. It auto-proceeds (there is nothing to overwrite).
2. The skill derives the identity (`handoff_id`, version 1), fills the metadata contract, and writes the resumption payload for a cold-reading agent.
3. Post-flight confirms the file. Download it (or find it in your working directory) and move it to wherever the next session will read it.

The handoff is self-contained: identity, lineage, and governance live inside the document, and a continuation briefing tells the resuming agent where to pick up.

## update: produce a new version that supersedes the prior

Say "update the handoff" or "refresh the handoff".

1. Pre-flight finds the current-schema prior handoff and returns `✓ Update target found`. It proposes the update and asks for `confirm update`.
2. On the token, the skill preserves the `handoff_id`, increments the version, and sets `supersedes` to the prior version.
3. **Curation:** live items (open decisions, active open items, current state) carry at full fidelity. Items resolved since the prior version compress to one-line ledger entries; their detail stays in the retained prior version, which is the durable archive.
4. If the projected length is over the per-version budget, pre-flight surfaces a recommendation on what to compress. It never hard-blocks; you decide.
5. Post-flight reports what was carried and what was compressed.

If the prior handoff is at an older schema, update composes retrofit first (it upgrades the schema losslessly, then refreshes) and says so.

## consolidate: gather several handoffs into one

Say "consolidate these handoffs" or "merge these handoffs" with the sources selected.

1. Pre-flight returns `⚠ Consolidation set`, shows the sources and the derived governance, and asks for `confirm consolidate`.
2. The skill mints a **new** identity (a consolidation is a new artifact, never a continuation of a source), builds a `prior_handoffs` ledger, and sets `consolidation_depth`.
3. **Governance is most-restrictive:** a confidential source makes the consolidation confidential, frameworks union, retention takes the strictest. Sensitivity is never downgraded.
4. **The cap:** more than `max_sources` (default 3) in soft mode requires `confirm over-cap`; in hard mode it is refused. The cap protects review quality; the per-version budget is the real ceiling.
5. **Source retention:** sources are kept by default. Deleting a confidential, restricted, or framework-bearing source requires `confirm delete protected sources`. The flattened lineage is captured into the audit record so provenance survives deletion.
6. Post-flight reports the ledger, the derived governance, and any sources you may delete after verifying the result.

## retrofit: upgrade an older-schema handoff

Say "retrofit this" (one file) or "retrofit these files" (a folder).

1. Pre-flight returns `⚠ Retrofit needed`. A schema-only upgrade can auto-proceed or ask for `confirm retrofit` per your config; a batch asks for `confirm retrofit`.
2. The skill upgrades the frontmatter to the current schema and **preserves your content verbatim**. A content rewrite during a schema bump is a defect; the skill diffs before-and-after and halts if the content changed.
3. Identity and lineage are preserved; retrofit does not mint a new id or increment the version.
4. Post-flight reports the source and target schema per file and confirms content was preserved.

At inception (v0.1.0) there is no older public schema to upgrade from; retrofit is ready for the first future schema bump and for upgrading files an organization carries forward.

## share-sanitize: make a redacted copy for sharing (plain language)

Say "sanitize this for sharing" or "redact this for [recipient]".

**What it does, plainly:** it makes a **separate, redacted copy** of your handoff that is safe to share, and a short report (a "manifest") listing what kinds of things were removed and how many of each, without ever repeating the removed content. Your original handoff is untouched and stays the real, complete version. The copy is clearly marked as a redacted derivative.

1. Pre-flight shows the plan: which categories will be masked (based on the handoff's sensitivity and anything you name), how many candidates were found, and an honesty disclaimer. It asks for `confirm sanitize`.
2. On the token, the skill masks the sensitive spans (by default tagged like `[REDACTED:client_names]` so you can see what kind of thing was removed) and writes the redacted copy with `derivative_of` pointing back to your original.
3. It emits the manifest: counts by category, the number of PII items it flagged but you chose to keep, and the disclaimer.
4. Post-flight restates the manifest and reminds you to review the redacted copy before sharing.

**Two honesty points, always:** PII flagging is assistive. The skill flags possible PII for you to review and never claims to have caught all of it. Redaction is model-based and not guaranteed complete. Review the redacted output before sharing.

The always-on surfacing line ("Sanitization is available...") appears in every pre-flight regardless of configuration, so you never have to remember that this capability exists. Whether a blocking question also fires is set by `sanitization_prompt` in your user-config (`always`, `on-signal` default, or `never`).

## Configuring

To set up or change a config file, load it and say "walk me through configuring this." The skill runs a short interview, uses that file's field guide, and shows you a proposed new version as a diff. It saves only when you approve, and it never silently overwrites. A change to a governance field (sensitivity defaults, sanctioned destinations, redaction categories, the sanitize gate) is flagged as compliance-relevant in the approval summary.

| To change | Edit |
|---|---|
| your name, preferred platform, conventions, privacy defaults, the sanitize gate | `config/user-config.md` |
| org identity, compliance taxonomy, sanctioned destinations, governance overrides | `config/org-config.md` |
| redaction categories, masking style, sensitivity rules, the redaction provider | `config/redaction-policy.md` |

See `references/configure.md` for the interview procedure and the config templates for full field guides.
