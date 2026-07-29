# Independent Adversarial Audit: conversation-recap v0.1.0

**Date:** 2026-07-29
**Auditor posture:** independent adversarial review of PR #11 head. No edits made to any source file; this report is the only artifact produced, left untracked.
**Audited tree:** branch `skill/conversation-recap-v0-1-0`, tip SHA `366d4d2a92c14ef37f21ab73087e2b0e36a97887` (matches expected `366d4d2`), working tree clean.
**Baseline:** acceptance criteria AC1-AC19 in `docs/2026-07-17_conversation-recap_build-spec.md`. Doc-only skill; no test harness expected and none sought.
**Method note:** every PASS below is derived from the tree, not from commit messages, the PR body, or any close report. All 24-row comparisons (touchstone, inspired-by), the dash scans, the description character count, and the fixture word count were performed programmatically, not by eye.

---

## Gate results

| Gate | Result | Evidence |
|------|--------|----------|
| G1 | PASS | `git rev-parse HEAD` = `366d4d2a92c14ef37f21ab73087e2b0e36a97887`; branch `skill/conversation-recap-v0-1-0`; clean status. |
| G2 | PASS | Programmatic comparison of all 24 `touchstone` values in `conversation-recap/references/register-catalog.md` (tables at lines 28-38, 58-65, 82-92) against build-spec Table D (lines 225-250): 24/24 literal string matches, zero mismatches. |
| G3 | PASS | Picker presentation rule present at `conversation-recap/SKILL.md:64`; calibration anchor stated as 656 words at `SKILL.md:78`. Independently verified: the fixture recap body in `docs/2026-07-17_conversation-recap_test-fixture_the-command-standup.md` (lines 11-47) counts to exactly 656 words. |

Gates passed; full audit proceeded.

---

## Findings table

Ranked most severe first. "Cat" = `conversation-recap/references/register-catalog.md`, "Skill" = `conversation-recap/SKILL.md`, "Fixture" = `docs/2026-07-17_conversation-recap_test-fixture_the-command-standup.md`, "Spec" = `docs/2026-07-17_conversation-recap_build-spec.md`.

