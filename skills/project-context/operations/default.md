---
file_role: skill-operation
operation: default
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operation: default

## Pre-flight prerequisite

The operations in this document apply only after pre-flight (`references/preflight.md`) has completed and operator confirmation (where required by the verdict) has been received. Operations described here assume a valid, classified project state. Do not execute these operations without pre-flight completion.

This is the default operation: triggered when the operator invokes the skill with no specific operation named. It parses the current conversation, classifies candidate records against the existing three-file system, applies the hybrid brake, surfaces gated proposals for approval, writes the updated files, and emits the operator brief.

Schema reference: `references/schema.md`. Scoring reference: `references/scoring.md`. Classifier and cross-operation logic: `references/operations.md`. Defaults: `references/defaults.md`. Configuration overrides: `config/user-config.md.template`, `config/org-config.md.template`.

## 1. Pre-flight prologue

Every operation runs the same pre-flight prologue. The detailed sequence lives in `references/operations.md`, section 4. For convenience the surface guard — the first step — is restated inline here because it is the only step that can terminate the operation immediately.

### 1.1 Surface guard (Claude Code → decline + recommend session-recap)

Before proceeding, confirm you are running on a supported surface. project-context targets AI workspaces with persistent project contexts the operator can attach files to: Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects, and similar hosted AI surfaces.

project-context is **not** designed for Claude Code. Claude Code uses filesystem-based working directories, not hosted project contexts; the `session-recap` skill is the right tool for capturing context from Claude Code sessions.

**If you detect you are running in Claude Code** — signals include: filesystem-mutation tools (e.g., `Bash`, `Write`, `Edit`) are present in your toolbox; the working directory is filesystem-based; no Project-UI affordances are visible to the operator — politely decline and recommend `session-recap`:

> This skill is designed for AI workspaces with persistent project contexts (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects). For capturing context from a Claude Code session, the `session-recap` skill is the right tool. Would you like to invoke `session-recap` instead?

Then stop. Do not proceed to the rest of pre-flight on a non-supported surface.

### 1.2 Remaining pre-flight

If the surface guard passes, hand off to the pre-flight protocol per `references/preflight.md` for the protocol-enforcement work (the search strategy and six-branch classification including UPGRADE_AVAILABLE_GENERATION for Scenario G, counter assignment per section 3.4, the generation self-consistency check per section 3.5, report block, confirmation token, the model advisory and two-tier gate per section 4.6, topology validation, stale-spoke detection). The post-classification runtime steps (project detection, conflict detection, migration trigger handling, configuration resolution) are described in `references/operations.md` section 4. Migration is initiated per `references/migration.md` whenever pre-flight classifies as `⚠ Legacy`, `⚠ Upgrade Available`, `⚠ Upgrade Available (v0.5.0 to v0.6.0)`, or `⚠ Upgrade Available (v0.6.0 to v0.7.0)`; only pure-current state at schema 0.5 with `pc-NNNN-*` names, `_managed_by`, `generation`, and a topology block skips migration. A schema-0.4 file with old canonical names and a topology block (no `pc-NNNN-*` files) triggers Scenario G, the v0.6.0 to v0.7.0 generation/naming upgrade; legacy files, schema-0.2 files, and schema-0.3-without-topology files trigger their respective migration paths.

## 2. Parse the conversation

Scan the current conversation for candidate records. The seven candidate kinds:

| Candidate kind | Routes to file | Routes to section |
|---|---|---|
| Decision | `pc-NNNN-context.md` | Decisions |
| Constraint | `pc-NNNN-context.md` | Constraints |
| Current state fact | `pc-NNNN-context.md` | Current State |
| Open item | `pc-NNNN-context.md` | Open Items |
| Terminology | `pc-NNNN-context.md` | Terminology |
| External reference | `pc-NNNN-context.md` | External References |
| Entity (person, place, thing, organization, dataset) | `pc-NNNN-entities.md` | matching sub-section |

For each candidate, extract:

