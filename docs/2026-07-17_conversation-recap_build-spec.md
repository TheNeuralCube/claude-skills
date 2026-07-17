# conversation-recap -- Build Spec (v0.1.0)

**Document type:** Build Spec (execution-ready for Claude Code)
**Date:** 2026-07-17
**Status:** Draft for operator approval, then build
**Governing inputs:** `2026-07-17_conversation-recap_design-spec.md` (primary), `2026-07-17_conversation-recap_vision.md` (context)
**Precedence rule for build:** the build spec governs. Where the build spec is silent, the design spec governs. Where both are silent, flag, do not improvise.
**Style law (carries into this document and every built file, including runtime strings):** no em dashes or en dashes anywhere. Hyphens and commas only.

---

## 0. INFORMATION GAP BLOCK (consolidated, read first)

Per the no-empty-fields principle, every item that cannot be fully resolved from the two input docs is listed here with a recommended default. Items marked BLOCKS-PHASE-2 or BLOCKS-PHASE-3 do not block approval of this build spec; they are surfaced now so the operator can clear them before the gated phase runs. Items marked BUILD-DECISION carry a recommended default that the build will apply unless the operator overrides at approval.

1. **[INFORMATION GAP: Phase 3 test source material] (BLOCKS-PHASE-3, material).**
   Design spec Section 11 item 1 requires regenerating "the Richard thread recap" and comparing against "the two ratified test runs." Neither the Richard thread source material nor the two ratified test runs (war-novella Short, documentary Medium) is reproduced in either input doc. Project search confirms they are not present in project knowledge. The Seinfeld calibration run "The Command" (~900 words) is named as the Medium gold standard but is likewise not reproduced.
   Consequence: the fabrication rule forbids inventing the thread's facts, so the test cannot be run against the operator's real Richard thread from the corpus available, and the "compare against the two ratified test runs" step cannot be performed at all without those artifacts.
   Recommended resolution at Phase 3: operator supplies the Richard thread source (a handoff, recap, or transcript) plus the two ratified runs; OR, if unavailable, Phase 3 substitutes a clearly labeled synthetic test fixture (a fabricated thread declared as a fixture, never presented as the operator's real life) to exercise contract compliance and tier budgets, and explicitly records that the gold-standard comparison was skipped for lack of the reference runs. Do not silently fabricate a "Richard thread" as if it were real source.

2. **[INFORMATION GAP: franchise-flavored inspired-by strings] (BUILD-DECISION).**
   Design spec Section 7 gives the attribution rule for only two families: real-show DNA names the show ("inspired by Seinfeld"), pure-genre names the tradition ("inspired by the war novella tradition"). The cinematic/franchise-flavored family (9 registers) sits between: its DNA column references specific franchises (Matrix-flavored, ET-flavored, Batman-register, and so on), yet the family is explicitly declared "registers, never fan fiction," and every slug is already tradition-named rather than franchise-named.
   Recommended default (applied unless overridden): franchise-flavored registers name the tradition or milieu, not the franchise (for example `simulation-noir` -> "inspired by the cyberpunk tradition"), consistent with the no-lifted-IP doctrine and the tradition-named slugs. `street-chronicle-90s` is the one the design spec resolves directly ("stories from that world, not real persons"), so it names the world: "inspired by the world of 90s hip-hop." Full proposed mapping in Section 3.4, Table C.

3. **[INFORMATION GAP: frontmatter version field shape] (BUILD-DECISION, verify at package).**
   Design spec Section 1 and Section 10 mandate `version: 0.1.0` as a top-level frontmatter field. Named peer `session-handoff` and `project-context` both use a top-level `version:` field; the third new-generation peer `transcript-metadata-tagger` nests it as `metadata:\n  version: 0.1.0`. The claude.ai packaging validator (`package_skill.py`) is not present in this environment (no `/mnt/skills`), so the field it reads cannot be confirmed here.
   Recommended default: follow the design spec and the majority of named peers, top-level `version: 0.1.0`. If the packaging validator at upload rejects it or ignores it, mirror `transcript-metadata-tagger` by nesting under `metadata:`. Recorded as a verify-at-upload item, not a build blocker.

4. **[INFORMATION GAP: dual Help section vs. peer practice] (RESOLVED, noted).**
   The design spec Section 10 item 3, the meta-conventions skill, and an explicit build non-negotiable all require a dual Help section (operator subsection primary). Two named reference peers (`session-handoff`, `transcript-metadata-tagger`) do not actually carry a `## Help` section. Resolution: the governing docs win. Build includes the dual Help section. This is a peer divergence note, not an open gap.

5. **[INFORMATION GAP: license header] (BUILD-DECISION, low risk).**
   New-generation peers open the body with `<!-- SPDX-License-Identifier: Apache-2.0 -->` and `<!-- Copyright 2026 Raul J. Soto -->`. The design spec does not mention license headers. Recommended default: carry the same two comment lines into `SKILL.md` and `references/register-catalog.md` for ecosystem consistency and the operator-owned house-style posture (vision Section 5). Provenance: inferred from peers, not spec-mandated.

6. **[INFORMATION GAP: repo not present] (BLOCKS-PHASE-2).**
   The `TheNeuralCube/claude-skills` repository is not checked out in this environment, and there is no `gh` CLI auth and no SSH key present. Phase 2 cannot create the branch or commit until the repo is available (cloned with a supplied remote URL and working credentials, or staged by the operator).

7. **[INFORMATION GAP: Neural Cube git identity] (BLOCKS-PHASE-2).**
   The build prompt requires verifying that git identity resolves to the Neural Cube profile before the first commit. This environment pins committer identity to `Claude <noreply@anthropic.com>` via a session-start hook (required for CCR commit signature verification) and enforces it with a stop hook. No separate Neural Cube profile is configured. Before Phase 2 commits, the operator must confirm the intended author/committer identity and how it reconciles with the CCR signing constraint (for example, committing under the Anthropic-signed identity with a Neural Cube co-author trailer, or committing in an environment where the Neural Cube identity is authorized). Flagged now; resolved at Phase 2 start.

No other fields in this build spec are empty. Every module section below carries purpose, exact path, content outline, acceptance criteria, and test hooks.

---

## 1. Build Scope and Module Inventory

Two files are built, no more. No scripts, no `modes/` router (registers are data, not modes, per design spec Section 10 item 4). The optional `assets/` and `scripts/` directories are intentionally omitted (documented null: not needed at v0.1.0).

| # | Module | Path (repo-relative) | Kind |
|---|--------|----------------------|------|
| 1 | Skill entry point | `conversation-recap/SKILL.md` | Required |
| 2 | Register catalog | `conversation-recap/references/register-catalog.md` | Required |

Repo root target: `conversation-recap/` (plain directory name, no prefix, no version in directory name).
Identity triple that must match exactly: directory `conversation-recap`, YAML `name: conversation-recap`, H1 `# conversation-recap (v0.1.0)`.

Supporting repo-hygiene files (README, CHANGELOG, and similar) that the peers carry are OUT of scope for v0.1.0 unless the operator requests them; documented null with reason: design spec Section 10 item 4 fixes the file structure at `SKILL.md` + `references/register-catalog.md` only.

---

## 2. Module 1: `conversation-recap/SKILL.md`

### 2.1 Purpose

The single entry point and the entire execution brain of the skill. It detects the trigger, acquires source material, runs the mood interview, makes the tier and register judgment calls, generates the recap against the fixed output contract, offers a re-cut, and (only on request) saves a file. It also carries every non-negotiable doctrine inline so the runtime never needs a second file to behave correctly. The register catalog is the one thing it defers to `references/register-catalog.md`.

### 2.2 Exact file path

`conversation-recap/SKILL.md`

### 2.3 Content outline (sections in order)

1. **YAML frontmatter.**
   - `name: conversation-recap`
   - `version: 0.1.0` (top-level; see Gap 3)
   - `description:` the Section 10 draft from the design spec, verbatim as the base, validated under 1024 characters before commit. The exact string to use is quoted in Section 2.5 below.
2. **License header comments** (Gap 5): SPDX Apache-2.0 line and `Copyright 2026 Raul J. Soto` line, immediately below the frontmatter, matching peer placement.
3. **H1:** `# conversation-recap (v0.1.0)`
4. **One-paragraph identity blurb.** What the skill is: the low-fidelity, narrative bottom rung of the fidelity ladder. Names its two ladder siblings and states the disambiguation (state vs. appetite). Names "Previously On" as the output brand, `conversation-recap` as the functional skill name.
5. **## When to use this skill.** Prose plus the trigger phrases. Restore-appetite framing (vision Sections 1 and 2). Explicit not-for pointers: machine state -> `session-handoff`; structured summary -> `nc3-session-recap-skill`; reflective record -> `per-jrn-journal-entry`.
6. **## Execution flow.** The seven-step pipeline from design spec Section 3, reproduced as a numbered protocol: TRIGGER, SOURCE, INTERVIEW, TIER CALL, GENERATE, DEBRIEF, OPTIONAL SAVE. State the collapse rule: when the operator specifies register and/or tier at invocation, skip the interview for what was specified and interview only for what is unspecified.
7. **## Source material acquisition.** The four-priority input ladder from design spec Section 5 (explicit file input; named past conversation; current thread stale head; pasted transcript or notes). The one-clarifying-question rule for thin or ambiguous sources. The fabrication rule stated in full here and again in the agent Help section.
8. **## The interview.** Design spec Section 6, as runtime instructions: host voice is a premiere-night announcer, not a settings menu; identify the thread (skip if stated); offer 3 to 4 register picks as a selectable list built from 1 to 2 past favorites plus 1 to 2 rotation picks, always allowing free-text or mashup; the emotionally-heavy-thread bias rule (grief, conflict, spiritual matter bias away from roast-native registers toward documentary, novella, amblin-wonder; do not Seinfeld a funeral). Past-favorites source at v0.1.0 is documented as "none" (see Section 5, Open Decision item 2, recommend defer to v0.2.0); the interview logic must degrade gracefully to rotation-only picks when no usage history exists.
9. **## Tier logic.** The three tiers from design spec Section 4 as a table (Short / The Teaser / 200 to 350 words / 60 to 90 sec; Medium / The Cold Open / 600 to 900 words / default; Long / The Season Recap / 1100 to 1600 words / sagas only). The judgment-call doctrine: AI picks the tier from complexity, open-thread count, stakes, and elapsed time; states the call in one line; operator overrides by exception. Same doctrine extends to structure, framing device, and intensity. Calibration anchor named: the "The Command" Medium run.
10. **## Output contract.** The fixed three-part contract from design spec Section 7, stated as non-negotiable:
    - Title card, two lines: `PREVIOUSLY ON: "<INVENTED EPISODE TITLE>"` then the italicized attribution line `*A story recap in the <register-slug> register, inspired by <source>.*` The `<source>` string is read from the catalog entry, never improvised.
    - Register-native body: chronological arc (how it started, progressed, insights, turns, decisions), native attitude, register-appropriate framing device allowed.
    - `WHERE WE LEFT OFF`: mandatory closing block in every register at every tier, open loops as scannable short-line cliffhangers, register-flavored but literal enough to act on, optional 1 to 2 "season two questions."
    - Low-fidelity inclusion contract (what must survive): arc, every decision, every keep-worthy insight, every open loop, the emotional register of the original.
    - Deliberate exclusions (what must be dropped): YAML, IDs, file paths, configs, schema, command syntax, metadata. Close with the pointer line when the operator needs state: *"For working state, see the session handoff."*
11. **## Debrief and re-cut.** One-line check that length and register landed; offer a re-cut in another register or tier if not.
12. **## Saving output.** Default delivery is in-chat and ephemeral. On explicit save request only, filename per the pattern in design spec Section 9, which references (does not restate) the Output Artifact Filename Convention in `nc3-meta-conventions-skill-v0-2`. Pattern: `{YYYY}-{MM}-{DD}_{Topic_Words}-{register-slug}-{tier}_conversation-recap.md`. Suffix is `conversation-recap`.
13. **## Version history.** A table with a single row for v0.1.0 (date 2026-07-17, "Initial build per 2026-07-17 design spec").
14. **## Help.** Dual section, operator subsection first and primary (this is an action skill):
    - **### For the Operator.** Plain language: what a Previously On is, when to reach for it, how to steer it (name a register, name a tier, or let the skill choose), that it is entertainment and ephemeral by default, and that it will point back to the handoff when real state is needed.
    - **### For the Agent.** Protocol instructions. Must embed, in full and inline, the four non-negotiables named in design spec Section 10 item 6 plus the two additional build non-negotiables:
      - Fabrication rule (verbatim, see Section 2.6).
      - Output contract (title card + inspired-by attribution line, register-native body, mandatory WHERE WE LEFT OFF block).
      - Roast doctrine: native attitude per register, no global dial; choosing the register is choosing the treatment.
      - Judgment-call doctrine: AI picks tier and structure, states the call in one line, operator overrides by exception.
      - Register integrity rule: registers are style DNA with original characters and dialogue; no lifted IP characters, no lifted lines, ever; the inspired-by attribution names the source.
      - Emotionally-heavy-thread bias rule, restated as agent logic.
      Also: references to related skills (`session-handoff`, `nc3-session-recap-skill`, `nc3-meta-conventions-skill-v0-2`), the execution-sequence summary, and the common failure modes (fabricating facts, dropping the WHERE WE LEFT OFF block, applying a global roast dial, roasting an emotionally heavy thread, emitting an em dash or en dash).

### 2.4 Voice and format constraints

Protocol-style voice matching `session-handoff` and `project-context`: imperative, declarative, "you MUST" for hard rules. No em dashes, no en dashes, anywhere, including inside example strings and the description. The skill's own host voice (used at runtime toward the operator) may have personality; the SKILL.md instructional prose stays protocol-flat.

### 2.5 Description string (validated base)

Use the design spec Section 10 draft as the base, adjusted only to strip any en/em dashes (the source uses " -- " double-hyphen sequences, which are legal). Confirm the final character count is under 1024 before commit. Base string:

> Generate low-fidelity NARRATIVE conversation recaps ("Previously On..." format) that re-immerse the operator in a stale conversation or project thread: narrative arc, insights, and open loops as cliffhangers, at minimal cognitive cost. Trigger on: 'previously on', 'catch me up', 'recap me in', 'what did I miss', 'reimmerse me', 'season recap this thread', 'where did we leave off with [topic]', 'Seinfeld me', 'war novella recap', or any request for an entertaining low-fidelity recap in a named register. Runs a short mood interview (register + tier: teaser/cold-open/season-recap), then generates per the register catalog. NOT for machine-readable state (use session-handoff) or structured summaries (use nc3-session-recap-skill).

Note: the design spec draft used " -- " in two places; the build must render those as a colon or comma to honor the no-dash law while keeping meaning. The version above already does this.

### 2.6 Fabrication rule (verbatim string to embed)

Embed this exact text in the agent Help section:

> Fabrication rule: the narrative shaping may exaggerate tone, never facts. Every event, decision, and open loop in the recap must be traceable to the source. Comic distortion of framing is allowed. Invented plot points are never allowed. This is a recap, not fiction about the operator's life.

### 2.7 Acceptance criteria (Module 1)

- AC1. Directory name, YAML `name`, and H1 all read `conversation-recap` exactly; H1 carries `(v0.1.0)`.
- AC2. Frontmatter has exactly `name`, `version`, `description` (version per Gap 3 default).
- AC3. `description` is under 1024 characters, contains the mandated trigger phrases, and contains zero em/en dashes.
- AC4. All seven execution-flow steps present and ordered; collapse rule stated.
- AC5. All four source-input priorities present; one-clarifying-question rule present; fabrication rule present in both the source section and the agent Help section.
- AC6. Tier table present with all three word budgets exactly as design spec Section 4; judgment-call doctrine and one-line-call rule present; "The Command" named as the Medium calibration anchor.
- AC7. Output contract present with all three mandatory parts; the italicized attribution line format present; the WHERE WE LEFT OFF block declared mandatory for every register and tier; the deliberate-exclusions list and the "For working state, see the session handoff" pointer present.
- AC8. Interview section present with the register-pick structure and the emotionally-heavy-thread bias rule; graceful degradation to rotation-only when no usage history.
- AC9. Dual Help section present, operator subsection first; all six non-negotiables embedded in the agent subsection.
- AC10. Zero em dashes and zero en dashes in the entire file (automated check: grep for U+2014 and U+2013 returns nothing).
- AC11. Version history table present with the v0.1.0 row.
- AC12. Naming and filename rules are referenced to `nc3-meta-conventions-skill-v0-2`, not restated.

### 2.8 Test hooks (from design spec Section 11)

- Feeds Test 1 (Richard thread in war-novella Short and documentary Medium): SKILL.md must be sufficient, together with the catalog, to produce a contract-compliant recap from source alone. Verifies AC7.
- Feeds Test 2 (tier word budgets within plus or minus 15 percent): the tier table and word budgets in this file are the reference the generated output is measured against. Verifies AC6.
- Feeds Test 3 (emotionally-heavy-thread simulation): the interview-section bias rule in this file is what the simulation exercises. Verifies AC8.
- Feeds Test 4 (description length): AC3 is the pre-check; the packaging validator (or the character-count fallback, since `/mnt/skills` is absent here) is the confirm.

---

## 3. Module 2: `conversation-recap/references/register-catalog.md`

### 3.1 Purpose

The style-contract library. It holds all 24 registers as data the generation pipeline reads at runtime. Per register it defines: slug, DNA, narrative contract, native attitude, the inspired-by attribution string used in the title card, and one original exemplar opening line that demonstrates the register's voice without lifting any IP. It also carries the catalog preamble that states the constitution doctrine and the register-integrity law.

### 3.2 Exact file path

`conversation-recap/references/register-catalog.md`

### 3.3 Content outline

1. **License header comments** (Gap 5): SPDX and Copyright lines.
2. **H1:** `# conversation-recap Register Catalog (v0-1)`
3. **Preamble.** Carries three doctrines as prose, so the runtime reads them whenever it opens the catalog:
   - Constitution doctrine (vision Section 7): an invisible Catholic moral spine governs what the stories value (fidelity, repentance, mercy, dignity of persons, consequences that mean something); never announced, never preached in-text, plainly owned if the operator or an audience member asks where the stories come from.
   - Register-integrity law (vision Section 5, design spec Section 2): registers are stylistic DNA, not licensed characters; original characters, original dialogue, the operator's own life as material; no lifted characters, no lifted lines, no reproduced IP, ever.
   - Explicit exclusion: no Star Trek register.
   - Extensibility rule (design spec Section 8): new registers are added by appending an entry (slug, DNA, contract, attitude, inspired-by, exemplar line) and bumping the skill MINOR version; mashups are allowed at generation time without a catalog entry.
   - Style law reminder: exemplar lines and all catalog prose contain no em dashes and no en dashes.
4. **Three family sections**, each a table plus per-register exemplar lines. The tables reproduce the design spec Section 8 columns exactly (slug, DNA, narrative contract, native attitude) and add the inspired-by column. The exemplar opening line for each register is authored at build time under the criteria in Section 3.5 (one per register, original, register-appropriate, dash-free).
   - Literary family: `novella`, `romance`, `war-novella`, `western`, `spy-thriller`, `mystery-noir`, `sci-fi`, `fantasy`, `documentary` (9).
   - Comedy family: `cringe-verite`, `standup-observational`, `office-mockumentary`, `farce-70s`, `living-room-70s`, `comedy-movie` (6).
   - Cinematic/franchise-flavored family: `simulation-noir`, `street-chronicle-90s`, `amblin-wonder`, `epic-quest`, `dark-vigilante`, `golden-age-hero`, `fourth-wall-antihero`, `everyman-hero`, `space-opera` (9).
   Total: 24 registers.

### 3.4 Inspired-by attribution strings (build-ready mapping)

These are the exact `<source>` strings the title card reads. Real-show DNA names the show; pure-genre names the tradition; franchise-flavored names the tradition or milieu per Gap 2 recommended default. Tables A and B are fully determined by design spec Section 7. Table C applies the Gap 2 default and is subject to operator override at approval.

**Table A, Literary family (determined):**

| Slug | inspired-by string |
|------|--------------------|
| `novella` | inspired by the literary fiction tradition |
| `romance` | inspired by the romance tradition |
| `war-novella` | inspired by the war novella tradition |
| `western` | inspired by classic Westerns |
| `spy-thriller` | inspired by the espionage fiction tradition |
| `mystery-noir` | inspired by the detective noir tradition |
| `sci-fi` | inspired by the science fiction tradition |
| `fantasy` | inspired by the fantasy tradition |
| `documentary` | inspired by the documentary tradition |

**Table B, Comedy family (determined; real-show DNA names the show):**

| Slug | inspired-by string |
|------|--------------------|
| `cringe-verite` | inspired by Curb Your Enthusiasm |
| `standup-observational` | inspired by Seinfeld |
| `office-mockumentary` | inspired by The Office |
| `farce-70s` | inspired by Three's Company |
| `living-room-70s` | inspired by All in the Family |
| `comedy-movie` | inspired by the broad film comedy tradition |

**Table C, Cinematic/franchise-flavored family (Gap 2 default, override-eligible):**

| Slug | inspired-by string (recommended) |
|------|----------------------------------|
| `simulation-noir` | inspired by the cyberpunk tradition |
| `street-chronicle-90s` | inspired by the world of 90s hip-hop |
| `amblin-wonder` | inspired by the 80s suburban wonder tradition |
| `epic-quest` | inspired by the high fantasy quest tradition |
| `dark-vigilante` | inspired by the caped-vigilante noir tradition |
| `golden-age-hero` | inspired by the golden-age superhero tradition |
| `fourth-wall-antihero` | inspired by the fourth-wall-breaking antihero tradition |
| `everyman-hero` | inspired by the everyman superhero tradition |
| `space-opera` | inspired by the space opera tradition |

If the operator prefers franchise-naming for Table C (for example "inspired by The Matrix"), the build swaps these strings; the register-integrity law is unaffected either way because attribution names a lens and never licenses lifting characters or lines.

### 3.5 Exemplar opening line criteria (authored at build)

Each register gets exactly one original opening line, authored during Phase 2, meeting all of:
- Original prose. Not quoted, paraphrased, or recognizably lifted from any source work, character, or catchphrase.
- Register-true. Demonstrably carries the DNA and native attitude of its entry (a reader could guess the register from the line).
- Self-contained and content-neutral. Illustrates voice without depending on any specific thread, so it reads as a style sample.
- Dash-free. No em dashes, no en dashes.
- One sentence or two short sentences. It is an opening beat, not a paragraph.

The build spec does not pre-author these 24 lines; authoring them is Phase 2 creative work governed by the criteria above. This is a documented deferral, not an empty field.

### 3.6 Acceptance criteria (Module 2)

- AC13. All 24 registers present, correctly partitioned into the three families, slugs spelled exactly as design spec Section 8.
- AC14. Each register row carries all five data fields: DNA, narrative contract, native attitude, inspired-by string, exemplar line. No blanks.
- AC15. Inspired-by strings match Tables A and B exactly; Table C matches the approved mapping (default or operator override).
- AC16. Each exemplar line satisfies every criterion in Section 3.5; spot-check that no line reproduces a known character name, catchphrase, or quoted line.
- AC17. Preamble carries all four doctrines (constitution, register-integrity, no-Star-Trek exclusion, extensibility) plus the dash-free reminder.
- AC18. Zero em dashes and zero en dashes in the entire file (automated grep check).
- AC19. Native-attitude text preserves the roast-doctrine distinctions (roast-native registers stay roast-native; flatterers flatter; war-novella stays unsentimental).

### 3.7 Test hooks (from design spec Section 11)

- Feeds Test 1: the `war-novella` and `documentary` entries (DNA, contract, attitude, inspired-by, exemplar) are the exact style contracts the two Richard thread runs are generated against. Verifies AC13 to AC16, AC19.
- Feeds Test 3: the roast-native registers (`cringe-verite`, `standup-observational`, and the roast entries) and the bias-toward set (`documentary`, `novella`, `amblin-wonder`) are the registers the emotionally-heavy-thread simulation selects between; their attitude fields must make the bias correct. Verifies AC19 and, jointly with SKILL.md AC8, Test 3.
- Feeds Test 1 title-card check: the inspired-by strings are what the generated title card must reproduce verbatim. Verifies AC15.

---

## 4. Cross-Cutting Non-Negotiables (carry into every file and every runtime string)

1. No em dashes, no en dashes, anywhere. Hyphens and commas only. Enforced by grep for U+2014 and U+2013 at end of build.
2. Fabrication rule: recaps may exaggerate tone, never facts. Embedded verbatim in the agent Help section (Section 2.6).
3. Output contract fixed: title card with PREVIOUSLY ON plus the inspired-by attribution line, register-native body, mandatory WHERE WE LEFT OFF block.
4. Roast doctrine: native attitude per register, no global dial.
5. Judgment-call doctrine: AI picks tier and structure, states the call in one line, operator overrides by exception.
6. Registers are style DNA with original characters and dialogue. No lifted IP characters, no lifted lines, ever. Inspired-by attribution names the source.
7. YAML description under 1024 characters; validate before commit.
8. Dual Help section, operator subsection primary.
9. Emotionally heavy threads bias away from roast-native registers in the interview; embedded in interview logic.

---

## 5. Open Decisions Preserved from Design Spec Section 12

1. Skill name: RESOLVED (final), `conversation-recap`, `version: 0.1.0` in frontmatter. No build action.
2. Usage-history mechanism for "past favorites" in the interview: Open Brain captures vs. local history file vs. none at v0.1.0. Design spec recommends none at v0.1.0, add at v0.2.0 once field patterns emerge. Build applies "none at v0.1.0" and makes the interview degrade to rotation-only picks. Carried to session close.
3. Whether Previously On outputs auto-offer a Wellhead capture: design spec recommends no (entertainment artifacts pollute the brain; capture the decisions from the underlying thread instead). Build offers no auto-capture. No build action beyond honoring the recommendation.

---

## 6. Build Sequence (Phase 2, after approval only)

1. Clear Gap 6 and Gap 7 (repo present, git identity confirmed).
2. Create branch `skill/conversation-recap-v0-1-0`.
3. Create `conversation-recap/` at repo root, then `conversation-recap/references/`.
4. Author `SKILL.md` per Section 2. Validate description length and dash-freeness.
5. Author `references/register-catalog.md` per Section 3, including the 24 exemplar lines.
6. Run the automated dash check and the AC checklist across both files.
7. Proceed to Phase 3 validation (design spec Section 11) before the commit.

Commit message (Phase 3, after validation passes):
`feat(conversation-recap): v0.1.0 initial build per 2026-07-17 design spec`

---

## 7. Ecosystem Debt (preserve, do not fix this session)

`nc3-meta-conventions-skill` needs a v0-3 bump to document the new-generation naming standard (plain directory name, `version:` in frontmatter, semver dots) and a migration posture for legacy `nc3-*` and `per-*` skills. Tracked in the hub session handoff. Not fixed in this build session.