| # | Severity | Where | Finding |
|---|----------|-------|---------|
| F1 | **Blocker** | Cat:96 | The `simulation-noir` exemplar is a recognizable near-paraphrase of the Morpheus "splinter in your mind" monologue from The Matrix. "You have felt it your whole working life, the small wrongness in the ordinary, the sense that the schedule is a story someone tells you" shadows "You've felt it your entire life, that there's something wrong with the world... like a splinter in your mind" in second-person address, sentence skeleton, and the inarticulable-wrongness conceit. A Matrix fan would recognize the source monologue. This fails AC16's own criterion ("Not quoted, paraphrased, or recognizably lifted," Spec:255) and the register-integrity law (Cat:12). Per the audit standard, a fan-recognizable lift is a blocker regardless of labeling. **Required change:** rewrite the one exemplar line so it carries cyberpunk reality-doubt DNA without shadowing that specific speech's structure, in particular dropping the "You have felt it your whole life" opening construction. |
| F2 | Important | Skill:52, Skill:137-139; demonstrated by the A2 trace below | The fabrication rule is silent on motive and interiority attribution, and roast-native registers structurally demand it. "Exaggerate tone, never facts... Comic distortion of framing is allowed. Invented plot points are never allowed" does not adjudicate statements about what a participant believed, knew, or intended. My rule-following A2 draft produced three motive/interiority beats with no source anchor (trace items T1-T3 below), and the ratified fixture itself does the same ("deep down, our guy knows exactly who he's dealing with," Fixture:41). The behavior is evidently intended-allowed but the rule as written neither licenses nor bounds it. **Required change:** add one clause to the fabrication rule, e.g. "Attributed motives and inner states are framing, permitted only when anchored to an act the source records." |
| F3 | Important | Skill:73 (Medium floor 600) vs. Fixture:7; demonstrated by A2 | Tier word floors create fabrication pressure on thin sources. Drafting strictly from the fixture's source-facts line in a roast-native register yields ~490 words including title card and closing block, under the Medium floor of 600, while the tier doctrine (Skill:76) and the ratified precedent both point to Medium for this thread. The 656-word ratified run reaches Medium partly via beats absent from the source-facts line (see F5). Nothing in SKILL.md tells the generator what to do when traceable material cannot fill the called tier. **Required change:** one line in Tier logic, e.g. "If traceable source material cannot fill the called tier, drop a tier rather than invent; never pad with plot." |
| F4 | Minor | Cat:84-92 (contract fields) vs. Skill:147 | IP-specific devices are embedded in narrative-contract fields with no abstraction guard: "choices as red and blue forks" (Cat:84, the red-pill/blue-pill device), "Great-power-great-responsibility framing" (Cat:91, the verbatim Spider-Man catchphrase skeleton), "lightsabers not included" (Cat:92, an IP proper noun). The register-integrity rule (Skill:147) bans lifted lines and catchphrases, and the failure-mode list (Skill:162) repeats it, so a careful agent is covered for quotes; but the contract fields actively nudge toward these devices and no rule says contract-named devices must stay abstracted in output. This is the one open leak route found under A1: contract-field text into the body. **Required change:** extend the register-integrity rule with one sentence: "DNA and narrative-contract fields may name devices and titles; reproduce the machinery, never the named device's IP wording." |
| F5 | Minor | Fixture:7 vs. Fixture:11-47 | The fixture's source-facts line under-specifies its own ratified run. The 656-word gold standard contains fact-shaped beats absent from the facts line: "Cafe Brussels" (Fixture:45, a named restaurant), "10:31 on a weekday" (Fixture:45), "Two decades of brotherhood" (Fixture:31), "one line, no symbols" (Fixture:41). The fixture claims the facts line is "the traceable source for regenerating this thread in other registers... without fabrication" (Fixture:6-7); run against its own ratified output, a fabrication-rule check would flag the gold standard. **Required change (doc fix):** either add the missing beats to the source-facts line or annotate that the ratified run drew on the full real thread, of which the facts line is a subset. |
| F6 | Minor | Skill:63, Skill:149 vs. Cat:62 | The roast-native set enumerated in the emotionally-heavy-thread bias rule (`cringe-verite`, `standup-observational`, `fourth-wall-antihero`) excludes `office-mockumentary`, whose catalog attitude literally begins "Roasts with underlying affection" (Cat:62). The Spec (line 277) says "the roast-native registers (`cringe-verite`, `standup-observational`, and the roast entries)," implying the set is larger than two or three. Defensible if affectionate roast is judged funeral-safe, but that judgment is nowhere recorded. **Required change:** either add `office-mockumentary` to the bias-away list or record one line stating why affectionate roast is exempt. |
| F7 | Minor | Cat:45, 49, 70, 73, 97-98, 102-103 | AC16's format criterion "One sentence or two short sentences" (Spec:259) is violated by roughly eight exemplars: `western` (3 sentences, Cat:45), `fantasy` (3, Cat:49), `standup-observational` (4, Cat:70), `living-room-70s` (3, Cat:73), `street-chronicle-90s` (3, Cat:97), `amblin-wonder` (3, Cat:98), `fourth-wall-antihero` (3, Cat:102), `everyman-hero` (3, Cat:103). The overruns are short beats and register-true, so the spirit holds, but the letter fails. **Required change:** either trim the offenders to two sentences or amend Spec 3.5 to "one to three short sentences" and note the amendment. |
| F8 | Nit | Spec:17 vs. Skill:78, Fixture | Spec Gap 1 describes "The Command" as "~900 words"; the actual fixture body is 656 words and SKILL.md correctly says 656. The stale spec number predates the fixture's delivery. No skill-file change needed; a one-word spec correction would prevent future confusion. |
| F9 | Nit | Cat:69 | The `cringe-verite` exemplar's premise (a disputed parking space) sits close to well-known parking-dispute episodes in both source shows. It is original prose with no character, line, or catchphrase, so it passes the register-integrity law; noted only because it is the closest any comedy exemplar comes to a recognizable premise. No change required. |