- `content` — the record text, rewritten to be a self-contained unit (no pronouns referring to other records).
- `source_quote` — the verbatim conversation snippet.
- `source_ref` — the session ID or a stable label.
- `importance` — model-assigned integer 1-10 per the bands in `references/scoring.md` section 6.
- Section / file routing.

Skip candidates that are conversational scaffolding, recap, or low-signal small talk. The bar for inclusion: would a future AI session reading the active file benefit from this record? If not, do not propose it.

## 3. Classify candidates (five-op merge classifier)

For every candidate produced in step 2, run the classifier from `references/operations.md` section 2:

```
candidate = parsed_record(conversation_chunk)
neighbors = find_similar_records(candidate, top_k = 5)

if neighbors is empty:
    return ADD

best_match = neighbors[0]

if semantically_identical(candidate, best_match):
    return NOOP

if contradicts(candidate, best_match):
    return SUPERSEDE

if evolves_meaning_of(candidate, best_match):
    return UPDATE

return ADD
```

`find_similar_records` searches `pc-NNNN-context.md` for non-entity candidates and `pc-NNNN-entities.md` for entity candidates. Do NOT match against the archive during classification.

## 4. End-of-session DEMOTE pass

After all candidate classifications are collected, run a separate pass over every active record:

```
for record in active_file:
    weight = score(record, current_update)
    if weight < demotion_threshold:
        emit DEMOTE proposal
```

The `score()` function uses the formula and coefficients from `references/scoring.md` (or their `user-config.md` / `org-config.md` overrides). The default `demotion_threshold` is `5`.

## 5. Apply the hybrid brake

Under the default `merge_policy: hybrid`, partition proposals:

| Classifier output | Auto-applied? |
|---|---|
| `ADD` (no similar neighbor) | Yes |
| `NOOP` | Yes |
| `UPDATE` | No — gate |
| `DEMOTE` | No — gate |
| `SUPERSEDE` | No — gate |

Under `merge_policy: gate`: every proposal is gated.
Under `merge_policy: auto`: every proposal is auto-applied. The auto-mode warning (section 8) fires first if it hasn't fired this session.

## 6. The diff-and-approve flow

Show up to `proposal_cap_per_session` (default 10) gated proposals to the operator in a single structured block. Auto-applied changes appear in the summary marked `[auto-applied]` but do not consume a proposal slot.

### 6.1 Severity marker

Select one based on the gated proposals' content:

| Marker | When |
|---|---|
| 🟢 | Routine session, no risky changes (only NOOP / safe ADDs auto-applied; no gated UPDATE/SUPERSEDE) |
| 🟡 | Some risky changes (gated UPDATE, DEMOTE, or non-contradictory SUPERSEDE) |
| 🔴 | Contradictions detected (SUPERSEDE proposals); review carefully |

### 6.2 Proposal block template

```
🟡 **Session merge proposals.** I've reviewed our session and propose 6 updates:

  ✏️  UPDATE   #1  (importance: 8) Deadline moved from May 20 → May 25
                   (saw it twice today; existing record dec-014 first noted 2026-04-12)
  ➕  ADD      #2  (importance: 7) New stakeholder: Priya Shah (Finance lead)
  📌  KEEP     #3  Reinforce: "no PII in customer-facing prompts" (seen 3x more) [auto-applied]
  📦  DEMOTE   #4  Old budget number ($45K) — superseded by #5
  🔄  SUPERSEDE #5 (importance: 9) New budget: $52K replaces old $45K (approved by Priya 2026-05-09)
  ➕  ADD      #6  (importance: 6) New external reference: Q2 board deck

Reply with: "all" to accept, "skip 3 4" to skip those, or
"explain 2" to see the source quote.
```

### 6.3 Operation markers

| Marker | Operation |
|---|---|
| ➕ | ADD |
| ✏️ | UPDATE |
| 📌 | KEEP (NOOP / reinforce) |
| 📦 | DEMOTE |
| 🔄 | SUPERSEDE |
| ⚡ | Auto-approved (in summary view) |

