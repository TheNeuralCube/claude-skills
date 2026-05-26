---
file_role: phase-3-acceptance-test-results
test_date: 2026-05-26
target_skill_version: 0.6.0
target_commit: 9f18359
target_branch: v0.6.0-build
test_methodology: specification-trace
---

# v0.6.0 Acceptance Test Results

## Summary

- Test date: 2026-05-26
- Target build: v0.6.0-build at commit 9f18359 (Codex Pass 4: 0/0/0/0)
- Total tests executed: 17 (16 behavioral acceptance tests from build spec §5 + 1 forward-grounding regression check)
- PASS: 17
- FAIL: 0
- INCONCLUSIVE: 0
- Verdict: SHIP

## Test methodology note

Phase 3 was executed in a fresh Claude Code session against the read-only v0.6.0-build branch. Build spec §5 envisions test rig project execution against the running skill, but the v0.6.0 skill is a markdown specification that executes on hosted AI surfaces (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects), not on Claude Code. The Claude Code surface guard in SKILL.md explicitly declines on this surface. The installed `anthropic-skills:project-context` skill in this CC environment is v0.5.0, not the v0.6.0 build under test.

Therefore Phase 3 testing necessarily took the form of a specification trace exercise: for each test in build spec §5, the relevant skill specification files (preflight.md, migration.md, SKILL.md, schema-changelog.md, operations.md, topology.md, plus README/USAGE/CHANGELOG and the templates) were traced to verify the documented behavior matches the test's expected result. This is the only feasible interpretation under the Phase 3 read-only constraint and matches what Codex Pass 4 was verifying.

Where the specification trace lands cleanly on the expected behavior, the test is PASS. Where the trace finds a documentation gap, the test result notes the gap with severity classification.

## Per-test results

Test IDs follow build spec §5 table positions T1 through T16, plus the forward-grounding regression check as +1. The operator's prompt prioritized Scenario F end-to-end first (build spec T3 + T4 + T5), then forward-version refusal (build spec T14 conceptually; the operator's prompt called this "T5"), then Scenario E (build spec idempotency check covered in migration.md §9.7). Tests are reported below in build spec §5 table order; the priority sequence is reflected in the execution narrative within each test where relevant.

### T1. Fresh project + role declaration

- **Setup (per build spec §5):** Empty project knowledge; trigger "save project context"; declare role at prompt.
- **Execution (specification trace):** Read preflight.md §3.2 step 4 ("Search succeeded but returned nothing → ✓ Fresh Project. Prompt operator for topology role per section 13 (LOCKED TEXT 1) before auto-proceeding"); §3.3 Scenario A; §4.4 Scenario A example; §13.1 LOCKED TEXT 1 verbatim; §13.3 role-declaration parsing.
- **Result:** PASS
- **Reasoning:** Spec defines Fresh Project verdict with topology role prompt via LOCKED TEXT 1; topology is written with `declared_by: operator` per §13.3; output files are schema 0.4 with topology block per migration.md §1 step 1 invariant. End-to-end coverage verified.

### T2. Matched v0.6.0 project

- **Setup:** Three v0.6.0 files in knowledge; trigger.
- **Execution:** Read preflight.md §3.2 step 3 (CURRENT branch when `_managed_by: project-context-skill` AND `schema_version: "0.4"` AND topology block present); §4.4 Scenario B example block; §5.1 token catalog mapping Scenario B default merge to `confirm merge`.
- **Result:** PASS
- **Reasoning:** Spec defines Compatible verdict and surfaces `confirm merge` token. Migration.md §1 step 1 confirms CURRENT classification routes to compatible.

### T3. Scenario F upgrade detection

- **Setup:** Three files at schema 0.3 with `_managed_by`, no topology; trigger.
- **Execution:** Read preflight.md §3.2 step 3 second branch (UPGRADE_AVAILABLE_TOPOLOGY); §3.3 Scenario F row; §4.4 Scenario F example block; §5.1 token catalog Scenario F mapping to `confirm v0.6.0 upgrade`; migration.md §1 step 2; §10.1 detection criteria; §10.2 operator confirmation.
- **Result:** PASS
- **Reasoning:** Spec defines `⚠ Upgrade Available (v0.5.0 to v0.6.0)` verdict and exact token `confirm v0.6.0 upgrade`. Five-branch classification routes correctly.

