<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Roadmap

Deferred items and future direction for session-handoff. Nothing here is committed; the list records intent and the conditions under which each item would be taken up.

## Deferred from v0.1.0

| Item | Disposition |
|---|---|
| Org-specific variant | Packaged after the public push. The public core plus an org-config profile that wires organization sequencing, capture hooks, org naming and frontmatter fields, and `sanitization_prompt: always`. No org-specific behavior lives in the public core. |
| `document-sanitizer` sister skill | Candidate. Would become the general redaction engine that share-sanitize delegates to through the `redaction_provider` seam. share-sanitize does not change shape when it ships, because the contract held. |
| Extract redaction-policy into a shared standalone entity | Deferred. Proven first as a built-in here; extracted later when multiple skills consume it. |
| Promote the config-layer convention to a cross-skill standard | Proposed. Ratified after proving here. project-context invited to converge in v0.7.0 with a scoped migration. |
| Platform identity API for verified `approved_by` | Awaits platform support. `approved_by` stays self-asserted until then. |
| Programmatic file management (delete and upload via API) | Awaits platform support. The skill reports which files to manage; it does not delete or upload them. |
| Multi-collaborator handoffs | Post-v1.0. |
| Full ChatGPT Enterprise and Copilot validation | Schema is present in `config/platform-parameters.md` and `references/platform-specific-parameters.md`; full validation deferred. m365-copilot parameters remain `tbd` pending a dedicated research pass. |

## Conditions for v1.0.0

v0.1.0 stays at 0.x because update, consolidate, and share-sanitize are unproven. The path to v1.0.0:

1. The three new modes prove out in real use without identity, lineage, governance-propagation, or content-preservation defects.
2. The config-layer convention is ratified across the sister skills.
3. The retrofit and update-on-stale paths are exercised against a real prior schema (see Deferred verification below).

## Deferred verification

These items are asserted-not-verified in v0.1.0 and are tracked as explicit follow-up tasks, not as release blockers:

- **Claude.ai hosted-Project config-instantiation.** The `claude-ai` `config_instantiation: flat-prefix` value in `config/platform-parameters.md` is provisional and unverified: assumed per design spec section 8.4, not confirmed on a live Project. Live verification is a separate task. The assumption is the safe degrade, so behavior is correct even if the surface differs.
- **retrofit and update-on-stale (genesis-untestable).** See Schema evolution below.

## Schema evolution

The schema starts at "0.1" and is decoupled from the skill version. retrofit is implemented and ready for the first future schema bump, but at inception there is no older public schema to upgrade from, so the retrofit and update-on-stale paths are **genesis-untestable**: they cannot be exercised end-to-end until a prior public schema exists. This is expected for a genesis release and is not a release blocker. When the contract gains or changes a field, the schema bumps, `references/schema-changelog.md` gains an entry with a field-level diff and a retrofit path, the build-time drift-detection guard activates against the prior tag, and these paths become testable for the first time. See `references/schema-changelog.md`.
