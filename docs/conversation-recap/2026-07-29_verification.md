# Final Verification Pass: conversation-recap v0.1.0 (PR #11 head)

**Date:** 2026-07-29
**Posture:** independent final verification. Read-only; no source edits, no git writes, no PR edits. This report is the only artifact produced, left untracked.
**Verified tree:** branch `skill/conversation-recap-v0-1-0`, tip SHA `5a6cd260bf3d019886f878eec32fa7f14d70da2d` (matches expected `5a6cd26`), working tree clean except this file and the prior untracked audit note under `docs/`.
**PR state:** #11 OPEN, `isDraft: false` (queried, not inferred), base `main`, head `skill/conversation-recap-v0-1-0`, MERGEABLE.
**Method note:** all exemplar and contract-cell judgments below were reached from the line itself before consulting the prior audit's written reasons; prior justifications were treated as advocacy. All string comparisons, counts, and dash scans were performed programmatically with strict UTF-8 decoding. Line numbers were derived live with `grep -n` at this SHA. Test 1b was not re-run per the pass brief (ran clean at the previous head; nothing since changes generation).

---

## Gate results

| Gate | Result | Evidence |
|------|--------|----------|
| G1 | PASS | Remote `origin` = `https://github.com/TheNeuralCube/claude-skills.git`; branch `skill/conversation-recap-v0-1-0`; `git rev-parse HEAD` = `5a6cd260bf3d019886f878eec32fa7f14d70da2d`. |
| G2 | PASS | `git status --porcelain` shows only untracked `docs/2026-07-29-audit-conversation-recap-v0-1-0.md`. No tracked file modified. |
| G3 | PASS | `gh pr view 11`: state OPEN, isDraft false, base main, MERGEABLE. `gh pr ready` not run (not authorized). |
| G4 | PASS | All three F4 rewrites present in the catalog contract column: "choices as forks with no way back" (Cat:84), "Capability-creates-obligation framing" (Cat:91), "borrowed props not included" (Cat:92). Case-insensitive grep for the three prior labels ("red and blue forks"/"red pill"/"blue pill", "great-power-great-responsibility", "lightsaber") returns zero hits in the catalog. Surviving hits are only in the dated historical design spec (design-spec:129-130) and the prior audit note; see the observation under C2a. AC16 (Spec:269) now carries the word ceiling only ("under 60 words") and no sentence criterion; Section 3.5 (Spec:259) records the deletion of the sentence-count half explicitly. |

---

## C1: Exemplar originality, all 24

Standard applied: would a person who knows the source work read this line and place it to a specific line, scene, or catchphrase? Register recognizability (the line evoking its genre) is the exemplar's stated job and is not a lift; placement to a specific moment or sentence is.