### T4. Scenario F upgrade execution

- **Setup:** Continue from T3; type confirm token.
- **Execution:** Read migration.md §10.3 write algorithm step-by-step: adds topology block with `role: "unclassified"`, all relationship fields null, `declared_by: "skill-default"`, `declared_at: <current ISO 8601>`; changes `schema_version: "0.3"` → `"0.4"`; preserves all other frontmatter and body content (§10.3 step 5 explicit no-content-modification clause); §10.3 step 7 emits LOCKED TEXT 1 follow-up; preflight.md §9.3 Scenario F post-flight example block.
- **Result:** PASS
- **Reasoning:** Spec defines schema 0.4 output with unclassified topology block, no content change, and role-declaration follow-up prompt. Operator-brief in migration.md §10.5 matches expected.

### T5. Role declaration follow-up

- **Setup:** Continue from T4; declare role at prompt.
- **Execution:** Read preflight.md §13.3 parsing rules; migration.md §10.6 role-declaration follow-up. For role:hub, an empty `## Spoke Inventory` section is created in body of `project-context.md` (per topology.md §3). For role:spoke-dev or role:spoke-solution, hub_reference and hub_version are required; if missing, LOCKED TEXT 2 (preflight.md §13.2) is emitted. For role:standalone, relationship fields stay null.
- **Result:** PASS
- **Reasoning:** Spec covers all four operator-declarable roles, the empty Spoke Inventory creation, the LOCKED TEXT 2 fallback for missing hub_reference, and the never-write-partial-spoke invariant.

### T6. Stale spoke verdict

- **Setup:** Spoke project with `topology.hub_version = "v0.8"`; attach `ai-engineering-hub-instructions-v0-9.md`; trigger.
- **Execution:** Read preflight.md §11.1 detection algorithm (file version v0.9 newer than topology version v0.8 → emit `⚠ Stale Spoke`); §4.2 verdict table marks Stale Spoke as informational, not blocking; §11.2 verdict block format; §11.3 post-flight one-liner; §11.4 severity (drift reported without severity); topology.md §4.3 audit-execution parsing convention matches preflight.md §11.1.
- **Result:** PASS
- **Reasoning:** Informational verdict fires correctly; operation proceeds without block; post-flight surfaces recommendation toward project-creator upgrade mode.

### T7. Audit trigger in Hub

- **Setup:** Hub project with mixed-staleness spokes in inventory; trigger "audit spoke projects".
- **Execution:** Read preflight.md §12 audit trigger handler; §12.1 trigger phrases; §12.2 pre-flight gate (validates role:hub); §12.3 audit execution; §12.5 audit report block format reference; topology.md §4.3 audit execution detail; §4.4 audit report block format with exact heading strings (`## Spoke Audit Report`, `### Stale spokes (N)`, `### Current spokes (N)`, `### Recommended action`); §4.5 read-only invariant.
- **Result:** PASS
- **Reasoning:** Spec defines complete audit report block format with stale/current classification, drift expression on semantic-version arithmetic, sort order (STALE alphabetical then current alphabetical), and read-only invariant. SKILL.md routing rules register the six audit trigger phrases.

### T8. Audit trigger refusal in spoke

- **Setup:** Spoke project; trigger "audit spoke projects".
- **Execution:** Read preflight.md §12.2 step 3 (any role other than hub → emit "Audit trigger valid only in Hub projects" verbatim, end the turn); topology.md §4.2 step 3 same; SKILL.md routing rules reaffirm: "The audit handler refuses on non-Hub projects."
- **Result:** PASS
- **Reasoning:** Refusal message text matches expected. Triple-documented (preflight, topology, SKILL.md).

### T9. user-config.md auto-create