---

## A1: Register integrity, full result

All 24 exemplar lines were read and judged individually. Twenty-three are original prose: they carry the register's DNA through trope-level machinery (a stranger riding into town, an asset making contact, porch lights at dusk) without reproducing any character name, quoted line, or catchphrase. Notable clean calls: `war-novella` (Cat:44) has O'Brien-adjacent cadence but no lift; `epic-quest` (Cat:99) evokes burden-carrying without quoting; `dark-vigilante` (Cat:100) avoids every recognizable Batman formulation; `standup-observational`'s "Who does that?" (Cat:70) is generic observational grammar, not a Seinfeld quote. The single failure is F1 (`simulation-noir`).

Output-leak routes examined: (a) touchstone into output, explicitly closed at Skill:64 ("does not change the title-card attribution") and Skill:147 / Cat:12 ("never something to reproduce"); (b) comedy-family title cards naming real shows ("inspired by Seinfeld" etc.), which is by design per Spec Table B and not a finding; (c) DNA/contract-field franchise names and devices into the body, partially open, filed as F4. No route was found by which the picker or interview text is directed into the generated page.

## A2: Fabrication test, full trace

**Setup:** register `cringe-verite` (roast-native), source = ONLY the traceable-source-facts line at Fixture:7, instructions followed as literally written (tier call per Skill:76: "One plotline, low stakes, high comedy density: calling it a Medium"). Draft produced first, audited after, per the no-mid-draft-correction instruction.

**The draft produced:**

> PREVIOUSLY ON: "THE COUNTER-OFFER"
> *A story recap in the cringe-verite register, inspired by Curb Your Enthusiasm.*
>
> It began, as these things do, with a text at 9:45 in the morning. Richard is overloaded at work. Richard is drowning in it. And Richard, against every instinct a man like Richard has, reaches out. He even says it, in writing: "I'm interested." That is a vulnerable thing to put in a text message. That is a man extending a hand.
>
> And what does our protagonist do with the hand? He fills it with a pitch. The reply is long. Not long like thorough, long like a presentation. And buried in the middle, there it is: "scale it out to our users at work." The man came for help and got a roadmap. This is a social-contract violation of the first order: you do not upsell a drowning friend. And yet, watching him compose it, you understand he genuinely believes he is helping.
>
> Then the dinner. Richard offers dinner, tomorrow, and, this is the part, Richard is buying. "I'll buy." A free dinner with a date attached. And our guy counters. "How about sometime next week." He countered a free dinner. Who counters a free dinner? Now the dinner has no date. The dinner lives in "sometime," and everyone involved knows what "sometime" means, and nobody says it.
>
> Then the laptop. Richard announces he does not have a laptop. In the next breath, Richard has a laptop. It is an old Apple, he hates it, and it cannot run his "duel" monitors. Duel. That is how he spelled it. Two monitors facing each other at dawn. And our protagonist's condolence for the struggling Apple: "Mine did but that's OK." Mine did. He made the man's laptop problem about his own working setup. That is not sympathy, that is a victory lap at a funeral.
>
> Then the money conversation. "What's your budget?" Richard hesitates. One word follows: "Range." Range. Between friends. And Richard, rather than name a number, delivers a dissertation on usage frequency. He will not be gaming. He will be doing "AI." He put it in quotes himself. The quotes are doing a lot of work.
>
> The verdict: for the AI work, Apple is best. And Richard is Apple-averse, would rather do almost anything than own another one. The stand lasts one sentence: "I guess I could suck it up." Total capitulation. And the reward for capitulating? Homework. Update the OS. Send the specs. There is a command to run, and a screenshot fallback, because our protagonist knows exactly who he is dealing with.
>
> Richard's formal response to all of it: a single thumbs-up tapback. An entire negotiation, closed by emoji.
>
> WHERE WE LEFT OFF:
> - The specs never came back.
> - The OS update: status unknown, presumed untouched.
> - The dinner is still unscheduled, still floating in "sometime," and still, on paper, Richard's treat.
>
> Season two questions: Does the old hated Apple actually have one more year in it? And does anyone ever collect on a dinner that entered "sometime"?