| # | Slug | Verdict | Notes |
|---|------|---------|-------|
| 1 | `novella` | ORIGINAL | Domestic-interior literary voice; no placeable source. |
| 2 | `romance` | ORIGINAL | Generic rehearsed-confession beat; no placeable source. |
| 3 | `war-novella` | ORIGINAL | Terse first-person-plural cost accounting. O'Brien-adjacent cadence at genre level; no placeable line ("we did not talk about the counting" is original construction). |
| 4 | `western` | ORIGINAL | Stranger-rides-into-town is the genre's founding premise (Shane, and dozens since), not one work's property; no lifted line. |
| 5 | `spy-thriller` | ORIGINAL | "above your clearance" close is original; no placeable source. |
| 6 | `mystery-noir` | ORIGINAL | The client-walks-into-the-office opening is genre grammar shared across the whole hardboiled tradition; the coat/problem wisecrack is an original simile, not a Chandler line. |
| 7 | `sci-fi` | ORIGINAL | Machine-answers-the-unasked-question conceit; checked against Clarke and Asimov openings, no placement. |
| 8 | `fantasy` | ORIGINAL | Road-as-agent personification is Tolkien-adjacent at concept level; "the road forgets your name" and "Fewer return changed" are original. |
| 9 | `documentary` | ORIGINAL | Reconstruction-from-the-record framing; generic documentary narration. |
| 10 | `cringe-verite` | ORIGINAL | Parking-dispute premise sits near famous parking episodes in both Seinfeld and Curb, but a parking dispute is universal urban pettiness and the prose, characters, and escalation are original. Premise-adjacency, not placement. |
| 11 | `standup-observational` | ORIGINAL | "Who does that?" is the load-bearing phrase; judged cold, it is generic observational-standup grammar, not a signature Seinfeld quotation (it appears on no list of the show's catchphrases and belongs to the form, not the show). |
| 12 | `office-mockumentary` | ORIGINAL | "Could have been an email" is broad office-culture idiom, not an Office line; the talking-head "leadership" irony is the mode, executed with original words. |
| 13 | `farce-70s` | ORIGINAL | Describes the genre's misunderstanding machinery in original prose. |
| 14 | `living-room-70s` | ORIGINAL | Two chairs, two opinions: the armchair-argument setting is the register's declared territory; no character, no line, no episode placed. |
| 15 | `comedy-movie` | ORIGINAL | Errand-escalates-to-marching-band; checked against known parade/band comedy set pieces, no specific placement. |
| 16 | `simulation-noir` | ORIGINAL (extra scrutiny, judged cold) | See detailed note below. |
| 17 | `street-chronicle-90s` | ORIGINAL | Dedication cadence ("This is for the block...") is the form's shared grammar; checked that no lyric is reproduced in whole or part. |
| 18 | `amblin-wonder` | ORIGINAL | Porch lights, kids-know-first; genre furniture of the whole 80s-suburban mode, no scene placed. |
| 19 | `epic-quest` | ORIGINAL | Runner-up; see below. |
| 20 | `dark-vigilante` | ORIGINAL | Avoids every recognizable formulation ("I am the night," "I am vengeance"); city-as-waiting is original. |
| 21 | `golden-age-hero` | ORIGINAL | Best-version-of-everyone conceit; no Superman line or motto shadowed. |
| 22 | `fourth-wall-antihero` | ORIGINAL | Frame-mocking is the register's function; "I get paid by the aside" is original. |
| 23 | `everyman-hero` | ORIGINAL | Broke-and-late texture with no catchphrase, no name, no scene. |
| 24 | `space-opera` | ORIGINAL | "In a time of fragile alliances..." uses crawl grammar (the register's licensed framing device) without shadowing any actual crawl's text; checked against the openings of the film crawls, no sentence skeleton match. |

**Verdict spread: 24 ORIGINAL, 0 ECHO, 0 LIFT.**

**`simulation-noir` detailed note (judged cold, no credit for being a replacement).** The line's three elements: a barista writing a name before hearing it, a crowd opening and closing "precise as water," and "whatever is running this... only the small things ever slip." Nearest neighbors checked: the Matrix's glitch conceit (deja vu, the black cat) — different mechanism, different furniture, no second-person address, no monologue skeleton; the Matrix crowd moments (the red-dress training program, Agents stepping out of crowds) — no shared element beyond "a crowd in a simulation"; The Truman Show's choreographed world (the world running on script around one man) — closest conceptual neighbor, but there is no barista scene, no name-on-cup moment, and no line in that film this sentence shadows. The prior exemplar failed because it reproduced a specific monologue's second-person skeleton; this line has no second person, no monologue source, and its imagery (name on cup, crowd as water) does not exist in any specific scene I can place. A Matrix or Truman Show fan would recognize the register, which is the job; they could not place a line or a scene. ORIGINAL.

**Closest runner-up: `epic-quest` (Cat:99).** "The company set out with light hearts and heavy packs, and only one of them understood how far the road truly went. He said nothing, and shouldered a little more of the load." A Lord of the Rings reader will map this instantly to the departure of the Fellowship and to the secretly-burdened companion (Frodo's knowledge, Sam's carrying ethos). I cleared it anyway because the mapping is to an archetype, not a sentence or scene: no proper noun, no lifted phrase ("shouldered a little more of the load" shadows no Tolkien line, including the famous "I can carry you" construction, which it deliberately does not echo), and the line is content-neutral where Tolkien's scenes are specific. The register-true criterion (Spec:256) requires exactly this level of evocation. It sits closest to the line of any of the 24 because "the company set out" brushes against Tolkien's own recurring "the Company," but sentence-initial, lowercase, and unaccompanied by any second identifying element, it does not cross.

---

## C2a: The three F4 rewrites

| Slug | Rewrite | Instruction preserved? | Output unplaceable? | Judgment |
|------|---------|------------------------|---------------------|----------|
| `simulation-noir` | "choices as red and blue forks" → "choices as forks with no way back" (Cat:84) | Yes: frame choices as irreversible binary forks. Same story shape. | Yes: an irreversible fork without color-coding is generic decision furniture; the pill scene is placeable only through the colors, which are gone. | **Fix holds.** |
| `everyman-hero` | "Great-power-great-responsibility framing" → "Capability-creates-obligation framing" (Cat:91) | Yes: frame small choices as ability creating duty. Same device by function. | Yes: this is a functional description, not a renamed artifact. A generator following it produces the framing without the sentence; reproducing the catchphrase itself remains separately banned by the register-integrity rule (Skill:153) and the failure-mode list (Skill:168). A knowing reader of the catalog cell would decode the reference, but the cell never prints; only its product does. | **Fix holds.** |
| `space-opera` | "lightsabers not included" → "borrowed props not included" (Cat:92) | Yes, and the rewritten clause was a guard, not an instruction: the generation instruction (crawl permitted, empires and rebellions mapped) is untouched in the same cell. | Yes, and the guard is now broader: it bans all franchise props by function instead of naming one by proper noun. | **Fix holds; marginally stronger than the original.** |

None of the three removed the instruction; none merely renamed the artifact. All three pass.

**Observation (non-blocking):** the historical design spec still carries the pre-fix contract text ("Great-power-great-responsibility framing," "lightsabers not included") at design-spec:129-130. It is a dated governing-input record and nothing reads it at runtime, so this is acceptable as history; but a future rebuild that regenerates the catalog from design spec Section 8 would reintroduce the leak. Worth a one-line amendment note in the design spec at the next touch, not now.

## C2b: Independent re-sweep of the 21 unflagged contract cells

Criteria: (a) proper-noun objects from a specific work, (b) quoted or near-quoted lines, (c) devices named by IP-specific label rather than function. Verdicts were reached before re-reading the fix pass's reasons.

| # | Slug | Verdict | Note |
|---|------|---------|------|
| 1 | `novella` | CLEAN | |
| 2 | `romance` | CLEAN | "will-they-won't-they" is trade vocabulary, not IP. |
| 3 | `war-novella` | CLEAN | |
| 4 | `western` | CLEAN | |
| 5 | `spy-thriller` | CLEAN | |
| 6 | `mystery-noir` | CLEAN | |
| 7 | `sci-fi` | CLEAN | |
| 8 | `fantasy` | CLEAN | "named artifacts" is generic. |
| 9 | `documentary` | CLEAN | |
| 10 | `cringe-verite` | CLEAN | Functional descriptions of the machinery, no episode named. |
| 11 | `standup-observational` | CLEAN | "who DOES that" is quoted in the cell but is the form's grammar, not a show quotation; and this family names its show openly by ratified design (Table B). |
| 12 | `office-mockumentary` | CLEAN | |
| 13 | `farce-70s` | CLEAN | |
| 14 | `living-room-70s` | CLEAN | Contract cell is functional; the armchair reference lives in the DNA column, which describes rather than directs, and the family names its show by design. |
| 15 | `comedy-movie` | CLEAN | |
| 16 | `street-chronicle-90s` | CLEAN | |
| 17 | `amblin-wonder` | CLEAN | "bikes, cul-de-sacs, flashlights" are common nouns, the shared furniture of the entire genre, not props from one film. (The slug itself is a separate matter; see C2c.) |
| 18 | `epic-quest` | CLEAN, near call | Ruling below. |
| 19 | `dark-vigilante` | CLEAN | |
| 20 | `golden-age-hero` | CLEAN | |
| 21 | `fourth-wall-antihero` | CLEAN | |

(The 21 are the 24 minus the three rewritten cells; `space-opera`'s crawl clause is examined below because the prior pass called it a near call.)

**Ruling on `space-opera`, "opening-crawl framing device" (Cat:92).** The prior defense — a scrolling prologue is film craft predating the franchise — holds, and I verified its factual basis independently: the crawl was standard serial-film practice (the 1930s Flash Gordon and Buck Rogers serials) that the franchise deliberately imitated. Reader's-standard test: a reader of a crawl-framed space-opera recap places the device to "a Star Wars-style crawl," but that is the register performing its declared, touchstone-labeled job, and what they place is a device the franchise itself borrowed, not that franchise's expression. The lift line is crossed only if the generated crawl reproduces actual crawl wording, and lifted lines are banned by the register-integrity rule regardless. **Clear stands. Defense holds.**

**Ruling on `epic-quest`, "Fellowship framing" (Cat:87).** I concur with the clear but reject half of the prior defense. The sentence-initial-capital argument is weak: the word does its recognition work regardless of case, and a reader of the cell places capital-F "Fellowship," in a register whose DNA says "LOTR-flavored," to The Fellowship of the Ring instantly. What actually sustains the clear is different: (1) "fellowship" retains a live common-noun function (a bonded company; continuous pre-Tolkien usage), which "lightsaber" and "red pill" never had, so a generator following "Fellowship framing" can and naturally will produce lowercase, descriptive fellowship-of-companions framing, which is unplaceable as a lift; (2) the cell never prints; the only leak route is the generator naming the group "the Fellowship" as a proper noun in output, and lifted names are already banned (Skill:153); (3) the reader's-standard failure requires placeable output, and output produced under this instruction that obeys the standing name ban is not placeable. Of the 21, this is the one cell where a functional rewrite ("bonded-company framing") would be marginally safer, and I recommend it as v0.1.1 hardening, not as a merge blocker. **Clear stands, on corrected grounds.**

## C2c: Register slug ruling

**Can a slug reach generated output? Yes, verbatim, twice.** SKILL.md:90: the title card's mandatory attribution line is `*A story recap in the <register-slug> register, inspired by <source>.*` — the slug prints in every recap. SKILL.md:111: the slug also appears in every saved filename. The slug additionally reaches the operator through the picker (SKILL.md:66).

**All 24 slugs checked.** Twenty-three are tradition-named and non-IP: genre terms (`war-novella`, `space-opera`), decade-anchored forms (`farce-70s`, `street-chronicle-90s`), and functional descriptions (`fourth-wall-antihero`, `simulation-noir`, `epic-quest`, `dark-vigilante`). One is not.

**`amblin-wonder` breaches the letter of the touchstone doctrine.** The doctrine (Spec:25, marked "operator decision 2026-07-17, governing") states: "Slugs and the title-card `inspired-by` attribution stay non-IP and tradition-named," with the stated purpose that "the printed artifact stays clean of IP naming." "Amblin" is the name of a specific production company, a live registered trademark of an active rights-holder, and it prints in the title card of every `amblin-wonder` recap and in every saved filename. Compounding this, Spec:23 asserts "every slug is already tradition-named rather than franchise-named" as part of the doctrine's rationale — an assertion this slug falsifies in the trademark sense. No prior pass examined this.

**Why this is a real finding and not a manufactured one:** the same architecture this PR just enforced in F4 (text that reaches the output page must not name IP; text that only describes may) applies a fortiori here — the slug does not merely direct output, it *is* output, verbatim, every time.

**Why it is nevertheless a narrow finding:** it is not a lift. A company name in an identifier is attribution-flavored, not creative expression; nothing is quoted, no character or line is reproduced, and the reader's-standard test in this pass's brief governs *lines*, which this is not. There is also a genuine spirit-level defense: "Amblin" functions in film criticism as the accepted shorthand for this exact genre ("Amblin-era," "Amblin-esque"), so a case exists that it *is* the tradition's name, the way "Hitchcockian" derives from a person — but unlike those, Amblin has not genericized and remains a named rights-holder, and the doctrine's letter says non-IP without exception. Finally, the ecosystem already prints real IP names in title cards by ratified design in the comedy family ("inspired by Seinfeld," Table B), so the operator's revealed policy tolerates deliberate IP naming in attribution; what it has not ratified is *this* instance, which contradicts the specific bargain struck for the franchise family.

**Ruling: doctrine breach, letter-level, output-reaching, operator decision required.** This is not nothing, and it is not a lift. It is the one place the tree contradicts its own governing doctrine, and only the operator can regularize it.

## C3: Regressions

All programmatic. Files read with strict UTF-8 decoding (Python `bytes.decode("utf-8")`, which raises on invalid sequences); no cp1252 fallback was possible.

**R1. Dash scan, per surface:**

| Surface | U+2014 em | U+2013 en |
|---------|-----------|-----------|
| `conversation-recap/SKILL.md` | 0 | 0 |
| `conversation-recap/references/register-catalog.md` | 0 | 0 |
| `docs/2026-07-17_conversation-recap_build-spec.md` | 0 | 0 |
| `docs/2026-07-17_conversation-recap_test-fixture_the-command-standup.md` | 0 | 0 |

**R2. Touchstone equality:** all 24 catalog touchstone strings compared programmatically against build spec Table D (Spec:225-250): **24/24 exact matches.** (Also re-verified inspired-by strings against Tables A/B/C: 24/24.)

**R3.**
- AC1 identity triple: directory `conversation-recap/` exists; YAML `name: conversation-recap` (Skill:2); H1 `# conversation-recap (v0.1.0)` (Skill:10). PASS.
- AC13: 24 slugs, all unique, partitioned 9 literary / 6 comedy / 9 cinematic. PASS.
- YAML description: **734 characters** against the 1024 limit. PASS.
- Fabrication-rule blockquote (Skill:143) vs. build spec Section 2.6 (Spec:124): **byte-identical** (292 characters). The inline restatement at Skill:52 also matches the rule text exactly. PASS.
- Bonus regression: all 24 exemplars pass the AC16 word ceiling; longest is `simulation-noir` at 48 words. Fixture body recount: exactly 656 words, matching the calibration anchor at Skill:82. PASS.

**R4. Interiority clause and thin-source rule.**

Interiority clause, present twice (Skill:54 and Skill:145, identical text): "Interiority is framing, not fact: attributed motives and inner states are permitted only as the narrator's openly-marked read of behavior the source records. ... The test is whether the subject could read the line and say 'that did not happen': a visible inference survives it, an asserted inner state does not." Reading: this *refines* the fabrication rule rather than contradicting it — the verbatim rule bans invented facts; the clause classifies openly-marked inference as framing (which the rule licenses as "comic distortion of framing") and asserted inner states as facts (which the rule bans). The boundary test is operational and consistent with the ratified fixture's own precedent line. No contradiction.

Thin-source rule (Skill:80): "When the traceable source cannot fill the called tier without invention, drop to the tier the source can support and write to that tier's budget instead. ... The fabrication rule outranks the tier budget, always. ... Word-budget conformance is then measured against the tier actually written, so the tier band is satisfied by the drop rather than broken by it." Reading: this resolves the fabrication-vs-floor tension by explicit precedence (fabrication outranks budget) and redefines conformance against the tier actually written, so it contradicts neither the fabrication rule nor the tier table; it is consistent with, and cites, the judgment-call doctrine's one-line-call format. No contradiction.

Test 1b was not re-run, per the pass brief.

---

## VERDICT: FIX FIRST

One item. Everything else in this pass — all 24 exemplars, all 24 contract cells, the three F4 rewrites, and every regression check — is clear.

**Required change (C2c, `amblin-wonder` slug vs. the touchstone doctrine).** The tree currently contradicts its own governing doctrine (Spec:25) in output-reaching text, resting partly on a false supporting claim (Spec:23, "every slug is already tradition-named"). Either remedy closes it; the choice is the operator's, and no edits were made here:

1. **Rename the slug** to a non-IP form (e.g. `suburban-wonder`), cascading to: the catalog row and exemplar label (Cat:86, Cat:98), both SKILL.md bias lists (Skill:65, Skill:155), and an amendment note in the build spec (AC13 pins slugs to design spec Section 8, so the design spec needs a dated amendment line too). The Table D touchstone "E.T.-style Amblin wonder" may keep "Amblin"; the touchstone field is where IP naming is licensed. **Or:**
2. **Ratify the exception in one sentence**, added to the touchstone doctrine (Spec:25) and/or the catalog preamble: that the `amblin-wonder` slug knowingly carries a production-company name used as the genre's accepted critical shorthand, and the operator accepts it in the title card and filename. This also corrects the Spec:23 assertion by exception.

Option 2 is doc-only and non-breaking. Until one lands, the merge would ship a known letter-level breach of an operator-ratified governing rule, which a final verification pass cannot wave through on its own authority.

---

## What I could not verify

- **The originality judgments are bounded by my own recall of the source works.** I compared each line against the famous formulations I can retrieve (monologues, catchphrases, opening skeletons, iconic scenes). A line echoing a less-famous passage — a deep-cut Chandler sentence, a specific war-novel paragraph, an album skit — could pass me exactly as it passed the two prior sessions, and for the same reason: we recall the same corpus the same way. This is the structural blind spot the brief names, and no in-family pass removes it. A human fan-check of the 24 lines, especially `epic-quest`, `war-novella`, and `simulation-noir`, remains the only real closure.
- **The ratified fixture's provenance.** The tree asserts the 656-word run is operator-ratified verbatim and that its source-facts line traces to a real thread. Nothing in the tree can prove either; I verified internal consistency (word count, facts-line coverage), not provenance.
- **Whether "who DOES that" is Seinfeld-signature.** I judged it generic observational grammar from my own knowledge of the show's recognized catchphrases. I did not (and per read-only scope, could not meaningfully) corroborate against an external corpus. If the operator knows it as a recurring signature line, my C1 #11 and C2b #11 clears weaken.
- **Where my agreement may have come too easily:** (1) I cleared `epic-quest`'s exemplar and its "Fellowship framing" cell on the archetype-vs-expression and common-noun-function distinctions; both are defensible, but both are also exactly the kind of careful justification the brief warns reads persuasive because it is written the way I reason. I flagged the cell for v0.1.1 hardening rather than blocking, and I am not fully certain that grading is severity, not agreeableness. (2) I accepted the comedy family's real-show title cards as ratified design without re-litigating, as the prior audit also did; the C2c ruling partially leans on that acceptance (the "revealed policy" argument), so if the operator ever revisits Table B, the amblin analysis shifts with it. (3) My FIX FIRST offers a one-sentence ratification as a sufficient remedy; a stricter reader could call that an escape hatch. I judged it proportionate because the breach is naming, not expression — but that judgment is mine, not the doctrine's.
