---
file_role: skill-reference
topic: operations
schema_version_documented: "0.4"
skill_version: "0.6.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Operations (project-context v0.6.0)

This file documents the **logic** of the four operations and the merge classifier they share. The actual operation entry points live in `operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`. SKILL.md routes invocation to one of those four files. This file is the cross-operation reference each of those files cites.

## 1. The four operations at a glance

| Operation | Default? | Triggered by | Primary job |
|---|---|---|---|
| `default` | yes | Any skill invocation with no specific operation named. | Parse the current conversation, classify candidates, propose merges, write updated files. |
| `merge_external` | no | Operator attaches a file or names a session-recap / vision / spec document as the input source. | Parse the file (not the conversation), classify, propose merges. |
| `compact` | no | Operator says "compact", "compact this", "trim the project context", "consolidate". | Score all active records, propose batch DEMOTE for those below threshold. |
| `rebuild` | no | Operator says "rebuild", "reset from archive", "regenerate project context". | Rebuild the active file from the archive using current scoring. Mandatory pre-commit review. |

Each operation has its own pre-flight prologue. The common pre-flight pieces are listed in section 4 below; per-operation specifics live in each operation file.

## 2. The five-operation merge classifier

The merge classifier takes a parsed candidate record plus the current state of the three-file system and emits exactly one of five operations.

| Operation | Semantic | Effect on active file | Effect on archive |
|---|---|---|---|
| `ADD` | Novel record; no existing record similar enough to match. | Append. | None. |
| `UPDATE` | Existing record's content evolves; spirit preserved. | Revise in place; preserve prior version. | Prior version copied with `status: superseded`, same `prior_id`. |
| `NOOP` | Duplicate or reinforcement. | Increment `times_seen`, update `last_seen_update`. | None. |
| `DEMOTE` | Existing record still true but no longer meets active threshold. | Remove from active. | Add with `status: archived`, `demoted_at_update` set. |
| `SUPERSEDE` | Existing record contradicted by new content. | Remove old, add new. | Old copied with `status: superseded`, `superseded_by` set, `superseded_at_update` set. |

### 2.1 Classifier pseudocode (per candidate)

```
candidate = parsed_record(input_chunk)
neighbors = find_similar_records(candidate, top_k = 5)

if neighbors is empty:
    return ADD

best_match = neighbors[0]

if semantically_identical(candidate, best_match):
    return NOOP

if contradicts(candidate, best_match):
    return SUPERSEDE   # archive best_match, add candidate

if evolves_meaning_of(candidate, best_match):
    return UPDATE      # revise best_match, archive prior version

return ADD             # default for ambiguous cases
```

`DEMOTE` is **not** emitted by the candidate-side classifier. It is emitted by a separate end-of-session consolidation pass:

```
for record in active_file:
    if weight(record) < demotion_threshold:
        emit DEMOTE proposal for record
```

See `references/scoring.md` for the `weight()` formula.

### 2.2 Similarity-search guidance

`find_similar_records` is implemented in-model. The model should:

