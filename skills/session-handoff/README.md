<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# session-handoff

A public, brand-free portability skill that gives any AI-literate user a high-fidelity, machine-readable handoff of a working session that any agent on any platform can resume cold.

A handoff is a **forward transfer of working state, optimized for a future AI agent as its primary reader**. It is a deliberate, higher-fidelity alternative to the lossy auto-compaction the platforms perform: the operator controls fidelity, not the platform.

- **License:** Apache 2.0 (SPDX headers on source files; none on generated handoffs).
- **Skill version:** 0.1.0. **Schema version:** "0.1". These are decoupled and start near 0.1 by coincidence, not coupling (see `references/schema-changelog.md`).
- **Lineage:** the public-ized successor to an internal v1.5 predecessor skill. The generate and retrofit cores carry forward; update, consolidate, and share-sanitize are new.
- **Sister skill:** project-context (shipped). session-handoff mirrors its portability and governance scaffolding and shares the config-layer convention described below.

## What it does

Five modes ship in v0.1.0, behind one auto-routed entry point:

| Mode | Use it to | Trigger |
|---|---|---|
| generate | capture the current session as a new handoff | "handoff this", "save this session", "make this portable" |
| update | produce a new version that supersedes the prior | "update the handoff", "refresh the handoff" |
| consolidate | gather several handoffs into one | "consolidate these handoffs", "merge these handoffs" |
| retrofit | upgrade an older-schema handoff, content preserved | "retrofit this", "retrofit these files" |
| share-sanitize | produce a redacted copy plus a manifest for sharing | "sanitize this for sharing", "redact this for [recipient]" |

A mandatory pre-flight check detects prior handoffs, classifies the input, and proposes the operation with a verdict and a confirmation token before any write. See `references/preflight.md`.

## When to use session-handoff versus project-context

The two skills are complementary, not competing.

| | session-handoff | project-context |
|---|---|---|
| Output | one self-contained handoff of a working session, optimized for a resuming agent | a rolling three-file project memory (active, entities, archive) that accretes over many sessions |
| Frame | a forward transfer across a session, platform, or person boundary | durable grounding for a long-running project |
| Lifecycle | per-handoff, versioned and consolidatable | continuous, with scoring and decay |
| Surfaces | every surface, including Claude Code and Cowork; never declines a surface | hosted Projects only; declines Claude Code |

Use session-handoff to move state across a boundary. Use project-context to keep a project grounded over time. They share the `_managed_by` registry-marker convention and an org-config.

## Customization: the layered config model

Behavior is calibrated by configuration, not by fork. A personal user gets a light, ignorable experience; an enterprise gets a rigorous one. The same skill serves both.

### The three layers

Resolution order: `config/user-config.md` > `config/org-config.md` > skill defaults in `references/defaults.md`.

| File | Tier | Holds |
|---|---|---|
| `config/user-config.md` | user | your identity, preferred platform, conventions, privacy defaults, the `sanitization_prompt` gate, the PII-flagging toggle |
| `config/org-config.md` | org | org identity, the compliance taxonomy (sensitivity defaults, regulatory scope), sanctioned destinations, governance overrides, methodology hooks |
| `config/redaction-policy.md` | org or user | redaction categories, masking style, `sensitivity_rules`, PII-flagging mechanics, the `redaction_provider` switch |
| `config/platform-parameters.md` | skill or platform | per-platform limits, feature support, overflow strategy, config-instantiation layout (shipped; rarely edited) |
| `references/defaults.md` | skill (not editable) | the universal public defaults |

`config/` holds files that are yours to edit; `references/` holds files the skill owns. If a file is in `config/`, you may edit it; if it is in `references/`, the skill owns it.

### How to configure

On first invocation, the skill auto-creates the config files from their `.template` files with placeholder defaults, and tells you it did. To populate one, load it and say "walk me through configuring this." The skill runs the shared interview (`references/configure.md`), uses that file's field guide, and writes you a new version as a diff for approval. It never silent-overwrites. A change to a governance field (sanctioned destinations, sensitivity defaults, redaction categories, the sanitize gate) is flagged as compliance-relevant in the approval summary, because at a public company a config change is a compliance action.

On filesystem surfaces (Claude Code, Cowork) `config/` is a real directory. On hosted Projects where knowledge is a flat list, `config/` degrades to a `config-` name prefix; the intent is preserved. See `references/platform-specific-parameters.md`.

## Redaction posture (share-sanitize)

share-sanitize is built as **the seam, not the engine**. The redaction step is a stable contract (in: a handoff plus a policy; out: a redacted copy plus a manifest of categories and counts, never the content), and behind it is a `redaction_provider` switch.

- v0.1.0 ships a deliberately minimal, model-driven built-in redactor (`redaction_provider: built-in`).
- When a future `document-sanitizer` sister skill ships and becomes the general redaction engine, the switch flips and share-sanitize does not change shape, because the contract held.

The redacted copy is a leaf derivative: same `handoff_id`, `derivative_of` set, `generation_mode: sanitized`, not part of the supersession chain. The canonical handoff is unchanged.

## The two honesty guardrails

These are stated plainly and are not softened:

- **PII flagging is assistive, not a guarantee.** The skill flags possible PII for review and never claims to have found or removed all PII. Redaction is model-based and not guaranteed complete; review the redacted output before sharing.
- **`approved_by` is self-asserted, not verified.** It populates from `config/user-config.md` identity or is null. Verbatim: "approved_by is self-asserted from user-config identity. It is not platform-verified and must not be treated as authenticated identity until a platform identity API exists."

## Governance and enterprise features

All eight enterprise features ship in the core, calibrated by config: governance metadata on every handoff, governance-aware redaction, a shared org-config across sister skills, sanctioned-destination awareness, the redaction manifest, a receiving-agent handling block, PII flagging, and the provenance-and-audit block. Public defaults are light (`sensitivity: internal`, frameworks empty); enterprise org-config populates the taxonomy. See `references/governance.md`.

Consolidation derives governance most-restrictively from its sources (a confidential source makes the consolidation confidential; frameworks union; retention takes the strictest). Deleting a protected source requires an explicit token, and the flattened lineage is captured into the audit record so provenance survives deletion. See `references/lineage.md`.

## The config-layer convention (a proposed cross-skill standard)

This release introduces one intentional divergence from the project-context benchmark, proposed as a cross-skill convention to be ratified after it is proven here:

1. A dedicated `config/` directory for editable files, separate from skill-owned `references/`.
2. A single shared `references/configure.md` that owns the interview mechanics once; field guides are local to each config file; interview logic is never duplicated.
3. Self-documenting, AI-walkable config files with a standard header and a local field guide.
4. Approval-diff discipline: config regeneration produces a diff for approval, never a silent overwrite.

project-context is invited to converge on this in v0.7.0.

## Files

See the tree in `SKILL.md`. The authoritative references are `references/schema.md` (the contract), `references/preflight.md` (the protocol), `references/lineage.md`, `references/redaction.md`, and `references/governance.md`. Worked examples live in `references/examples/`.

## Provenance and credit

session-handoff carries forward the generate and retrofit logic from an internal v1.5 predecessor skill, renamed and brand-stripped for public release. Two internal dependencies (a naming-and-versioning conventions skill and a capture-pipeline skill) are removed from the core; all operator-specific and organization-specific behavior lives in config. A separately-packaged org-specific variant layers this public core via an org-config profile.