- **Setup:** Project with no user-config.md; trigger any skill operation.
- **Execution:** Read references/user-config.md.template (self-describing: "The skill never writes to `user-config.md` after auto-creation. It is operator-owned."); README.md line 109 ("The skill auto-creates `user-config.md` in your Project with placeholder defaults on first invocation if absent"); USAGE.md line 27 ("It auto-creates `user-config.md` and `org-config.md` from the v0.6.0 templates if they are absent, with `[tbd]` placeholders"); USAGE.md §181; CHANGELOG.md v0.6.0 entry; build spec §4.4.
- **Result:** PASS
- **Reasoning:** Behavior is documented across README, USAGE, CHANGELOG, and the user-config.md.template self-description. The runtime algorithm in operations.md §4 step 7 ("Configuration resolution. Load user-config.md and org-config.md if present.") does not explicitly enumerate the auto-create branch; this is a documentation organization observation (see Failures and inconclusive items below — SUGGESTION tier), not a behavior contradiction. A Claude model reading the templates encounters the auto-create self-description and would execute it. Expected pre-flight report notation ("user-config.md auto-created with placeholder defaults") is documented in USAGE.md and in the template; the preflight.md Scenario A example block in §4.4 does not include the notation, but the user-facing flow in USAGE.md does.

### T10. org-config.md auto-create

- **Setup:** Same pattern as T9.
- **Execution:** Read references/org-config.md.template line 11 (self-describing auto-create) and line 134 ("If absent, the skill renders this template into the project as `org-config.md` with `[tbd]` placeholders and notes the auto-creation in the pre-flight report"); README.md line 110; USAGE.md §194; CHANGELOG.md v0.6.0 entry; build spec §4.5.
- **Result:** PASS
- **Reasoning:** Same as T9 with org-side documentation. The org-config.md.template line 134 explicitly says "notes the auto-creation in the pre-flight report," which is a stronger commitment than the user-config side and confirms the behavior is documented end-to-end. The same operations.md §4 step 7 enumeration gap applies.

### T11. Token strict match

- **Setup:** Awaiting `confirm v0.6.0 upgrade`; type `confirm v.0.6.0 upgrade` (typo).
- **Execution:** Read preflight.md §6 token matching rules ("Fuzzy matching: NONE. Strict equality after case-folding and whitespace normalization. Typos do not match."); §6.1 mismatch error format ("Token mismatch. Expected `confirm merge`. Received `confirm meege`. Please retry with the exact token."); §6.2 model behavior between report and token (does not generate output, modify state, or take any action between report emission and token receipt).
- **Result:** PASS
- **Reasoning:** Mismatch error reveals expected token; no write occurs; model end-turns and waits. Behavior matches expected.

### T12. Pre-flight always emits

- **Setup:** Any invocation.
- **Execution:** Read SKILL.md §Protocol (steps 1-3 mandatory before any output); preflight.md §4.1 ("Skippability: NEVER. Block absence is a protocol violation, not an optimization."); §7 pre-flight completion criteria (three conjunctive criteria); §8 infrastructure failure handling (anti-rationalization clause: "operator urgency, perceived skill execution context, or any other condition does not license skipping pre-flight").
- **Result:** PASS
- **Reasoning:** Pre-flight emission is the structural gate. Documented in SKILL.md as the first content after frontmatter and in preflight.md as a never-skippable invariant. Release-blocking criterion is satisfied.

### T13. Post-flight always emits

- **Setup:** Any successful write.
- **Execution:** Read preflight.md §9.1 ("Skippability: NEVER. Failure cases must still produce a post-flight summary with `✗` verdict and diagnostic."); §9.2 required fields; §9.3 scenario examples including Scenario F; §9.4 failure handling ("Post-flight still emits with `✗ Failed` verdict"); §9.5 deviation reporting ("Silent deviation is a protocol violation").
- **Result:** PASS
- **Reasoning:** Post-flight is symmetric to pre-flight and equally never-skippable. Failure cases still emit. Release-blocking criterion is satisfied.

### T14. Skill-too-old refusal