- Match on semantic content first, then on entity overlap, then on section.
- Prefer narrow matches over broad ones (the classifier's job is to discriminate, not to coalesce loosely related records).
- Search across `project-context.md` only for non-entity candidates, and `entities.md` only for entity candidates.
- Never match against archive records during classification (archive is read-only history).

### 2.3 Wellhead taxonomy mapping

For operators who come from the operator's prior wellhead skill, the v0.6.0 classifier (unchanged from v0.4.0) maps to their five-class taxonomy:

| Wellhead class | v0.6.0 operation |
|---|---|
| novel | `ADD` |
| duplicate | `NOOP` |
| reinforcement | `NOOP` + `times_seen` increment |
| contradiction | `SUPERSEDE` |
| evolution | `UPDATE` |
| deprioritized (operator extension) | `DEMOTE` |

## 3. The hybrid brake

The default `merge_policy` is `hybrid`. Each classifier output is either auto-applied or gated:

| Classifier output | Auto-applied under `hybrid`? |
|---|---|
| `ADD` of a record with no similar neighbors | Yes |
| `NOOP` (duplicate, reinforcement) | Yes |
| `UPDATE` | No — gate for approval |
| `DEMOTE` | No — gate for approval |
| `SUPERSEDE` | No — gate for approval |

Under `merge_policy: gate`, every output is gated. Under `merge_policy: auto`, every output is auto-applied (the auto-mode warning fires first; see `operations/default.md` Auto-mode section). The brake is not user-tunable beyond the three policy values.

## 4. Common pre-flight prologue

**Pre-flight pointer (current as of v0.6.0).** The authoritative pre-flight protocol (the four-tier search strategy, the six-step classification, the report block format including v0.6.0's topology validation, stale-spoke detection, and audit trigger handler, the confirmation token catalog including `confirm v0.6.0 upgrade` for Scenario F, the token matching rules, the completion criteria, the infrastructure-failure handling, and the symmetric post-flight summary) lives in `references/preflight.md`. SKILL.md's `## Protocol` section structurally gates every operation on the completion of that protocol. This section describes the post-pre-flight runtime steps each operation performs once pre-flight has classified the project state — it is not a complete pre-flight specification.

Every operation begins with a pre-flight check. The runtime sequence operation files consume:

1. **Surface guard.** Detect whether the skill is running on Claude Code. If so, decline and recommend `session-recap`. The detection signals: filesystem-mutation tools present (`Bash`, `Write`, `Edit`, etc.), filesystem-based working directory, no Project-UI affordances visible. The decline message:

   > This skill is designed for AI workspaces with persistent project contexts (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects). For capturing context from a Claude Code session, the `session-recap` skill is the right tool. Would you like to invoke `session-recap` instead?

   The surface guard runs upstream of the schema-protocol gate. It is restated inline in each operation file because it can terminate the operation immediately.

2. **Project detection.** Identify the project container. If the conversation is not in a Project, ask the operator before proceeding (the output has no natural home as a project file).

3. **File discovery and schema verification.** Defer to `references/preflight.md` for the four-tier search strategy and the five-branch classification (CURRENT, UPGRADE_AVAILABLE, UPGRADE_AVAILABLE_TOPOLOGY, LEGACY, UNKNOWN per `references/migration.md` section 1). The classification's resulting state snapshot is the input to steps 5–7 below.

4. *(Reserved — see step 3.)*

5. **Conflict detection.** If multiple files claim the same `file_role`, prompt the operator to identify the canonical one.

6. **Migration trigger.** If pre-flight classified the project state as `⚠ Legacy`, `⚠ Upgrade Available`, or `⚠ Upgrade Available (v0.5.0 to v0.6.0)`, initiate the corresponding migration flow per `references/migration.md` (legacy migration in sections 3–8; v0.4.0-to-v0.5.0 upgrade in section 9; v0.5.0-to-v0.6.0 topology upgrade in section 10). Follow the corresponding migration brief's file-management ordering as the review gate — legacy uses `download → verify → delete old → upload new` (section 4); both upgrade paths use `download → upload (replace)` with no deletion step (section 9.5 for Scenario E, section 10.5 for Scenario F). Pre-flight does not add a separate coexistence prompt. Only the pure-current state (canonical v0.6.0 files present at schema "0.4" with `_managed_by` and topology block, no legacy or schema-0.2 or schema-0.3-without-topology files) skips migration.

7. **Configuration resolution.** Load `user-config.md` and `org-config.md` if present. Apply layered resolution per `references/defaults.md` to determine effective settings.

Pre-flight produces a state snapshot that the operation body consumes.

## 5. Per-operation logic summary

The detail for each operation lives in its own file. This is a quick summary of how each one composes the pieces above.

### 5.1 `default`

1. Run common pre-flight.
2. Parse the **conversation** for candidate records (decisions, constraints, current state, open items, entities, terminology, external references).
3. For each candidate, run the merge classifier (section 2). Collect the proposals.
4. Run the end-of-session DEMOTE pass: for each active record, compute weight; if below threshold, emit DEMOTE proposal.
5. Apply the hybrid brake (section 3). Auto-apply non-gated proposals; collect gated proposals.
6. Present gated proposals to the operator via the diff-and-approve flow (see `operations/default.md`). Honor `proposal_cap_per_session`.
7. After approval, write the updated three-file system. Increment `update_count`, update `last_merged`, append a checkpoint to the archive's `checkpoints` array if any record changed.
8. Emit the operator brief.

### 5.2 `merge_external`

Identical to `default` except step 2: parse the **attached file** instead of the conversation. Source quotes in proposals reference the file (filename plus line range or section header) rather than the conversation. If the file is a recognized structured artifact (e.g., session-recap output), apply structure-specific extraction.

### 5.3 `compact`

1. Run common pre-flight.
2. Compute weight for every active record (`references/scoring.md`).
3. Identify all records with `weight < demotion_threshold` (default 5).
4. Emit a DEMOTE proposal for each, in one batch. The proposal cap may be temporarily raised because the operator explicitly asked for batch demotion.
5. Operator reviews. Approved DEMOTEs move to the archive with `status: archived`.
6. Emit the operator brief noting post-compact file size and demoted record count.

`compact` does not parse the conversation. It operates purely on the existing active file.

### 5.4 `rebuild`

1. Run common pre-flight, plus require an existing `project-context-archive.md` (if archive is empty, halt with explanation).
2. Read all archive records.
3. Score every archive record with the current scoring algorithm.
4. Determine which records belong in the new active file (`weight >= demotion_threshold`) and which stay in the archive.
5. Construct a candidate new `project-context.md` from the qualifying archive records.
6. **Show the rebuilt file to the operator BEFORE committing.** This is the only operation where review-before-commit is mandatory regardless of `merge_policy`. Auto-mode does not bypass this gate.
7. On approval, replace the active file with the rebuilt one. Update `last_merged`, increment `update_count`, append a checkpoint.
8. Emit the operator brief noting the rebuild and which records were promoted.

## 6. Failure modes the operations handle

| Failure mode | Handled by |
|---|---|
| Skill running on Claude Code | Surface guard (decline + recommend session-recap). |
| Not in a Project container | Pre-flight warning + ask before proceeding. |
| Legacy v0.1.x-v0.3.x files detected | Migration flow (`references/migration.md`). |
| Schema version conflict (e.g., one file at v0.2, another at v0.1-era) | Operator picks canonical; non-canonical is left alone. |
| Both generate and consolidate trigger phrases in one invocation | Pre-flight asks the operator to disambiguate (legacy phrases route per the routing rules in SKILL.md). |
| Empty archive on `rebuild` | Halt; explain. |
| `project-context.md` corrupted | Operator can invoke `rebuild` to regenerate from the archive. |
| User does not respond to auto-mode warning | Per design spec section 12.3: passive = proceed with auto-mode, `warning_response: passive`. |

## 7. Cross-references

- Schema: `references/schema.md`.
- Scoring: `references/scoring.md`.
- Defaults: `references/defaults.md`.
- Migration: `references/migration.md`.
- User-tunable overrides: `references/user-config.md.template`.
- Per-operation entry points: `operations/default.md`, `operations/merge_external.md`, `operations/compact.md`, `operations/rebuild.md`.