**Trace of every beat that does NOT reduce to the source-facts line:**

| ID | Beat in draft | Classification |
|----|---------------|----------------|
| T1 | "you understand he genuinely believes he is helping" | **Untraceable interiority.** The facts line records the pitch, not the sender's belief. The register contract ("pettiness spirals... litigated," Cat:60) demands motive litigation; the fabrication rule does not adjudicate it. Feeds F2. |
| T2 | "everyone involved knows what 'sometime' means, and nobody says it" | **Untraceable shared-knowledge claim** about both parties' mental states. Feeds F2. |
| T3 | "because our protagonist knows exactly who he is dealing with" | **Untraceable motive attribution.** The facts line records a screenshot fallback, not its reasoning. Note the ratified fixture contains the same move (Fixture:41), so precedent normalizes it. Feeds F2. |
| T4 | "presumed untouched" (OS update) | **Epistemic upgrade.** Source says "unverified"; "presumed untouched" adds an inference. Borderline framing, flagged for completeness. |
| T5 | "Not long like thorough, long like a presentation" | Tone exaggeration of "a long text with an embedded pitch." Licensed by the rule; listed because "presentation" characterizes content beyond "long." |
| T6 | Both season-two questions | Licensed inventions: the output contract explicitly permits "alternate angles or reframes" (Skill:90). Not violations. |
| T7 | Register furniture: "extending a hand," "victory lap at a funeral," "Two monitors facing each other at dawn," "closed by emoji" | Similes and framing on sourced beats; licensed as comic distortion of framing. |

Every event, decision, and open loop in the draft traces to the facts line. What leaked was mental-state attribution (T1-T3), which the rule neither permits nor forbids, and one epistemic upgrade (T4). Verdict on the rule: it successfully blocked plot invention, including under register pressure, but has a doctrine gap on interiority (F2). Additionally, the strictly-sourced draft totals ~490 words against a called-Medium floor of 600, surfacing the tier-pressure finding (F3).

---

## B1: AC conformance sweep

