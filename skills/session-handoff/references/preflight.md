---
file_role: skill-reference
topic: preflight
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Pre-flight and post-flight (session-handoff v0.1.0)

This file is the authoritative specification for the pre-flight protocol, the auto-routing table, the verdict set, the confirmation-token catalog, the sanitization surfacing, surface awareness, and the symmetric post-flight summary. SKILL.md's `## Protocol` section structurally gates every mode on the completion of pre-flight as defined here. Mode files (`modes/*.md`) cite this file in their pre-flight prerequisite notes.

Pre-flight is the dominant operation (search, classify, surface, propose, await confirmation). Post-flight is the symmetric closing block (report what was actually written). Both live here for protocol cohesion: they share a verdict-glyph convention, a structured-fields convention, and a "skippability is a protocol violation" rule.

## 1. The first principle

**The existing handoff state is authoritative. The executing skill is not.**

When the skill is invoked, it validates against the existing handoff state before performing any operation. If a prior handoff declares a schema newer than the executing skill writes, the skill surfaces the mismatch and refuses to proceed until the operator resolves it. The skill never assumes correctness on the basis of being the running instance.

This mirrors the benchmark's protocol-enforcement posture. Pre-flight is a structural gate: SKILL.md's `## Protocol` section is the first content after frontmatter, the model cannot reach mode content without passing through it, and the model must emit a pre-flight report block as the first content of every response before any generation. The `_managed_by: session-handoff-skill` marker makes detection reliable.

## 2. Pre-flight algorithm

Pre-flight is a search strategy followed by classification, auto-routing, sanitization surfacing, and a token gate.

### 2.1 Search strategy

Sequential; each tier runs only if the prior returned nothing relevant. Relevance means a result chunk that includes actual frontmatter signals (not merely a filename reference or a spec describing the schema).

1. **Primary:** search project knowledge for `_managed_by: session-handoff-skill` AND `schema_version: "0.1"`.
   - Purpose: find handoffs under skill management at the current schema.
   - Hit signal: chunks with actual frontmatter carrying `_managed_by: session-handoff-skill` AND `schema_version: "0.1"`.
2. **Secondary (if primary returns nothing relevant):** search for `_managed_by: session-handoff-skill` (any schema).
   - Purpose: find handoffs at a different schema version that may need retrofit.
   - Hit signal: chunks with `_managed_by: session-handoff-skill` and a `schema_version` other than `"0.1"`.
3. **Tertiary (if both return nothing relevant):** search for legacy patterns the operator names (a folder of older-schema handoffs handed to retrofit; older recap-era files identified by the operator).
   - Purpose: support the batch-retrofit files-only case, which is distinct I/O (N files, no live conversation).
4. **If all tiers return nothing relevant:** classify as a fresh session.

Config files are detected by a parallel search for `_managed_by: session-handoff-skill` with the matching `config_type` (`references/configure.md` section 5).

### 2.2 Classification and verdict

From the returned chunks, parse YAML frontmatter where present, disregard chunks that merely reference handoffs (recaps quoting frontmatter, specs describing the schema), and classify:

| Detected state | Verdict | Routes to |
|---|---|---|
| No prior handoff, fresh session | `✓ Fresh` | generate (auto-proceeds) |
| Current-schema handoff plus new conversation | `✓ Update target found` | update (`confirm update`) |
| Stale-schema handoff, no new content in scope | `⚠ Retrofit needed` | retrofit, schema-only (auto-proceeds or `confirm retrofit` per config) |
| Stale-schema handoff plus new conversation | `⚠ Retrofit needed` | retrofit then update (`confirm update`) |
| N prior handoffs selected | `⚠ Consolidation set` | consolidate (`confirm consolidate`) |
| Batch of stale-schema files | `⚠ Retrofit needed` | batch retrofit (`confirm retrofit`) |
| Sharing or sensitive content signaled | `⚠ Share-sanitize decision` | share-sanitize (`confirm sanitize`) |
| Prior handoff at a schema newer than the skill | `✗ Mismatch and refuse` | refuse; reveal expected schema |
| Frontmatter present but unparseable | `✗ Parse Error` | refuse; name the offending field |
| Search errored or returned nothing parseable | `✗ Infrastructure Failure` | refuse; surface the failure |

