---
file_role: skill-reference
topic: section-activation
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Section activation rules (session-handoff v0.1.0)

This file defines which Zone 2 (markdown body) narrative sections a handoff includes, the order they appear in, and the writing rules for all of them. The Zone 1 tier-1 metadata contract (`references/schema.md` section 1) is always fully populated, and the tier-2 payload blocks (`references/schema.md` section 2.1) follow their own activation notes. These rules govern only the Zone 2 narrative.

The two-zone model is carried from the predecessor skill (v1.5): Zone 1 is structured machine-parseable YAML, Zone 2 is dense narrative prose that expands on Zone 1. Anything an agent can programmatically extract or verify belongs in Zone 1; anything that needs natural-language understanding belongs in Zone 2.

`modes/generate.md` produces these sections at capture time. `modes/update.md` and `modes/consolidate.md` regenerate them. `modes/retrofit.md` preserves them verbatim (it does not rewrite narrative).

## 1. Always-include sections

These appear in every handoff regardless of `thread_type`.

### Project Background

Zero-context briefing for a cold-start agent: what the project is, who owns it, why it exists, what stage it is in. Written as if the reader has never heard of the project. Three to eight dense sentences. Expands on the `project` payload block.

### Session Summary

What happened in this session. Not a transcript: a compressed account of work performed, inputs processed, outputs generated, and decisions made. Reference deliverables by exact filename. Three to ten sentences by complexity.

### Current State

Where things stand right now. Facts, not interpretation. When the payload has a `state_snapshot`, this section is the narrative wrapper explaining what those numbers mean in context.

### Decisions and Rationale

Expands on the `decisions` payload block. Each decision gets one to three sentences of reasoning that does not fit cleanly in a YAML string. If the payload captures the rationale adequately, this section may be brief and point to the `decisions` block.

### Open Items in Context

Expands on the `open_items` payload block: why each item is unresolved, what was tried, what evidence exists, the recommended path.

### Receiving-agent handling block

The sensitivity-aware standing instruction to the destination agent on how to treat this handoff. Wording per `governance.sensitivity` is specified in `references/governance.md` section 3.2. Always present (this is a session-handoff addition beyond the v1.5 set).

### Continuation Briefing

Addressed directly to the reading agent. Expands on the `continuation` payload block: what to do first, what to watch for, what the operator expects, what not to touch. Operational instructions, not suggestions.

### Staleness Warning

Always included. States that the handoff reflects artifact state as of `state_captured_at`, that the operator may modify deliverables between sessions, and that the agent should diff the actual files against this handoff (and against the `state_snapshot` metrics) before making changes.

## 2. Conditional sections

Include based on `thread_type` and session content.

### Technical Context

Include when `thread_type` is `build` OR any code, architecture, infrastructure, schemas, formulas, configs, or toolchain decisions were discussed. Contains: architecture decisions and reasoning, schema-design rationale beyond what the `schemas` block captures, formula logic, cross-system dependencies, build-approach rationale, environment constraints, integration patterns. Does not contain raw code dumps or full formula strings (those go in the `schemas` payload block).

### Source Ingestion Context

Include when `thread_type` is `research` OR any data source was processed, analyzed, or discussed this session (CSV import, PDF analysis, screenshot data entry, API export, statement reconciliation, dataset review, or any workflow that turned raw data into structured information). Contains the per-source narrative: what the source was, what was found, what matched existing data, what was new, what was excluded, what judgment calls were made, what ambiguities remain. This is the audit trail explaining why the `source_ingestion` and `artifacts.references` payload entries say what they say.

Scope note: this section is an operator-approved scope addition in v0.1.0. The locked design spec enumerated the payload block set without it; it is carried forward from the predecessor skill and gated to the `research` thread type and the data-processing content signal. A design-spec delta documenting the addition accompanies this build for the Hub to ratify.

### Strategic Context

Include when `thread_type` is `strategic` OR decision frameworks, option analysis, execution planning, or business strategy were discussed. Contains: strategic objectives, options considered and why each was chosen or rejected, execution timeline and phasing, contingency plans, constraints that shaped strategy, principles that influenced decisions.

### Guardrails and Watchpoints

Include when there are active patterns to monitor, acknowledged blind spots, boundaries the reading agent should maintain, or anti-patterns to avoid. Contains specific behavioral instructions for the reading agent: things to watch for, things to avoid, commitments to help enforce. Skip when no active guardrails are relevant.

### Workflow and Process Notes

Include when the session established or refined a workflow pattern future sessions should follow (an iterative build-then-diff process, a data-ingestion protocol, a review-and-approve cycle). Contains the workflow steps in order, what triggers each, the operator versus agent role at each step, and the expected inputs and outputs.

## 3. Section ordering

Sections appear in this order when included:

1. Project Background (always)
2. Session Summary (always)
3. Current State (always)
4. Technical Context (conditional)
5. Source Ingestion Context (conditional)
6. Strategic Context (conditional)
7. Decisions and Rationale (always)
8. Open Items in Context (always)
9. Guardrails and Watchpoints (conditional)
10. Workflow and Process Notes (conditional)
11. Receiving-agent handling block (always)
12. Continuation Briefing (always)
13. Staleness Warning (always)

`mixed` thread type: include every conditional section whose content signal is present, in the order above.

## 4. Writing rules for all sections

1. Third-person observer voice, addressed to the reading agent.
2. No em dashes anywhere. Use commas, periods, parentheses, or restructure.
3. No bold, italic, or emphasis formatting in prose. Headers only mark section breaks.
4. No bullet points in prose. Use numbered lists only when order matters (continuation steps). Otherwise write in sentences.
5. No tables in the narrative body. Structured data belongs in Zone 1 YAML.
6. No filler: "it is worth noting", "as mentioned", "interestingly", "it should be noted" are banned.
7. Every sentence carries information. If removing a sentence loses nothing, remove it.
8. Prefer specifics over generalizations: "62 expense items across 22 categories", not "many items across multiple categories".
9. Reference deliverables by exact filename every time.
10. Reference Zone 1 payload blocks by name when the prose expands on structured data, e.g. "see the `schemas` block for exact column definitions".

## 5. Cross-references

- The two-zone model and the tier-2 payload block set: `references/schema.md` section 2.
- The canonical field-by-field payload schema: `modes/generate.md`.
- The receiving-agent handling block wording per sensitivity: `references/governance.md` section 3.2.
- Retrofit preserves narrative verbatim: `modes/retrofit.md`.
