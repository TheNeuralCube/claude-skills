---
name: session-handoff
version: 0.1.0
description: >
  Capture a high-fidelity, machine-readable handoff of the current working session that
  any AI agent on any platform can resume cold. One entry point auto-routes to five modes
  through a mandatory pre-flight check. Use when the operator says: "handoff this", "save
  this session", "make this portable", "create a handoff" (generate); "update the handoff",
  "refresh the handoff" (update); "consolidate these handoffs", "merge these handoffs"
  (consolidate); "retrofit this", "retrofit these files" (retrofit); or "sanitize this for
  sharing", "redact this for sharing" (share-sanitize). Produces a self-contained handoff
  with a versioned metadata contract, lineage, and governance. Pre-flight detects prior
  handoffs and proposes the operation before any write.
---

## Protocol

This skill operates under a mandatory pre-flight protocol. Before any output
is generated, before any other section of this skill applies, you MUST:

1. Complete the pre-flight check defined in references/preflight.md.
2. Emit the pre-flight report block (per references/preflight.md format) as
   the first content in your response to the operator.
3. Always emit the locked sanitization-surfacing line (references/preflight.md
   section 5) within the report.
4. Where the verdict requires operator confirmation (per the report's
   "To proceed" line), wait for the operator's confirmation token. Do not
   generate output, do not write a handoff, do not propose files until the
   matching token is received.

Failure to complete pre-flight before generation is a protocol violation,
not an optimization. Operator urgency, perceived skill execution context,
or any other condition does not license skipping pre-flight. If project
knowledge access fails and pre-flight cannot complete, refuse to proceed
and surface the failure to the operator.

All modes described in subsequent sections (generate, update, consolidate,
retrofit, share-sanitize) are conditional on pre-flight completion. Do not
read further as actionable instruction until pre-flight has emitted its
report and any required confirmation has been received.

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# session-handoff (v0.1.0)

A thin-router skill. This file detects the invocation, runs the mandatory pre-flight protocol (`## Protocol` above), and delegates to one of five mode files. Mode logic lives in `modes/`. The schema, lineage, redaction, governance, configuration interview, defaults, platform parameters, and the pre-flight / post-flight protocol live in `references/`. Editable configuration lives in `config/`.

session-handoff is the public, brand-free successor to an internal predecessor skill (v1.5). It is renamed because the output is a **forward transfer**, not a backward recap: a handoff is optimized for a future AI agent as its primary reader, a deliberate higher-fidelity alternative to the lossy auto-compaction the platforms perform. The generate and retrofit cores carry forward from v1.5; update, consolidate, and share-sanitize are new in v0.1.0. The schema starts at "0.1", decoupled from the skill version. Provenance and credit are recorded in `CHANGELOG.md`. See also `references/schema-changelog.md`.

A handoff has two zones: Zone 1 is structured machine-parseable YAML (the tier-1 metadata contract plus the tier-2 payload blocks), Zone 2 is the dense narrative body that expands on Zone 1. This is inherited from the predecessor skill: anything an agent can programmatically extract or verify goes in Zone 1. See `references/schema.md` section 2 and `references/section-activation.md`.

Key references the router and modes consume: `references/preflight.md` (pre-flight algorithm, verdicts, token catalog, routing table, sanitization surfacing, surface awareness, post-flight), `references/schema.md` (two-zone model, two-tier metadata contract, the tier-2 payload block summary, `schema_version: "0.1"`, governance, provenance and audit blocks, no-empty-fields rule), `references/section-activation.md` (Zone 2 narrative section set, conditional activation, ordering, writing rules), `references/schema-changelog.md` (Supported Schemas, 0.1 inception, schema-versus-skill decoupling), `references/lineage.md` (supersession, consolidation identity, governance propagation, source retention, derivative identity), `references/redaction.md` (built-in redactor, manifest, the `redaction_provider` seam), `references/governance.md` (sensitivity taxonomy, resolution order, receiving-agent handling block), `references/configure.md` (the shared config interview), `references/defaults.md` (universal public defaults), `references/platform-specific-parameters.md` (per-platform schema and config-instantiation layout). The canonical tier-2 payload field-by-field schema is owned by `modes/generate.md`.