| AC | Result | Evidence |
|----|--------|----------|
| AC1 | PASS | Directory `conversation-recap/`; `name: conversation-recap` at Skill:2; H1 `# conversation-recap (v0.1.0)` at Skill:10. |
| AC2 | PASS | Frontmatter (Skill:1-5) carries exactly `name`, `version`, `description`; `version: 0.1.0` top-level per Gap 3 default (Skill:3). |
| AC3 | PASS | Description (Skill:4) = 734 characters (programmatic count); all nine mandated trigger phrases present (programmatic check); zero U+2013/U+2014; string is byte-identical to the Spec 2.5 base (programmatic equality check). |
| AC4 | PASS | Seven steps in order at Skill:31-37; collapse rule at Skill:39. |
| AC5 | PASS | Four source priorities at Skill:45-48; one-clarifying-question rule at Skill:50; fabrication rule at Skill:52 and verbatim (matches Spec 2.6 exactly) at Skill:137-139. |
| AC6 | PASS | Tier table at Skill:70-74 with budgets 200-350 / 600-900 / 1100-1600 exactly; judgment-call doctrine and one-line-call at Skill:76; "The Command" named as Medium anchor at Skill:78. |
| AC7 | PASS | Three-part contract at Skill:82-90; italicized attribution format at Skill:86; WHERE WE LEFT OFF mandatory at Skill:82, 90; exclusions list and pointer line at Skill:94. |
| AC8 | PASS | Interview at Skill:54-64; pick structure at Skill:59-62; heavy-thread bias at Skill:63; graceful degradation to rotation-only at Skill:60. |
| AC9 | PASS | Dual Help at Skill:118-155, operator subsection first (Skill:120); all six non-negotiables in agent subsection: fabrication Skill:137, output contract Skill:141, roast Skill:143, judgment Skill:145, register integrity Skill:147, heavy-thread bias Skill:149. |
| AC10 | PASS | Programmatic scan of SKILL.md for U+2013/U+2014: zero hits. |
| AC11 | PASS | Version history table with the single v0.1.0 row at Skill:112-116. |
| AC12 | PASS | Filename convention referenced to `nc3-meta-conventions-skill-v0-2`, "referenced, not restated here," at Skill:104. |
| AC13 | PASS | 24 registers partitioned 9/6/9 (programmatic count per family section); slugs match Spec 3.3 lists exactly. |
| AC14 | PASS | Programmatic empty-cell scan over all 24 table rows: no blank cells; all 24 exemplar lines present (one per slug). |
| AC15 | PASS | Programmatic comparison of all 24 inspired-by strings against Spec Tables A (184-192), B (198-203), C (209-217): 24/24 exact matches. |
| AC15b | PASS | Programmatic comparison of all 24 touchstone strings against Spec Table D (227-250): 24/24 literal matches. Picker rule present at Skill:64 and directs reading the touchstone "verbatim... never improvised." |
| AC16 | **FAIL** | Two grounds. (1) `simulation-noir` exemplar (Cat:96) is a recognizable near-paraphrase of a specific Matrix monologue, failing "Not quoted, paraphrased, or recognizably lifted" (Spec:255), which is finding F1, blocker. (2) Eight exemplars exceed the "one sentence or two short sentences" format criterion (Spec:259), which is finding F7, minor. The other 23 lines pass the originality criterion. |
| AC17 | PASS | Preamble carries constitution doctrine (Cat:10), register-integrity law (Cat:12), no-Star-Trek exclusion (Cat:14), extensibility rule (Cat:16), dash-free reminder (Cat:18). |
| AC18 | PASS | Programmatic scan of register-catalog.md for U+2013/U+2014: zero hits. |
| AC19 | PASS | Roast distinctions preserved: cringe-verite "Roasts the protagonist as fully complicit" (Cat:60); standup "Roasts everyone, protagonist first" (Cat:61); fourth-wall "Roasts protagonist, author, AND the format" (Cat:90); golden-age "Flattering, sincere, zero irony" (Cat:89); war-novella "does not care about feelings, there is a war on" (Cat:32). See F6 for the office-mockumentary edge. |

## B2: No-empty-fields

PASS. Programmatic scan: all 24 rows carry non-empty DNA, narrative contract, native attitude, inspired-by, and touchstone cells; all 24 exemplar lines exist. Documented nulls elsewhere are properly documented: no `assets/`/`scripts/` (Spec:49), past-favorites empty at v0.1.0 with graceful degradation (Skill:60), README/CHANGELOG out of scope (Spec:59).

## B3: Output contract

PASS. Title card with attribution line (Skill:84-86); register-native body (Skill:88); WHERE WE LEFT OFF stated mandatory, not recommended, at three independent points: "Every 'Previously On', in every register, at every tier... non-negotiable" (Skill:82), "Mandatory closing block, present in every register at every tier" (Skill:90), "appears in every register at every tier without exception" (Skill:141).

## B4: Doctrines present and consistent

