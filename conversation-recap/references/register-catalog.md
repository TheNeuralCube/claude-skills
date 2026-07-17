<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# conversation-recap Register Catalog (v0-1)

This catalog is the style-contract library the generation pipeline reads at runtime. It holds all 24 registers as data. Per register it defines six fields: DNA, narrative contract, native attitude, the inspired-by attribution string printed in the title card, the touchstone (a picker recognition aid only), and one original exemplar opening line. Read the register's fields here before generating; the title card must reproduce the register's inspired-by string verbatim.

## Preamble: the doctrines that govern this catalog

**Constitution doctrine.** All registers share an invisible moral spine: a Catholic worldview governing what the stories value, that is fidelity, repentance, mercy, the dignity of persons, and consequences that mean something. This is the author's perspective, not the story's sermon. It is never announced, never evangelized in-text, and never visible unless the operator or an audience member asks where the stories come from. If asked, the answer is given plainly.

**Register-integrity law.** Registers are stylistic DNA, not licensed characters. Each register captures the narrative machinery of its inspiration using original characters, original dialogue, and the operator's own life as material. No lifted characters, no lifted lines, no reproduced IP, ever. This is a house style library owned by the operator, not a costume rack borrowed from studios. The inspired-by string names the lens the reader is looking through; it never licenses lifting a character or a line. The touchstone is a recognition aid for the operator at pick time only; it is never something to reproduce.

**Explicit exclusion.** No Star Trek register.

**Extensibility rule.** New registers are added by appending a catalog entry, that is slug, DNA, narrative contract, native attitude, inspired-by string, touchstone, and one original exemplar line, and bumping the skill MINOR version. Mashups ("war-novella x mockumentary") are permitted at generation time without a catalog entry.

**Style law.** Exemplar lines and all catalog prose contain no em dashes and no en dashes. Hyphens and commas only.

**Field reference.** The tables below carry five of the six fields per register (slug, DNA, narrative contract, native attitude, inspired-by, touchstone). The sixth field, the original exemplar opening line, is listed under each family table. Tables A, B, and C hold the inspired-by strings; Table D holds the touchstone strings.

---

## Literary family

Table A holds the inspired-by strings for this family (pure genre names the tradition; the documentary names the tradition). Table D holds the touchstones.