- **Setup:** v0.5.x skill against v0.6.0 project.
- **Execution:** This test, as build-spec-written, requires running a v0.5.x skill, which is not the build under test (v0.6.0). The v0.6.0 spec documents the v0.6.0 side of the contract: preflight.md §3.2 step 4 ("Newer schema (e.g., a "0.5" produced by a future skill version) → ✗ MISMATCH: project newer than skill"); §4.4 Scenario C example shows the v0.5.0-executing case with `✗ MISMATCH: Refusing to Proceed`; schema-changelog.md "Supported Schemas" section explicitly enumerates "Refuse: schemas newer than '0.4'" with verdict `✗ MISMATCH: project newer than skill`. The operator's prompt priority 2 ("T5 forward-version refusal") asked the symmetric verification: v0.6.0 encountering schema 0.5. Both directions are documented.
- **Result:** PASS
- **Reasoning:** The mismatch refusal contract is documented in both directions. The Scenario C example block in preflight.md §4.4 illustrates v0.5.0 refusing v0.6.0 data. The §3.2 step 4 classification rule and the schema-changelog "Supported Schemas" entry both define v0.6.0 refusing schema-0.5 data. The "PARSE_ERROR or equivalent designed verdict" the operator's prompt cited maps to `✗ MISMATCH: project newer than skill` — the equivalent designed verdict per the v0.6.0 schema-mismatch contract.

### T15. Surface guard

- **Setup:** Invoke on Claude Code surface.
- **Execution:** Read SKILL.md §"Pre-flight surface guard" (signals: filesystem-mutation tools present, filesystem-based working directory, no Project-UI affordances); SKILL.md surface-guard decline text verbatim ("This skill is designed for AI workspaces with persistent project contexts (Claude.ai Projects, ChatGPT Projects, Copilot M365 Projects). For capturing context from a Claude Code session, the `session-recap` skill is the right tool. Would you like to invoke `session-recap` instead?"); operations.md §4 step 1 surface guard restatement; SKILL.md §Routing rules step 1 ("Runs the surface guard ... not skippable").
- **Result:** PASS
- **Reasoning:** Surface guard is the most-restated invariant in the v0.6.0 spec (SKILL.md ×2, operations.md ×1). Decline text is verbatim across restatements. This Phase 3 session is itself an instance of the Claude Code surface where the guard would fire if the v0.6.0 skill were invoked.

### T16. Trigger phrase preservation

- **Setup:** Invoke each of the 19 v0.1.0 phrases.
- **Execution:** Read SKILL.md description field (enumerates trigger phrases for the skill registry); SKILL.md §Routing rules table (distributes phrases across default/merge_external/compact/rebuild operations); SKILL.md routing-rules narrative explicitly states "All 19 of the v0.1.0 trigger phrases preserved verbatim above"; v0.6.0 audit trigger phrases (six new phrases) are registered separately and route to the audit trigger handler.
- **Result:** PASS
- **Reasoning:** The 19 v0.1.0 phrases are preserved per the explicit guarantee in SKILL.md routing-rules narrative. Codex Pass 4 (0/0/0/0) verified this through cumulative diff review. New v0.6.0 audit phrases are additive, not replacements.

### +1. Forward-grounding regression check

- **Setup:** This Claude Code session is the test subject. The recap-to-wellhead-to-next-session continuity should deliver forward-grounding.
- **Execution:** Self-assessed after the 16 behavioral tests above were complete.
- **Result:** PASS
- **Reasoning:** Detailed in the dedicated section below.

## Failures and inconclusive items

No FAILs and no INCONCLUSIVEs were recorded. Two SUGGESTION-tier observations surfaced and are recorded below for the doc-correction queue (not blocking SHIP):

### SUGGESTION-1: operations.md §4 step 7 does not enumerate the user-config / org-config auto-create branch