## Model-assumption disclosure

This skill is optimized for top-tier thinking models (Claude Opus 4.5+, GPT-5 Pro thinking, Gemini Ultra thinking, equivalents). The primary reader of a handoff is such a model resuming work cold, not a human skimmer. Self-containment beats brevity.

## When to use this skill

Invoke session-handoff to move working state across a session boundary, a platform boundary, or a person boundary. One entry point; pre-flight auto-routes to the right mode.

| Mode | Trigger phrases | What it does |
|---|---|---|
| generate | "handoff this", "save this session", "make this portable", "create a handoff" | Produce one new handoff from the current conversation. |
| update | "update the handoff", "refresh the handoff" | Produce a new version that supersedes the prior, same `handoff_id`, version incremented. |
| consolidate | "consolidate these handoffs", "merge these handoffs" | Gather N prior handoffs into one consolidated handoff with a new identity and a source ledger. |
| retrofit | "retrofit this", "retrofit these files" | Upgrade an older-schema handoff (or a folder of them) to the current schema, content preserved verbatim. |
| share-sanitize | "sanitize this for sharing", "redact this for [recipient]" | Produce a redacted derivative copy plus a manifest of what was removed. |

The three core jobs: platform migration (resume a conversation on a different platform), user handoff (share state with a different person, where share-sanitize applies), and fresh context window (start a clean session with operator-controlled fidelity, where update lives).

## Routing rules

When the skill is invoked, the router:

1. **Runs pre-flight** (`references/preflight.md`), which detects prior handoffs via the `_managed_by: session-handoff-skill` marker, classifies the input state, and proposes one operation with a verdict and (where required) a confirmation token.
2. **Auto-routes** per the routing table below. The operator confirms the proposed route before any destructive write.

| Pre-flight detects | Proposed mode | Token | Content behavior |
|---|---|---|---|
| no prior handoff, fresh session | generate | auto-proceeds | new |
| current-schema handoff plus new conversation | update | `confirm update` | folded and curated |
| stale-schema handoff, no new content | retrofit (schema-only) | auto-proceeds or `confirm retrofit` per config | preserved verbatim |
| stale-schema handoff plus new conversation | retrofit then update | `confirm update` | migrate, then fold and curate |
| N prior handoffs selected | consolidate | `confirm consolidate` | new consolidated identity |
| batch of stale-schema files | batch retrofit | `confirm retrofit` | preserved verbatim |
| sharing or sensitive content signaled | share-sanitize | `confirm sanitize` | redacted derivative |

3. **Loads the mode file** (`modes/<mode>.md`) and runs its body to completion.
4. **Applies configuration** by loading `config/user-config.md`, `config/org-config.md`, and `config/redaction-policy.md` if present; resolution order is user > org > skill defaults from `references/defaults.md`.

retrofit and update stay distinct internal paths because their content rules are opposite (retrofit is lossless; update is intrinsically lossy, curating to a budget). A single shared content default would risk silently rewriting archival content. The operator-facing surface is unified anyway; pre-flight catches a misroute before any write.

The router itself does not parse the conversation, mint identities, derive governance, or write files. It detects intent, runs pre-flight, and hands off.

## Sanitization is always surfaced

Pre-flight always emits this line verbatim, on every invocation, regardless of configuration:

```
Sanitization is available. If this handoff will be shared with another person, run
share-sanitize to produce a redacted copy and a manifest of what was removed. Say
"sanitize this for sharing" to invoke it.
```

The blocking sanitize question (distinct from the always-on surfacing line) is gated by `sanitization_prompt` (`config/user-config.md`, default `on-signal`). See `references/preflight.md` section 5.

## Surface awareness, never decline