| Slug | DNA | Narrative contract | Native attitude | Inspired-by (Table A) | Touchstone (Table D) |
|------|-----|-------------------|-----------------|-----------------------|----------------------|
| `novella` | Literary fiction | Interior, patient, image-driven; the thread as a short story with a quiet turn | Compassionate, unsparing | inspired by the literary fiction tradition | Literary short fiction, the quiet-turn story |
| `romance` | Romance fiction | Longing, obstacles, timing; open loops as will-they-won't-they | Warm, swooning, gently teasing | inspired by the romance tradition | The sweeping romance novel |
| `war-novella` | War fiction (operator's beloved genre; flagship) | Field report cadence, unit loyalty, cost accounting; decisions as orders, open loops as unsecured ground | Grave, terse, zero sentimentality; does not care about feelings, there is a war on | inspired by the war novella tradition | The literary war novel |
| `western` | Western fiction and film | Frontier morality, laconic narration, the stranger and the town; open loops as unfinished business at sundown | Dry, laconic, quietly judging | inspired by classic Westerns | The classic frontier Western |
| `spy-thriller` | CIA and espionage fiction | Case file framing, tradecraft language, asset and handler dynamics; open loops as active operations | Paranoid, clinical, redacted humor | inspired by the espionage fiction tradition | Cold War tradecraft espionage |
| `mystery-noir` | Detective fiction | The thread as a case; clues, red herrings, the reveal; open loops as unsolved counts | World-weary, wry | inspired by the detective noir tradition | Hardboiled detective noir |
| `sci-fi` | General science fiction | Ideas-forward, extrapolative; the thread's stakes projected to their logical extreme | Curious, slightly ominous | inspired by the science fiction tradition | Idea-driven science fiction |
| `fantasy` | General fantasy | Wonder register, quest logic, named artifacts | Earnest, mythic | inspired by the fantasy tradition | Mythic high fantasy |
| `documentary` | Non-fiction documentary | Sober narrator, talking-head asides, archival framing; the most literal register in the catalog | Neutral, occasionally deadpan | inspired by the documentary tradition | The sober long-form documentary |

**Exemplar opening lines (Literary family):**

- `novella`: The kettle had gone cold again, and she noticed it the way you notice a thing you have been avoiding. Outside, the morning did what mornings do, indifferent and on time.
- `romance`: He had rehearsed the sentence for a week, and now, with her finally in front of him, every word of it left the room. She waited, one eyebrow raised, enjoying this far too much.
- `war-novella`: The order came down at dawn and nobody argued it. We took the ground we were told to take, we counted what it cost, and then we did not talk about the counting.
- `western`: The stranger rode in a little after noon and the town went quiet the way a town does when it already knows how this ends. He tied off his horse and did not look at anyone. He did not have to.
- `spy-thriller`: The asset made contact on schedule, which was the first thing that felt wrong. Everything after that was worse, and most of it is above your clearance.
- `mystery-noir`: She walked into the office with a problem and a good coat, and I could tell the coat was going to outlast the problem. They usually do.
- `sci-fi`: The machine answered the question correctly, which was expected. Then it answered the question we had not asked yet, which was not.
- `fantasy`: They say the road out of the valley forgets your name the moment you take it, and gives it back only when you return changed. Few return. Fewer return changed.
- `documentary`: What follows is a reconstruction, assembled from the available record. The participants remember it differently, which is itself part of the record.

---

## Comedy family

Table B holds the inspired-by strings for this family (real-show DNA names the show; broad film comedy names the tradition). Table D holds the touchstones.

| Slug | DNA | Narrative contract | Native attitude | Inspired-by (Table B) | Touchstone (Table D) |
|------|-----|-------------------|-----------------|-----------------------|----------------------|
| `cringe-verite` | Curb-style improvised cringe comedy | Pettiness spirals, social-contract violations litigated at length, escalation from a trivial premise | Roasts the protagonist as fully complicit | inspired by Curb Your Enthusiasm | Curb Your Enthusiasm, the grievance spiral |
| `standup-observational` | Seinfeld-style standup plus scenes | Comedian framing device bookends scenes; "who DOES that" interrogation of behavior; callbacks mandatory | Roasts everyone, protagonist first. Gold-standard calibration register | inspired by Seinfeld | Seinfeld, the "who does that" bit |
| `office-mockumentary` | The Office-style mockumentary | Talking-head confessionals, camera-catch moments, painful sincerity under the comedy | Roasts with underlying affection | inspired by The Office | The Office, the talking-head confessional |
| `farce-70s` | Three's Company-style farce | One misunderstanding load-bearing for the whole episode; doorbell timing; everything resolves and nothing is learned | Silly, innocent, zero malice | inspired by Three's Company | Three's Company, the load-bearing mix-up |
| `living-room-70s` | All in the Family-style sitcom | Two entrenched worldviews argue in one room; the argument IS the plot; uncomfortable truths land inside jokes | Provocative, humane underneath | inspired by All in the Family | All in the Family, the armchair argument |
| `comedy-movie` | Broad film comedy | Set pieces, escalation, a third-act run | Playful, big | inspired by the broad film comedy tradition | Broad studio comedy, the third-act runaround |

**Exemplar opening lines (Comedy family):**

- `cringe-verite`: It began, as these things do, over a parking space that technically belonged to no one. By the end of the week it had cost him two friendships and the respect of a valet.
- `standup-observational`: So here is a guy, a grown adult, who reorganizes the entire plan and then acts surprised that the plan changed. Who does that? This guy. Every time.
- `office-mockumentary`: He said the meeting could have been an email, then scheduled a second meeting to explain the first one. Later, to the camera, he called this "leadership."
- `farce-70s`: The whole disaster hinged on a single overheard sentence, taken exactly the wrong way, by exactly the wrong person, at exactly the moment the doorbell rang.
- `living-room-70s`: There were two chairs, two opinions, and absolutely no chance either man was getting up before he had won. The argument was the evening. It always was.
- `comedy-movie`: It was supposed to be a simple errand. Ninety minutes later there was a marching band involved, and nobody could say exactly how.

---

## Cinematic and franchise-flavored family (registers, never fan fiction)

Table C holds the inspired-by strings for this family (the tradition or milieu is named, not the franchise, per the register-integrity law). Table D holds the touchstones (the recognizable franchise is named here as a picker aid only, never to be reproduced).

| Slug | DNA | Narrative contract | Native attitude | Inspired-by (Table C) | Touchstone (Table D) |
|------|-----|-------------------|-----------------|-----------------------|----------------------|
| `simulation-noir` | Matrix-flavored cyberpunk | Reality-questioning frame; the mundane thread revealed as signal in the system; choices as red and blue forks | Cool, portentous, leather-jacket solemn | inspired by the cyberpunk tradition | The Matrix, the red-pill reveal |
| `street-chronicle-90s` | The world of 90s hip-hop (stories from that world, not real persons) | Block-level loyalty, rise-and-rivalry arcs, spoken-word narration cadence | Unflinching, loyal, elegiac | inspired by the world of 90s hip-hop | 90s hip-hop cinema, the block-loyalty saga |
| `amblin-wonder` | ET-flavored 80s suburban wonder | Ordinary kid-height perspective on extraordinary events; bikes, cul-de-sacs, flashlights; awe over irony | Tender, wide-eyed | inspired by the 80s suburban wonder tradition | E.T. and Amblin, kid-height awe |
| `epic-quest` | LOTR-flavored high fantasy | Fellowship framing, burdens carried, maps and long roads; open loops as roads yet untraveled | Solemn, loyal, occasionally merry | inspired by the high fantasy quest tradition | The Lord of the Rings, the fellowship road |
| `dark-vigilante` | Batman-register noir | Night city, obsession, the case as personal wound; justice versus vengeance undertow | Brooding, relentless | inspired by the caped-vigilante noir tradition | Batman, the brooding night-city detective |
| `golden-age-hero` | Superman-register heroism | Bright, hopeful, principled; the thread's best version of everyone | Flattering, sincere, zero irony | inspired by the golden-age superhero tradition | Superman, the bright and principled hero |
| `fourth-wall-antihero` | Deadpool-register irreverence | Breaks the recap's own frame, mocks the skill itself, footnotes its own jokes | Roasts protagonist, author, AND the format | inspired by the fourth-wall-breaking antihero tradition | Deadpool, the self-mocking narrator |
| `everyman-hero` | Spider-Man-register | Great-power-great-responsibility framing on small choices; quips under pressure; the hero is broke and late | Self-deprecating, warm | inspired by the everyman superhero tradition | Spider-Man, great power and broke and late |
| `space-opera` | Star Wars-register | Opening-crawl framing device permitted; empires and rebellions mapped onto the thread's factions; lightsabers not included | Grand, mythic, a little pulpy | inspired by the space opera tradition | Star Wars, the opening-crawl saga |

**Exemplar opening lines (Cinematic and franchise-flavored family):**

- `simulation-noir`: You have felt it your whole working life, the small wrongness in the ordinary, the sense that the schedule is a story someone tells you. Today the story blinks.
- `street-chronicle-90s`: This is for the block that raised him and the corner that watched him leave. Remember the names. The city already forgot half of them, and it should not have.
- `amblin-wonder`: The porch lights were coming on one by one down the whole street, and none of the grown-ups knew yet that the ordinary night had already ended. The kids knew. The kids always know first.
- `epic-quest`: The company set out with light hearts and heavy packs, and only one of them understood how far the road truly went. He said nothing, and shouldered a little more of the load.
- `dark-vigilante`: The city does not sleep so much as wait. He works the hours it fears most, chasing a single question down every wet alley until it finally turns and answers him.
- `golden-age-hero`: There is a version of every person that shows up when it counts, does the right thing without being asked, and never mentions it after. This is the story of that version.
- `fourth-wall-antihero`: Oh good, a recap. Because nothing says "thriving" like needing a previously-on to understand your own week. Buckle up, I get paid by the aside.
- `everyman-hero`: Rent was due, the bus was early for once in its life, and of course that was the exact morning the whole thing decided to fall apart. Typical. Let us go.
- `space-opera`: In a time of fragile alliances and long silences between the stars, one small decision was about to matter far more than the people making it could possibly know.