### 2.3 The six runtime steps

1. Run the search strategy (2.1) and classify (2.2).
2. Run `handoff_id` collision detection for the generate and update paths: if a same-topic same-date handoff exists, the `s<NN>` sequence increments on detection (`references/schema.md` section 3).
3. Auto-route per the routing table and propose the operation with a verdict.
4. Always emit the locked sanitization-surfacing line (section 5), and fire the blocking sanitize question if the `sanitization_prompt` gate condition is met.
5. Note config auto-creation for any config file confirmed absent (section 6).
6. Require the appropriate confirmation token before any destructive write (section 4). Auto-proceed only on `✓ Fresh` (and on `⚠ Retrofit needed` schema-only when config sets retrofit to auto-proceed).

The model ends its turn after emitting the report (except where the verdict auto-proceeds). It does not generate output, modify state, or propose files between report emission and token receipt.

## 3. Pre-flight report block format

| Element | Choice |
|---|---|
| Format | Rendered markdown, NOT wrapped in a code block |
| Heading | `## Pre-flight Report` followed by the verdict on the same line |
| Verdict glyphs | Unicode `✓` `⚠` `✗` (not emojis); core Unicode, render reliably across surfaces |
| Placement | FIRST content emitted in the response; no preamble |
| Skippability | NEVER. Block absence is a protocol violation, not an optimization. |

### 3.1 Required fields

| Field | Purpose |
|---|---|
| Verdict (in header) | The operator's eye lands here first |
| Prior handoff(s) | Files found: `handoff_id`, `handoff_version`, schema, generation_mode, date; or "none" |
| Executing skill | The skill version running, with a compatibility note |
| Surface | The detected surface and its model-identity provenance note (section 7) |
| Proposing | The operation pre-flight selected, and the content behavior (new / curated / preserved / derivative) |
| Sanitization | The locked surfacing line (always), and the blocking question if the gate fired |
| To proceed | The confirmation token, or "Auto-proceeding" |

For `✗` verdicts, `Proposing` is replaced with `Issue` (diagnostic) and `Resolution options` (numbered operator paths).

### 3.2 Report examples

**Fresh (generate, auto-proceeds):**

```
## Pre-flight Report ✓ Fresh

**Prior handoffs:** none detected.
**Executing skill:** session-handoff v0.1.0 (schema 0.1).
**Surface:** Claude Code (high model-identity provenance).
**Proposing:** generate a new handoff at schema 0.1 (new identity, handoff_version 1).

**Sanitization:** Sanitization is available. If this handoff will be shared with
another person, run share-sanitize to produce a redacted copy and a manifest of what
was removed. Say "sanitize this for sharing" to invoke it.

**Configuration:** config/user-config.md, config/org-config.md, config/redaction-policy.md
auto-created with placeholder defaults; populate to enable full personalization.

**To proceed:** auto-proceeding (fresh session, no destructive write).
```

**Update target found:**

```
## Pre-flight Report ✓ Update target found

**Prior handoff:** HND-auth-rewrite-20260530-s01 v2 (schema 0.1, generation_mode live,
  2026-05-30).
**Executing skill:** session-handoff v0.1.0 (schema 0.1, compatible).
**Surface:** Claude Code (high model-identity provenance).
**Proposing:** update. Preserve handoff_id, increment to handoff_version 3, set
  supersedes to HND-auth-rewrite-20260530-s01#v2. Live items carry at full fidelity;
  items resolved since v2 compress to ledger lines. Projected length within the
  per-version budget.

**Sanitization:** [locked surfacing line emitted verbatim]

**To proceed:** type `confirm update`
```

**Consolidation set (with mixed sensitivity and a protected source):**

```
## Pre-flight Report ⚠ Consolidation set

**Sources (3):**
- HND-pricing-20260520-s01 v1 (confidential, retention review_by 2026-09-01)
- HND-pricing-20260524-s01 v1 (internal)
- HND-pricing-20260528-s02 v1 (internal, framework: SOX)
**Executing skill:** session-handoff v0.1.0.
**Surface:** Claude Code.
**Proposing:** consolidate into a new identity. Derived governance (most-restrictive):
  sensitivity confidential, retention review_by 2026-09-01, frameworks [SOX].
  consolidation_depth 1. Sources retained by default.
**Cap:** 3 sources, at the soft max_sources of 3.

**Sanitization:** [locked surfacing line emitted verbatim]

**To proceed:** type `confirm consolidate`
  (Deleting any source would require `confirm delete protected sources`, because one
  source is confidential and one carries a framework. Sources are kept unless you ask.)
```

