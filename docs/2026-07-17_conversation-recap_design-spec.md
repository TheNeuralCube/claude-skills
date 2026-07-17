# conversation-recap -- Design Spec (v0.1.0)

**Document type:** Design Spec (build-ready for Claude Code)
**Date:** 2026-07-17
**Status:** Draft for operator ratification, then build
**Companion document:** `2026-07-17_conversation-recap_vision.md`
**Governing conventions:** `nc3-meta-conventions-skill-v0-2` for file structure, dual Help sections, YAML description limits, and output artifact filenames. **CAVEAT:** its skill-naming and version-in-directory-name rules are superseded for this skill by the new-generation standard in field use (`session-handoff`, `project-context`, `transcript-metadata-tagger`): plain directory name, `version:` field in YAML frontmatter, semver dots. The conventions skill requires a v0-3 bump to document this; do not block the build on it.

---

## 1. Identity

- **Skill name:** `conversation-recap` (ratified 2026-07-17, final). Plain functional name, new-generation standard: no prefix, no version in directory name.
- **Brand vs. name:** the skill name is functional so agents discover it by purpose; "Previously On" is the product brand and appears only in output title cards and trigger phrases. Agents call `conversation-recap`; humans watch "Previously On."
- **Ladder position:** third rung of the fidelity ladder beside `nc3-session-recap-skill`. The YAML descriptions carry the disambiguation between the two: structured/state recap (session) vs. narrative/story recap (conversation).
- **Version:** `version: 0.1.0` in YAML frontmatter (semver, dots). Directory name, YAML `name` field, and H1 heading must all read `conversation-recap` and must match exactly. Version lives ONLY in the frontmatter, never in the directory name.
- **One-line purpose:** Generate a low-fidelity, persona-driven, narratively shaped "Previously on..." recap of a stale conversation or project thread, to restore the operator's orientation and appetite at minimal cognitive cost.

## 2. What This Skill Is Not

- Not a session recap (medium fidelity, structured, agent-consumable). If the operator needs state, route to `nc3-session-recap-skill` or `session-handoff`.
- Not a journal entry (`per-jrn-journal-entry`). Journals are reflective records; this is re-entry entertainment.
- Not fan fiction. Registers are style contracts with original characters and dialogue. No lifted IP characters or lines, ever.

## 3. Execution Flow

```
1. TRIGGER        Operator invokes ("previously on", "catch me up", "recap me in", etc.)
2. SOURCE         Acquire source material (Section 5)
3. INTERVIEW      Mood elicitation (Section 6) -> register selected
4. TIER CALL      AI judges tier from complexity + stakes (Section 4); states the call; operator may override
5. GENERATE       Produce the recap per output contract (Section 7) in the chosen register (Section 8)
6. DEBRIEF        One-line check: length/register land? Offer re-cut in another register if not
7. OPTIONAL SAVE  Only on request; filename per Section 9
```

Steps 3-4 collapse when the operator specifies register and/or tier at invocation ("Seinfeld me on the Richard thread, medium"). Respect explicit parameters; interview only for what is unspecified.

## 4. Tiers

Tier is a length/immersion contract measured in reading time (~230 wpm silent reading).

| Tier | Name | Reading time | Word budget | Contract |
|------|------|-------------|------------|----------|
| Short | The Teaser | 60-90 sec | 200-350 | Pure hook. Open loops only, minimal arc. For threads the operator half-remembers. |
| Medium | The Cold Open | 2-3 min | 600-900 | Full arc + native attitude + all open loops. **The default.** |
| Long | The Season Recap | 4-6 min | 1100-1600 | Immersive, multi-thread, act structure. Reserved for sagas: multiple plotlines, high stakes, long gap since last contact. |

**Judgment-call doctrine (operator-ratified):** the AI picks the tier from story complexity, number of open threads, stakes, and time elapsed. It states its call in one line ("One plotline, low stakes, high comedy density: calling it a Medium") and proceeds. The operator overrides by exception. Same doctrine applies to structure, framing devices, and intensity within a register: the AI decides, the operator tweaks.