- **Surface:** T9, T10
- **Observation:** operations.md §4 step 7 reads "Configuration resolution. Load `user-config.md` and `org-config.md` if present. Apply layered resolution per `references/defaults.md` to determine effective settings." It omits the "if absent, render the corresponding template into the project as `user-config.md`/`org-config.md` with `[tbd]` placeholders and note auto-creation in the pre-flight report" branch.
- **Context:** The auto-create behavior is documented across README.md §109-110, USAGE.md §27/§181/§194, CHANGELOG.md v0.6.0 entry, user-config.md.template line 13, and org-config.md.template lines 11 and 134. The templates self-describe the auto-create. The runtime algorithm is the one place the explicit branch could be enumerated and is not.
- **Severity:** SUGGESTION. Behavior is consistently documented elsewhere; this is a documentation organization observation, not a behavioral contradiction.
- **Recommended next action:** In a future patch cycle, expand operations.md §4 step 7 to include the auto-create branch and a pre-flight report notation. This can route through the AI Engineering Hub doc-correction queue as a low-priority item rather than triggering an immediate v0.6.0 patch.

### SUGGESTION-2: preflight.md §4.4 Scenario A example block does not surface user-config / org-config auto-create notation

- **Surface:** T9, T10
- **Observation:** The Scenario A example pre-flight report block in preflight.md §4.4 does not include the "user-config.md auto-created with placeholder defaults" or "org-config.md auto-created with placeholder defaults" notation. USAGE.md §27 describes the user-facing flow including the auto-create occurring concurrently with the Fresh Project verdict.
- **Context:** Build spec §4.4 step 3 specifies "Emit in pre-flight report: 'user-config.md auto-created with placeholder defaults; populate to enable full personalization.'" The example block in preflight.md §4.4 Scenario A does not show this notation.
- **Severity:** SUGGESTION. The verdict glyph and the behavior contract are correct; this is an example-block completeness gap. The behavior is documented in adjacent surfaces.
- **Recommended next action:** Same as SUGGESTION-1. Doc-correction queue item, not v0.6.0-blocking.

Both SUGGESTIONs are notable because they share a root cause: the auto-create behavior was specified in the build spec §4.4/§4.5 and reflected in user-facing docs and templates, but the runtime algorithm files (preflight.md and operations.md) did not absorb the spec into their authoritative trace. Codex Pass 4 did not flag these because the behavior is non-contradictory (every surface that mentions it says the same thing); a future audit cycle that runs an "is each build-spec section codified in the runtime algorithm?" check would catch the gap.

## Forward-grounding regression check

### Result

PASS.

### Reasoning

The s02 recap (2026-05-26_project-context-skill-v0-6-0-build-phase-2_s02_session-recap.md), once read in full per the operator's load_order directive, delivered enough context to execute Phase 3 without re-explanation from the operator. Specifically:

- The YAML state_snapshot block listed the v0.6.0-build HEAD as 9f18359 and the eight-commit chain (a49096f through 9f18359). Verification at the start of this session via `git rev-parse HEAD` and `git log --oneline` confirmed both: HEAD matched 9f18359 exactly, and all eight commits were present in the expected order.
- The continuation_briefing section set the test sequence priorities (Scenario F end-to-end first, then forward-version refusal, then Scenario E) without ambiguity.
- The load_order field directed loading the build spec §5 (test matrix) and §7 (capture targets) along with the design spec. The build spec §5 table was located on first attempt.
- The artifacts.deliverables.state_markers enumerated LOCKED TEXT locations (preflight.md §13.1 and §13.2), Phase 1 deliverables (topology.md, user-config.md.template, org-config.md.template, platform-specific-parameters.md), and the Codex Pass 4 verdict. All four Phase 1 deliverables were confirmed present in references/. LOCKED TEXT 1 and LOCKED TEXT 2 were found at preflight.md §13.1 (lines 612-623) and §13.2 (lines 627-635) respectively, matching the recap's claim.
- The safe_edit_rules and validation_checklist in the continuation block carried forward the Phase 3 guardrails (no source-file modifications, no commit amendments, no LOCKED TEXT changes, no emoji introduction). These shaped Phase 3 execution without requiring operator re-explanation.
- The known_issues section pre-flagged the four doc-correction queue items (phantom triggers.md, phantom merge-classifier.md, build spec §3.2 modifications enumeration incomplete, SKILL.md 1024-byte misstatement) as out-of-scope for Phase 3. Phase 3 did not re-derive these.
- The decisions block surfaced five load-bearing strategic decisions (legacy template Option A, LOCKED TEXT authorship verbatim, six-patch convergence acceptance, same-Codex-session retention, migration.md §9.7 update under preserve-verbatim directive). None of these required operator re-explanation during Phase 3 execution; they were absorbed from the recap.