**Emojis live in this chat-only output. Stored `.md` files never carry emojis** (the `[AUTO]` content prefix and the explicit `audit.approval_mode` value are the structured equivalents).

### 6.4 Approval grammar

Accepted operator responses (case-insensitive):

| Response | Meaning |
|---|---|
| `all`, `accept`, `yes` | Approve every gated proposal. |
| `skip N M ...` | Approve all except the listed proposal numbers. |
| `only N M ...` | Approve only the listed numbers; skip the rest. |
| `explain N` | Show proposal #N's `source_quote` and the closest existing record's content; then re-prompt for approval. |
| `set importance N=K` | Override the importance score for proposal #N to integer K (1-10); stamp `audit.importance_source: user-override` on the resulting record. |
| `cancel`, `abort` | Stop without writing. |

If the operator's response is ambiguous, ask for clarification. Do not guess.

## 7. Write the updated files

For each approved proposal, apply the corresponding state change to the in-memory file representation:

| Operation | State change |
|---|---|
| `ADD` | Append record to its section in `pc-NNNN-context.md` or `pc-NNNN-entities.md`. Initialize `times_seen = 1`, `first_seen_update = current_update`, `last_seen_update = current_update`, `first_seen_at = now`, `last_seen_at = now`, `status: active`, audit block per section 9. |
| `UPDATE` | Replace existing record's content. Bump `last_seen_update = current_update`, `last_seen_at = now`, increment `times_seen`. Copy the prior version to the archive with `status: superseded`, `prior_id` = the original ID, a fresh `arc-` ID, `superseded_by` = the new record's ID, `superseded_at_update = current_update`. |
| `NOOP` | On the matched record, increment `times_seen`, set `last_seen_update = current_update`, set `last_seen_at = now`. No archive write. |
| `DEMOTE` | Remove record from active. Move to archive with a fresh `arc-` ID, `prior_id` = the original ID, `status: archived`, `demoted_at_update = current_update`. |
| `SUPERSEDE` | Remove old record from active. Move old to archive with `status: superseded`, `prior_id` = the original ID, fresh `arc-` ID, `superseded_by` = the new record's ID, `superseded_at_update = current_update`. Add the new record to the active file per the `ADD` rules. |

After all changes are applied:

1. Remove the first-run placeholder block (delimiters and content) from any file that still has it, if at least one record was added to that file.
2. **Increment `update_count` by 1 on every file touched** (the scoring lifecycle counter; only files with content changes are touched). Do NOT touch `update_count` on a file with no content change. `update_count` is distinct from `generation`; see `references/schema.md`.
3. **Stamp `generation = N` on all three files**, where `N` is the counter assigned at pre-flight (`references/preflight.md` section 3.4: confirmed-empty seeds 1; populated is highest plus one). **Write all three files under `pc-000N-{context,entities,archive}.md`** so the canonical set advances together at one counter. A file with no content change is still re-stamped to generation `N` and re-written under the new name; this keeps the set coherent at a single `NNNN` and lets the set-integrity directive prune lower sets safely. `generation` and `update_count` move independently: `generation` is `N` on all three; `update_count` increments only on touched files.
4. Update `last_merged` to now on every file written.
5. Recompute `record_count` on every file.
6. Append a checkpoint object to the archive's `checkpoints` frontmatter array summarizing the session (e.g., `"3 ADDs, 1 UPDATE, 1 DEMOTE."`). If the archive had no record changes, still add the checkpoint with `summary: "No archive changes."` for traceability.
7. Run the validation checklist from `references/schema.md` section 6 on every file written (including the generation self-consistency check: the `NNNN` in each filename equals its frontmatter `generation`). If any check fails, halt and report.

## 8. Auto-mode

If `merge_policy: auto` is in effect (either from `user-config.md`, `org-config.md`, or operator chat command), fire the published auto-mode warning before classifying proposals. The warning fires once per session.

### 8.1 Warning text (verbatim — must not be edited)