**Mismatch and refuse:**

```
## Pre-flight Report ✗ Mismatch and refuse

**Prior handoff:** HND-roadmap-20260601-s01 v1 (schema 0.2).
**Executing skill:** session-handoff v0.1.0 (writes schema 0.1).
**Issue:** the prior handoff is at a schema newer than this skill writes. Proceeding
  would risk corrupting a newer-schema handoff.

**Resolution options:**
1. Upgrade your local skill copy to the version that writes schema 0.2 (recommended).
2. Open the file to confirm its schema is genuine and not a malformed literal.
```

## 4. Confirmation token catalog

### 4.1 Tokens by route

| Route | Token | Why it gates |
|---|---|---|
| generate (fresh) | none, auto-proceeds | no prior state to overwrite |
| update | `confirm update` | update supersedes a prior version (destructive to the "latest" pointer) |
| retrofit (schema-only) | auto-proceeds, or `confirm retrofit` per config | content is preserved verbatim; low risk |
| batch retrofit | `confirm retrofit` | N files written at once |
| consolidate | `confirm consolidate` | a new artifact gathers several sources |
| consolidate over cap (soft mode) | `confirm over-cap` | N exceeds `max_sources` and review fidelity is at risk |
| delete sources after consolidate (protected) | `confirm delete protected sources` | a source is confidential, restricted, or framework-bearing |
| share-sanitize | `confirm sanitize` | redaction is a decision with sharing consequences |

`cap_mode: hard` refuses above `max_sources` instead of offering `confirm over-cap`.

### 4.2 Token matching rules

| Rule | Detail |
|---|---|
| Case | Case-insensitive: `confirm update`, `Confirm Update`, `CONFIRM UPDATE` all match. |
| Whitespace | Tolerant: leading, trailing, and intra-token extra whitespace normalized. |
| Fuzzy matching | NONE. Strict equality after case-folding and whitespace normalization. Typos do not match. |
| Timeout | NONE. The operator can take any amount of time. Conversation-scoped state. |

Token mismatch error format:

```
Token mismatch. Expected `confirm update`. Received `confirm updaet`.
Please retry with the exact token.
```

The error reveals the expected token so the operator can copy-paste.

### 4.3 Model behavior between report and token

After emitting the report, the model ends its turn. The next operator message is either the matching token (proceed, then post-flight), a non-matching token (emit the mismatch error, end turn, wait again), or something else entirely (treat as context change; re-run pre-flight if appropriate). The model takes no action and writes nothing between report emission and token receipt.

## 5. Sanitization surfacing (locked) and the gate

Pre-flight handles sanitization in two layers.

| Layer | Behavior | Configurable |
|---|---|---|
| Surfacing | always emits a locked, plain-language line stating sanitization is available and how to invoke it | no, always on |
| Gate | the blocking sanitize question fires only when sharing is signaled or sensitive content (including flagged PII) is detected | yes: `sanitization_prompt: always \| on-signal \| never` |

LOCKED TEXT, emitted verbatim in every pre-flight report, regardless of `sanitization_prompt`:

```
Sanitization is available. If this handoff will be shared with another person, run
share-sanitize to produce a redacted copy and a manifest of what was removed. Say
"sanitize this for sharing" to invoke it.
```

The gate (`references/defaults.md` section 1): `on-signal` (public default) fires the blocking sanitize question when sharing is signaled or sensitive content (including flagged PII) is detected. `always` (set by an enterprise org-config) fires it on every invocation. `never` suppresses the blocking question; the surfacing line still emits.

When the gate fires, the report adds a blocking question: "This handoff appears headed for sharing or contains flagged sensitive content. Run share-sanitize first? Reply `confirm sanitize` to produce a redacted copy, or tell me to proceed without sanitizing."

## 6. Config auto-creation in pre-flight