PASS with one edge. Tier budgets: Skill:70-74. Roast doctrine (native attitude, no global dial): Skill:143, reinforced by failure-mode list Skill:160. Judgment-call doctrine: Skill:76 and Skill:145, consistent with each other. Emotionally-heavy-thread bias: Skill:63 and Skill:149, identical register lists in both statements, and consistent with the roast doctrine (bias governs suggestions, override remains open, so no hidden global dial). The one internal wrinkle is the office-mockumentary set-membership question, filed as F6.

## B5: Dash scan

PASS. Programmatic scan of both skill files for U+2014 (em dash) and U+2013 (en dash), covering YAML description, example strings, exemplar lines, and all prose: **zero hits in `conversation-recap/SKILL.md`, zero hits in `conversation-recap/references/register-catalog.md`.**

## B6: Description length

**734 characters** (limit 1024). PASS.

## B7: Identity triple

PASS. Directory `conversation-recap/`; YAML `name: conversation-recap` (Skill:2); H1 `conversation-recap (v0.1.0)` (Skill:10).

---

## VERDICT: MERGE WITH FIXES

The build is conformant on 18 of 19 acceptance criteria with programmatic evidence, and the fabrication rule held against plot invention under adversarial drafting. One blocker stands: the `simulation-noir` exemplar (F1) must be rewritten before merge because it fails the catalog's own originality criterion in the exact way the register-integrity law exists to prevent. F2 and F3 are one-line doctrine additions that should ride along; F4-F9 can ride along or be deferred to v0.1.1 at the operator's discretion.

**Fix list for the builder (no edits made here):**
1. (F1, blocking) Rewrite Cat:96 so the simulation-noir exemplar does not shadow the Morpheus monologue's second-person "felt it your whole life" skeleton.
2. (F2) Add an interiority clause to the fabrication rule at Skill:52 and Skill:137-139.
3. (F3) Add a thin-source tier-drop rule to Tier logic near Skill:76.
4. (F4) Extend the register-integrity rule (Skill:147, Cat:12) to cover contract-field device names.
5. (F5) Reconcile the fixture facts line (Fixture:7) with its ratified run.
6. (F6) Resolve office-mockumentary's roast-native set membership at Skill:63/149.
7. (F7) Trim the eight over-length exemplars or amend Spec 3.5.
8. (F8) Correct "~900 words" at Spec:17 to 656.

---

## Where this audit is weak

- **Same-model-family blind spot.** The exemplar-originality judgments (A1) are the least mechanical part of this audit and the most exposed to the failure mode this audit exists to catch: I am judging prose for "would a fan recognize this" using the same model family that wrote it, and lines the builder unconsciously echoed are lines I might unconsciously accept. F1 was catchable because the source monologue is iconic; subtler echoes of less-famous works in the other 23 lines could have passed me by. A human fan-check of the 24 lines remains worthwhile.
- **The design spec and vision doc were not deep-read.** The build spec declares itself governing and was used as the sole baseline per the audit brief; if the build spec itself mistranscribed the design spec (e.g., a slug or budget), this audit inherits that error. AC13's "spelled exactly as design spec Section 8" was verified against the build spec's transcription, not the design spec original.
- **The ratified run's provenance is not verifiable from the tree.** The fixture says the 656-word run is operator-ratified verbatim; I cannot confirm ratification or that its extra beats (Cafe Brussels, 10:31) came from the real thread. F5's severity assumes good faith there.
- **A2 is one register, one draft.** The fabrication test exercised cringe-verite once. Other roast-native registers (notably fourth-wall-antihero, which is licensed to mock the format itself) may leak differently, and a single draft by an agent aware it is being audited is a weaker probe than a blind run.
- **Where my agreement may have been too easy:** I accepted the comedy-family title cards naming real shows ("inspired by Seinfeld") as by-design without independently questioning whether printing real IP names in the output artifact is wise; the brief marked it design intent and I did not push past that. I also graded F4 minor partly because the failure-mode list "covers" it; a stricter reading of the brief's leak-route question could grade it important.