**Calibration anchor:** the 2026-07-17 Seinfeld-register test ("The Command", ~900 words) is the ratified gold standard for Medium feel and native-attitude intensity.

## 5. Source Material Acquisition

The skill must work from any of these inputs, in priority order:

1. **Explicit file input:** a session handoff or session recap `.md` (downsample it; this is the cleanest source).
2. **Named past conversation (claude.ai context):** use conversation search / recent chats tools to retrieve the thread.
3. **The current thread's own stale head:** the conversation being resumed is the one being recapped.
4. **Pasted transcript or raw notes.**

If source material is thin or ambiguous ("that thing we decided"), ask one clarifying question rather than fabricating. **Fabrication rule:** the narrative shaping may exaggerate tone, never facts. Every event, decision, and open loop in the recap must be traceable to the source. Comic distortion of framing: yes. Invented plot points: never. This is a recap, not fiction about the operator's life.

## 6. The Interview

Short, warm, in-character-for-the-skill (the skill's own host voice can have personality; think a premiere-night announcer, not a settings menu).

1. Identify the thread being revived (skip if obvious/stated).
2. Offer 3-4 register suggestions as a tappable/selectable list:
   - 1-2 **past favorites** (registers the operator has used and liked; consult usage history if available -- Open Brain search on prior Previously On captures, or in-skill history file in Claude Code contexts).
   - 1-2 **rotation picks** (registers untried or not used recently; deliberately surface variety).
   - Always allow free-text ("or name any register / mashup").
3. If the thread is emotionally heavy (grief, conflict, spiritual matter), bias suggestions away from roast-native registers and toward documentary, novella, or amblin-wonder. Do not Seinfeld a funeral.

## 7. Output Contract (Register-Independent)

Every Previously On, in every register, at every tier, contains exactly three parts:

1. **Title card.** Two lines, always:
   - `PREVIOUSLY ON: "<INVENTED EPISODE TITLE>"` -- the episode title is original, evocative, drawn from the thread's content.
   - Attribution line, italicized: `*A story recap in the <register-slug> register -- inspired by <source>.*` Registers with real-show DNA name the show ("inspired by Seinfeld", "inspired by Curb Your Enthusiasm"); pure genre registers name the tradition ("inspired by the war novella tradition", "inspired by classic Westerns"). The user always knows what lens they are looking through. Each catalog entry defines its `inspired-by` string.
2. **The recap body.** Register-native narrative. Chronological arc of the thread: how it started, how it progressed, the insights, the turns, the decisions. Attitude per register. May include register-appropriate framing devices (cold open, narrator, field report header, case file stamp).
3. **WHERE WE LEFT OFF.** Mandatory closing block, present in every register. Surfaces every open loop as a cliffhanger, in scannable form (short lines, not buried in prose). This is the functional payload; the body earns the reader's attention, this block aims it. May be register-flavored but must remain literal enough to act on. Optionally followed by 1-2 "season two questions" -- alternate angles or reframes the operator hasn't considered.

**Low-fidelity inclusion contract** (what MUST survive compression): the arc, every decision made, every insight worth keeping, every open loop, the emotional register of the original conversation.

**Deliberate exclusions** (what MUST be dropped): YAML, IDs, file paths, exact configs, schema, command syntax, metadata. If the operator needs those, close with the pointer line: *"For working state, see the session handoff."*

## 8. Register Catalog v0-1

Registers are style contracts. Each entry: **slug | DNA | narrative contract | native attitude**. The built skill should store this catalog in `references/register-catalog.md` with, per register: one short exemplar opening line (written original, not quoted from any source) and its `inspired-by` attribution string for the title card (Section 7). The catalog preamble carries the constitution doctrine (vision doc Section 7): Catholic moral spine, invisible, never preached, plainly owned if asked. No Star Trek register.

### Literary family

| Slug | DNA | Narrative contract | Native attitude |
|------|-----|-------------------|----------------|
| `novella` | Literary fiction | Interior, patient, image-driven; the thread as a short story with a quiet turn | Compassionate, unsparing |
| `romance` | Romance fiction | Longing, obstacles, timing; open loops as will-they-won't-they | Warm, swooning, gently teasing |
| `war-novella` | War fiction (operator's beloved genre; flagship) | Field report cadence, unit loyalty, cost accounting; decisions as orders, open loops as unsecured ground | Grave, terse, zero sentimentality; does not care about feelings, there is a war on |
| `western` | Western fiction/film | Frontier morality, laconic narration, the stranger and the town; open loops as unfinished business at sundown | Dry, laconic, quietly judging |
| `spy-thriller` | CIA/espionage fiction | Case file framing, tradecraft language, asset/handler dynamics; open loops as active operations | Paranoid, clinical, redacted humor |
| `mystery-noir` | Detective fiction | The thread as a case; clues, red herrings, the reveal; open loops as unsolved counts | World-weary, wry |
| `sci-fi` | General SF | Ideas-forward, extrapolative; the thread's stakes projected to their logical extreme | Curious, slightly ominous |
| `fantasy` | General fantasy | Wonder register, quest logic, named artifacts | Earnest, mythic |
| `documentary` | Non-fiction documentary | Sober narrator, talking-head asides, archival framing; the most literal register in the catalog | Neutral, occasionally deadpan |

### Comedy family

| Slug | DNA | Narrative contract | Native attitude |
|------|-----|-------------------|----------------|
| `cringe-verite` | Curb-style improvised cringe comedy | Pettiness spirals, social-contract violations litigated at length, escalation from trivial premise | Roasts the protagonist as fully complicit |
| `standup-observational` | Seinfeld-style standup + scenes | Comedian framing device bookends scenes; "who DOES that" interrogation of behavior; callbacks mandatory | Roasts everyone, protagonist first. **Gold-standard calibration register** |
| `office-mockumentary` | The Office-style mockumentary | Talking-head confessionals, camera-catch moments, painful sincerity under the comedy | Roasts with underlying affection |
| `farce-70s` | Three's Company-style farce | One misunderstanding load-bearing for the whole episode; doorbell timing; everything resolves and nothing is learned | Silly, innocent, zero malice |
| `living-room-70s` | All in the Family-style sitcom | Two entrenched worldviews argue in one room; the argument IS the plot; uncomfortable truths land inside jokes | Provocative, humane underneath |
| `comedy-movie` | Broad film comedy | Set pieces, escalation, a third-act run | Playful, big |

### Cinematic/franchise-flavored family (registers, never fan fiction)

| Slug | DNA | Narrative contract | Native attitude |
|------|-----|-------------------|----------------|
| `simulation-noir` | Matrix-flavored cyberpunk | Reality-questioning frame; the mundane thread revealed as signal in the system; choices as red/blue forks | Cool, portentous, leather-jacket solemn |
| `street-chronicle-90s` | The world of 90s hip-hop (stories from that world, not real persons) | Block-level loyalty, rise-and-rivalry arcs, spoken-word narration cadence | Unflinching, loyal, elegiac |
| `amblin-wonder` | ET-flavored 80s suburban wonder | Ordinary kid-height perspective on extraordinary events; bikes, cul-de-sacs, flashlights; awe over irony | Tender, wide-eyed |
| `epic-quest` | LOTR-flavored high fantasy | Fellowship framing, burdens carried, maps and long roads; open loops as roads yet untraveled | Solemn, loyal, occasionally merry |
| `dark-vigilante` | Batman-register noir | Night city, obsession, the case as personal wound; justice vs. vengeance undertow | Brooding, relentless |
| `golden-age-hero` | Superman-register heroism | Bright, hopeful, principled; the thread's best version of everyone | Flattering, sincere, zero irony |
| `fourth-wall-antihero` | Deadpool-register irreverence | Breaks the recap's own frame, mocks the skill itself, footnotes its own jokes | Roasts protagonist, author, AND the format |
| `everyman-hero` | Spider-Man-register | Great-power-great-responsibility framing on small choices; quips under pressure; the hero is broke and late | Self-deprecating, warm |
| `space-opera` | Star Wars-register | Opening crawl framing device permitted; empires and rebellions mapped onto the thread's factions; lightsabers not included | Grand, mythic, a little pulpy |

**Extensibility rule:** new registers are added by appending a catalog entry (slug, DNA, contract, attitude, exemplar line) and bumping the skill MINOR version. Mashups ("war-novella x mockumentary") are permitted at generation time without catalog entries.

## 9. Saved-Output Filename

Default delivery is **in-chat, ephemeral** -- this is entertainment, not archive. On explicit save request, follow the Output Artifact Filename Convention in `nc3-meta-conventions-skill-v0-2`:

```
{YYYY}-{MM}-{DD}_{Topic_Words}-{register-slug}-{tier}_conversation-recap.md
```

Suffix: `conversation-recap` (human-readable hyphenated form, one per skill; distinct at a glance from the structured recap's `session-recap` suffix). Example:
`2026-07-17_The_Command-standup-observational-medium_conversation-recap.md`

## 10. SKILL.md Requirements for the Build

1. YAML frontmatter: `name: conversation-recap`, `version: 0.1.0`, and `description`. **Description under 1024 characters** (validator-enforced). Draft description below (verify length before packaging):

> Generate low-fidelity NARRATIVE conversation recaps ("Previously On..." format) that re-immerse the operator in a stale conversation or project thread -- narrative arc, insights, and open loops as cliffhangers, at minimal cognitive cost. Trigger on: 'previously on', 'catch me up', 'recap me in', 'what did I miss', 'reimmerse me', 'season recap this thread', 'where did we leave off with [topic]', 'Seinfeld me', 'war novella recap', or any request for an entertaining low-fidelity recap in a named register. Runs a short mood interview (register + tier: teaser/cold-open/season-recap), then generates per the register catalog. NOT for machine-readable state (use session-handoff) or structured summaries (use nc3-session-recap-skill).

2. Version history table.
3. Dual Help section (operator-primary; this is an action skill).
4. File structure: `SKILL.md` + `references/register-catalog.md`. No scripts needed. Thin-router `modes/` pattern NOT needed at v0-1 (registers are data, not modes; one generation pipeline).
5. Reference, do not restate, the conventions skill for naming/filename rules.
6. Embed the fabrication rule (Section 5), the output contract (Section 7), the roast doctrine, and the judgment-call doctrine as non-negotiables in the agent Help section.

## 11. Test Plan

1. Regenerate the Richard thread recap in `war-novella` (Short) and `documentary` (Medium) from this spec alone; compare against the two ratified test runs for contract compliance (title card, arc, WHERE WE LEFT OFF, no fabricated facts).
2. Verify tier word budgets hit within +/-15%.
3. Run one emotionally-heavy-thread simulation and confirm the interview biases away from roast-native registers.
4. Package with `/mnt/skills/examples/skill-creator/scripts/package_skill.py`; confirm description length passes.

## 12. Open Decisions for Operator Ratification

1. ~~Skill name~~ RESOLVED 2026-07-17 (final): `conversation-recap`, `version: 0.1.0` in frontmatter, with "Previously On" as output brand only. Naming history and the two-generation ecosystem finding are recorded in the vision doc, Section 10.
2. Usage-history mechanism for "past favorites" in the interview: Open Brain captures vs. local history file vs. none at v0-1 (recommend: none at v0-1; add at v0-2 once field patterns emerge).
3. Whether Previously On outputs should ever auto-offer a Wellhead capture (recommend: no; entertainment artifacts pollute the brain; capture the *decisions* from the underlying thread instead).