For each config file the skill expects (`config/user-config.md`, `config/org-config.md`, `config/redaction-policy.md`), pre-flight searches project knowledge; if a file is confirmed absent, it instantiates the config by extracting the fenced rendered block from the matching `.template` (the content between the fence delimiters, not the template's SPDX header or prose) and writing it with placeholder defaults, then notes the creation in the report. The exact extraction mechanism is defined in `references/configure.md` section 5. On flat surfaces the file lands with a `config-` name prefix (`references/platform-specific-parameters.md` section 3). Never blind-write; auto-create only when confirmed absent.

## 7. Surface awareness, never decline

session-handoff is the cross-surface tool and never declines a surface. It keeps awareness that Claude Code and Cowork yield higher model-identity provenance (the skill can read its execution environment, so `generated_by.surface` and `generated_by.model` are reliable and `model_source` is `system-reported`), and notes it in the report, but does not refuse. On hosted chat surfaces, model identity may be `operator-stated`; the skill records that and proceeds. This inverts the project-context surface guard, which is deliberately not adopted.

## 8. Pre-flight completion criteria

Pre-flight is complete when ALL hold:

1. The search strategy has run for the `_managed_by` marker at the current schema and, as needed, any schema and legacy patterns.
2. The pre-flight report block has been emitted as the FIRST content of the response.
3. The locked sanitization-surfacing line has been emitted.
4. Where the verdict requires it, the operator confirmation token has been received and exact-matched.

If any criterion is missing, generation must not proceed.

Anti-rationalization clause: operator urgency, perceived skill execution context, or any other condition does not license skipping pre-flight. If project-knowledge access fails and pre-flight cannot complete, refuse to proceed and surface the failure (`✗ Infrastructure Failure`). Do not assume a fresh session on infrastructure failure; the project may have state the search could not see.

## 9. Post-flight summary

Pre-flight is "here is what I am about to do." Post-flight is "here is what I actually did." The symmetry closes the audit loop.

### 9.1 Rendering rules

| Element | Choice |
|---|---|
| Heading | `## Post-flight Summary` followed by verdict |
| Verdict glyphs | `✓ Complete`, `✗ Failed`, `⚠ Partial` |
| Placement | LAST structured content, after the write completes |
| Skippability | NEVER. Failure cases still produce a post-flight summary with `✗` and a diagnostic. |

### 9.2 Required fields

| Field | Purpose |
|---|---|
| Verdict (in header) | Outcome at a glance |
| Handoff written | `handoff_id`, `handoff_version`, filename, schema |
| Lineage effect | What was superseded, consolidated (with the flattened source lineage captured into the audit record), or marked derivative |
| Mode performed | The mode that actually ran; flag any divergence from the pre-flight proposal |
| Curation report (update) | What was carried at full fidelity, what was compressed to ledger lines |
| Manifest summary (share-sanitize) | Categories and counts, the assistive disclaimer, the flagged-not-redacted count |
| Operator action required | Any follow-up (e.g. sources to delete after verifying the consolidated handoff) |

### 9.3 Deviation reporting

If the mode performed differs from the mode pre-flight proposed (rare; possible if execution finds something pre-flight missed, e.g. a stale-schema prior that forces a composed retrofit), the post-flight summary states it explicitly. Silent deviation is a protocol violation.

### 9.4 Failure handling

If a write fails, post-flight still emits with `✗ Failed`, names what succeeded and what failed, and gives the operator a recovery path. On consolidate, the flattened source lineage captured into the audit record at consolidation time means a partial failure does not lose provenance.

## 10. Cross-references

- The `## Protocol` structural gate that cites this file: `SKILL.md`.
- Metadata contract, `handoff_id` derivation, no-empty-fields Parse Error: `references/schema.md`.
- Supported Schemas matrix that drives the mismatch verdict: `references/schema-changelog.md`.
- Lineage, consolidation identity, governance propagation, source-retention gating: `references/lineage.md`.
- Sanitization gate, length contract, consolidate cap defaults: `references/defaults.md`.
- Redaction policy and the share-sanitize flow: `references/redaction.md`, `modes/share-sanitize.md`.
- Surface and config-instantiation parameters: `references/platform-specific-parameters.md`, `config/platform-parameters.md`.
- Mode files that cite this pre-flight: `modes/generate.md`, `modes/update.md`, `modes/consolidate.md`, `modes/retrofit.md`, `modes/share-sanitize.md`.
