<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# conversation-recap

A narrative recap skill that re-immerses you in a stale conversation or project thread instead of re-briefing you on it. It applies the television "Previously On" treatment to one of your own threads: a short, narratively shaped, emotionally loaded compression that restores the feel of the conversation and surfaces every open loop as a cliffhanger.

The bottleneck on returning to a cold thread is rarely missing state. It is missing appetite. A session handoff gives you the state; this gives you back the wanting.

- **License:** Apache 2.0 (SPDX headers on repo wrapper files; generated recaps carry none).
- **Skill version:** 0.1.1, declared in the SKILL.md frontmatter.
- **Brand vs. name:** the functional skill name is `conversation-recap` so agents discover it by purpose. "Previously On" is the product brand and appears only in the output title card and the trigger phrases.

## Where it sits on the fidelity ladder

Three rungs restore three different things. Only the bottom rung restores appetite.

| Rung | Carries | Reader |
|---|---|---|
| `session-handoff` (in this repo) | full working state under a YAML contract | a resuming agent |
| a structured-summary skill (not in this repo) | an agent-consumable digest | an agent |
| `conversation-recap` | the arc, the feeling, the open loops | you |

This skill is deliberately not a state carrier. YAML, IDs, file paths, configs, schema, and command syntax are contractually excluded from its output. When you need those, it points you back to the handoff rather than pretending to carry them.

## What it does

1. **TRIGGER.** You invoke with a trigger phrase.
2. **SOURCE.** It acquires source material: an explicit handoff file, a named past conversation, the current thread's stale head, or a pasted transcript.
3. **INTERVIEW.** A short mood interview in a premiere-night host voice offers 3 to 4 register picks, always allowing free text.
4. **TIER CALL.** It judges the length tier, states the call in one line, and proceeds. You override by exception.
5. **GENERATE.** It writes the recap in the chosen register, reading that register's fields from `references/register-catalog.md`.
6. **DEBRIEF.** A one-line check that length and register landed, plus an offer to re-cut.
7. **OPTIONAL SAVE.** Only if you ask. Output is ephemeral by default.

When you specify the register or tier at invocation ("Seinfeld me on the Richard thread, medium"), the interview collapses to whatever you left unspecified.

## Tiers

Tier is a length and immersion contract measured in reading time at about 230 words per minute.

| Tier | Name | Reading time | Words | Use |
|---|---|---|---|---|
| Short | The Teaser | 60 to 90 sec | 200 to 350 | threads you half-remember; open loops only |
| Medium | The Cold Open | 2 to 3 min | 600 to 900 | the default: full arc, native attitude, all open loops |
| Long | The Season Recap | 4 to 6 min | 1100 to 1600 | sagas: multiple plotlines, high stakes, long gap |

## Registers

24 registers ship in `references/register-catalog.md` across three families:

- **Literary:** `novella`, `war-novella`, `documentary`, `mystery-noir`, `romance`, `western`, and siblings.
- **Comedy:** `standup-observational`, `office-mockumentary`, `cringe-verite`, `farce-70s`, `living-room-70s`, `comedy-movie`, and siblings.
- **Cinematic and franchise-flavored:** `simulation-noir`, `space-opera`, `spy-thriller`, `dark-vigilante`, `epic-quest`, `golden-age-hero`, and siblings.

Each register is defined as data across six fields: DNA, narrative contract, native attitude, the inspired-by attribution string, a touchstone used only as a picker recognition aid, and one original exemplar line. Mashups are permitted at generation time without a catalog entry.

## The rules that keep it honest

These are the load-bearing constraints. They are why the skill is safe to point at your real life.

- **Fabrication rule.** Narrative shaping may exaggerate tone, never facts. Every event, decision, and open loop must be traceable to the source. Invented plot points are never allowed.
- **Interiority clause.** Attributed motives are permitted only as the narrator's openly-marked read of recorded behavior. A visible inference is allowed; an asserted inner state about another person is a fabrication however tonal it reads.
- **Register-integrity law.** Registers are style DNA with original characters and original dialogue, using your life as the material. No lifted IP characters, no lifted lines, ever. The inspired-by string names the lens; it never licenses lifting.
- **Thin-source rule.** When the source cannot fill the called tier without invention, the skill drops to the tier the source supports rather than padding. The fabrication rule outranks the tier budget, always.
- **Emotionally-heavy-thread bias.** On grief, conflict, or a spiritual matter, suggestions bias away from roast-native registers and toward `documentary`, `novella`, or `suburban-wonder`. Do not Seinfeld a funeral. The bias governs what is suggested, never what is permitted.
- **Style law.** No em dashes and no en dashes anywhere, including inside generated recaps, titles, and attribution lines.

## Output contract

Every recap, in every register, at every tier, has exactly three parts:

1. **Title card.** `PREVIOUSLY ON: "<INVENTED EPISODE TITLE>"` plus an italicized attribution line reading the register's inspired-by string verbatim.
2. **The recap body.** Register-native narrative carrying the chronological arc: how it started, how it progressed, the insights, the turns, the decisions.
3. **WHERE WE LEFT OFF.** A mandatory closing block surfacing every open loop as a scannable cliffhanger. The body earns attention; this block aims it.

## Files

```
conversation-recap/
  SKILL.md                        trigger logic, pipeline, tier logic, output contract, doctrines
  references/
    register-catalog.md           all 24 registers as data; read at generation time
```

## Output filenames

Saved only on explicit request. Pattern:

```
{YYYY}-{MM}-{DD}_{Topic_Words}-{register-slug}-{tier}_conversation-recap.md
```

Example: `2026-07-17_The_Command-standup-observational-medium_conversation-recap.md`