```
⚠️  Auto-mode is about to be enabled.

Records added in auto-mode skip your approval gate. This trades data
integrity for speed and may cause cascading quality issues over time as
auto-approved records influence future merges.

Your name will be attached to every auto-approved record. This is an
audit feature, not a blame feature — if data quality degrades later, the
audit trail helps diagnose and coach, not assign fault.

Proceed with auto-mode for this session?
```

### 8.2 Response handling

| Operator response | Effect | `audit.warning_response` stamp |
|---|---|---|
| Explicit acknowledgment ("yes", "proceed", "go ahead") | Auto-mode active for the session. | `acknowledged` |
| Explicit rejection ("no", "cancel", "use hybrid") | Auto-mode cancelled. Fall back to `hybrid` for the rest of the session. | n/a |
| Passive (unclear, off-topic, silent) | Auto-mode proceeds (per workshop decision). | `passive` |
| Explicit dismissal ("whatever", "fine") | Auto-mode proceeds. | `dismissed` |

Activation scope is per-session. The warning fires again on the next session if auto-mode is still configured. Persistent across-session activation is not supported.

Every record added under auto-mode carries:

- `content` prefixed with the literal `[AUTO]` token.
- `audit.approval_mode: auto`.
- `audit.approved_by`: the user's `user_identifier` from `user-config.md`, or `null` if unset.
- `audit.warning_response`: per the table above.

## 9. The operator brief

After successful write, emit a structured brief in the chat. Emojis are allowed in the brief (chat-only). Template:

```
✅ **Session complete. Here is what to do next.**

📥 **Download** the current generation's files from this chat (generation 4):
   • pc-0004-context.md  (updated — 3 ADDs, 1 UPDATE, 1 DEMOTE)
   • pc-0004-archive.md  (updated — 2 records archived this session)
   ℹ pc-0004-entities.md — content unchanged this session, but re-stamped to
     generation 4; download and upload it too so the set stays at one counter.

📂 **Upload** the pc-0004-* set to your Project, then follow the set-integrity
   directive rendered in the post-flight summary above (canonical wording in
   references/preflight.md section 9.6).
   In Claude.ai: Project → Knowledge → Upload file.

🔔 **Heads up**: a future Anthropic API update may automate this upload
   step. Until then, manual upload is the dominant friction in the
   workflow. Tracking on the project roadmap.
```

The set-integrity directive is owned canonically by `references/preflight.md` section 9.6 and rendered by the post-flight summary; this brief does not restate the replace wording, it points at it.

Brief fields adapt to session content:

- List all three files of the current generation. Annotate files with content changes; mark a content-unchanged file with the `ℹ` indicator, noting it is still re-stamped to the new generation and must be uploaded so the set stays at one counter.
- Append `downstream_chaining` instructions from `org-config.md` after the cleanup section if any apply (`after_default`, `after_any`).
- Include token-budget reminder if `pc-NNNN-context.md` is above `soft_warning` (default 50K).
- Include auto-mode audit summary if `merge_policy: auto` was used this session and `brief.include_audit_summary` is true.

## 10. Failure handling

| Failure | Handling |
|---|---|
| Surface guard fires | Decline immediately, recommend session-recap. Do not write files. |
| Project container missing | Warn, ask before proceeding. |
| Legacy v0.1.x files found | Route to migration per `references/migration.md`. |
| `find_similar_records` is uncertain (multiple candidate neighbors with similar scores) | Surface the ambiguity in the proposal block; let operator pick. |
| Validation fails on a generated file | Halt; report the validation error; do not present files to operator. |
| Operator cancels mid-flow | Stop. Do not write. Do not emit a brief beyond a one-line confirmation. |

## 11. Cross-references

- Schema: `references/schema.md`.
- Scoring: `references/scoring.md`.
- Common operation logic and classifier: `references/operations.md`.
- Defaults: `references/defaults.md`.
- Migration: `references/migration.md`.
- Configuration: `config/user-config.md.template`, `config/org-config.md.template`.
- Other operations: `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`.