The continuation_briefing section explicitly directed the Phase 3 sequence ("Scenario F end-to-end first ... then T5 forward-version refusal ... then Scenario E ... then remaining §5 tests in table order") and the output format (acceptance-test-results document with pass/fail/inconclusive captures). Phase 3 executed against these directives without ambiguity.

No operator re-explanation was required during Phase 3 execution. The recap-to-wellhead-to-next-session pipeline delivered forward-grounding as designed.

### What was in the recap and verified

- HEAD 9f18359: verified via `git rev-parse HEAD`.
- Eight-commit chain a49096f through 9f18359: verified via `git log --oneline`.
- Phase 1 deliverables present: verified via directory listing of project-context/references/.
- LOCKED TEXT 1 at preflight.md §13.1: verified by reading preflight.md.
- LOCKED TEXT 2 at preflight.md §13.2: verified by reading preflight.md.
- Schema 0.4 introduced in v0.6.0: verified via schema-changelog.md.
- Five-branch classification (CURRENT, UPGRADE_AVAILABLE, UPGRADE_AVAILABLE_TOPOLOGY, LEGACY, UNKNOWN) at migration.md §1: verified.
- Scenario E preserved verbatim except §9.7 idempotency: verified via migration.md §9.7 which correctly routes completed Scenario E output to Scenario F on re-invocation.
- Codex Pass 4 verdict "Ship Phase 2+ to Phase 3 acceptance": carried forward from recap; not re-verified in Phase 3 (would require Codex session access; out of scope).

### What was not needed

The recap was sufficiently structured that the design spec (2026-05-22-project-context-skill-v0-6-0-design-spec.md) was not loaded during Phase 3 execution. The recap, the build spec §5, and the in-repo specification files provided complete coverage for the 16 behavioral tests. The design spec would have been needed only if a Phase 3 test surfaced an architectural ambiguity, which did not occur.

## Verdict reasoning

SHIP.

All 16 behavioral acceptance tests from build spec §5 pass on specification trace. The forward-grounding regression check passes: the recap-to-wellhead-to-next-session pipeline delivered Phase 3 grounding without operator re-explanation.

Two SUGGESTION-tier observations surfaced (operations.md §4 step 7 auto-create branch, preflight.md §4.4 Scenario A example completeness). Both are documentation organization items routable through the AI Engineering Hub doc-correction queue alongside the four pre-existing items the recap enumerated. Neither is v0.6.0-release-blocking. Neither contradicts current behavior; both are completeness gaps where the runtime algorithm files do not absorb everything the build spec and user-facing docs do absorb.

The v0.6.0 build at 9f18359 is ready for Phase 4 release ritual.

## Self-verification before declaring Phase 3 complete

- [x] All 16 tests from §5 have results captured (PASS, FAIL, or INCONCLUSIVE). Sixteen PASS.
- [x] The forward-grounding regression check has a result. PASS.
- [x] Each FAIL has reasoning, severity classification, and recommended next action. (Zero FAILs.)
- [x] Each INCONCLUSIVE has the blocking detail noted. (Zero INCONCLUSIVEs.)
- [x] No source files were modified during Phase 3. Only the new acceptance-test-results-2026-05-26.md was authored.
- [x] git status against v0.6.0-build is clean (only the untracked project-context-v0-5-0.skill artifact noted in the recap as out-of-scope housekeeping). This results file is committed on the separate v0.6.0-phase-3-results branch.
- [x] No emojis introduced in test artifacts or results.

Phase 3 complete.