session-handoff is the cross-surface tool and never declines a surface. It keeps awareness that Claude Code and Cowork yield higher model-identity provenance (the skill can read its execution environment, so `generated_by` is reliable and `model_source: system-reported`), and notes it in pre-flight, but does not refuse on any surface. On hosted chat surfaces, model identity may be operator-stated; the skill records that and proceeds. This inverts the project-context surface guard, which is deliberately not adopted.

## The two honesty guardrails

- **PII flagging is assistive, not a guarantee.** The skill flags possible PII for review and never claims to have found or removed all PII.
- **`approved_by` is self-asserted, not verified.** It populates from `config/user-config.md` identity or is null. It is not platform-verified and must not be treated as authenticated identity until a platform identity API exists.

## Output behavior

Modes write the handoff (and, for share-sanitize, a manifest) and present it via the available file mechanism. On filesystem surfaces (Claude Code, Cowork) files land in the working directory; on hosted surfaces the operator downloads and uploads to project knowledge. The skill does not commit, push, or transmit output anywhere; distribution is the operator's responsibility. Generated handoffs carry no SPDX header (they are the operator's work product); skill source files carry Apache 2.0 SPDX headers.

## Files in this skill

```
session-handoff/
├── SKILL.md                                  (this file: router, ## Protocol gate, surface awareness)
├── README.md                                 (full customization instructions)
├── CHANGELOG.md                              (v0.1.0 entry, v1.5 provenance, schema-vs-skill decoupling)
├── ROADMAP.md
├── USAGE.md                                  (per-mode walkthroughs incl. a plain-language share-sanitize explanation)
├── modes/
│   ├── generate.md                           (carried from v1.5, adapted to schema 0.1)
│   ├── update.md                             (current-vs-resolved curation, length projection)
│   ├── consolidate.md                        (ledger, most-restrictive governance, cap, source retention)
│   ├── retrofit.md                           (carried from v1.5; lossless schema upgrade, batch)
│   └── share-sanitize.md                     (built-in redactor, the seam, derivative identity, manifest)
├── references/
│   ├── preflight.md                          (algorithm, verdicts, tokens, routing, sanitization surfacing, post-flight)
│   ├── schema.md                             (two-zone model, two-tier metadata contract, schema_version "0.1")
│   ├── section-activation.md                 (Zone 2 narrative sections, conditional activation, ordering, writing rules)
│   ├── schema-changelog.md                   (Supported Schemas, 0.1 inception)
│   ├── lineage.md                            (supersession, consolidation identity, governance propagation)
│   ├── redaction.md                          (built-in redactor mechanics, manifest, the redaction_provider seam)
│   ├── governance.md                         (sensitivity taxonomy; anchors sanctioned-destination and share-sanitize)
│   ├── configure.md                          (the shared config-interview procedure, defined once)
│   ├── defaults.md                           (universal public defaults; skill-owned, not user-editable)
│   ├── platform-specific-parameters.md       (per-platform schema, overflow strategy, config-instantiation layout)
│   └── examples/
│       ├── example-handoff.md                (fresh generate)
│       ├── example-updated-handoff.md        (update)
│       ├── example-consolidated-handoff.md   (consolidate)
│       ├── example-sanitized-handoff.md      (share-sanitize derivative plus manifest)
│       └── example-user-config.md            (a populated user-config)
└── config/
    ├── user-config.md.template
    ├── org-config.md.template
    ├── redaction-policy.md.template
    └── platform-parameters.md                (shipped platform values)
```

## Failure modes the router handles

- **Prior handoff at a newer schema.** Refuse (`✗ Mismatch and refuse`); reveal the expected schema.
- **Frontmatter unparseable, or a required field empty.** `✗ Parse Error` with the offending field; no write.
- **Project knowledge access fails.** `✗ Infrastructure Failure`; do not assume a fresh session; surface the failure.
- **Ambiguous trigger in one invocation.** Pre-flight proposes the most specific operation; if still ambiguous, ask the operator.

All other failure modes (curation defects, governance conflicts, redaction provider unavailability, validation errors) are handled by the mode files.
