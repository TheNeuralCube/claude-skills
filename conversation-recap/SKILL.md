---
name: conversation-recap
version: 0.1.0
description: Generate low-fidelity NARRATIVE conversation recaps ("Previously On..." format) that re-immerse the operator in a stale conversation or project thread: narrative arc, insights, and open loops as cliffhangers, at minimal cognitive cost. Trigger on: 'previously on', 'catch me up', 'recap me in', 'what did I miss', 'reimmerse me', 'season recap this thread', 'where did we leave off with [topic]', 'Seinfeld me', 'war novella recap', or any request for an entertaining low-fidelity recap in a named register. Runs a short mood interview (register + tier: teaser/cold-open/season-recap), then generates per the register catalog. NOT for machine-readable state (use session-handoff) or structured summaries (use nc3-session-recap-skill).
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# conversation-recap (v0.1.0)

This skill is the low-fidelity, narrative bottom rung of the continuity fidelity ladder. Its two ladder siblings restore machine state: `session-handoff` carries full state under a YAML contract, and `nc3-session-recap-skill` carries a structured, agent-consumable summary. This skill restores something they do not: the operator's appetite and orientation, delivered as a story. The functional skill name is `conversation-recap` so agents discover it by purpose; "Previously On" is the product brand and appears only in the output title card and the trigger phrases. The siblings restore state; this one restores the operator's appetite to resume. State is what the thread contained; appetite is whether the operator wants back in.

## When to use this skill

Reach for this skill when the operator has been away from a conversation or project thread and needs to be re-immersed, not re-briefed. The bottleneck on return is rarely missing state; it is missing enthusiasm. A "Previously On" restores the feeling of the thread, its arc, and its open cliffhangers, so the operator wants back in.

Trigger phrases: "previously on", "catch me up", "recap me in [register]", "what did I miss", "reimmerse me", "season recap this thread", "where did we leave off with [topic]", "Seinfeld me", "war novella recap", or any request for an entertaining low-fidelity recap in a named register.

This skill is NOT for:
- Machine-readable working state (decisions, file paths, schema, configs). Route to `session-handoff`.
- Structured, agent-consumable summaries. Route to `nc3-session-recap-skill`.
- Reflective personal records. Route to `per-jrn-journal-entry`.

If the operator needs any of those, name the right skill and stop; do not smuggle machine state into a narrative recap.

## Execution flow

Run this seven-step pipeline in order:

1. **TRIGGER.** The operator invokes with a trigger phrase (see above).
2. **SOURCE.** Acquire source material per "Source material acquisition" below.
3. **INTERVIEW.** Run the mood interview per "The interview" below; a register is selected.
4. **TIER CALL.** Judge the tier per "Tier logic" below; state the call in one line; the operator may override.
5. **GENERATE.** Produce the recap against the output contract in the chosen register, reading the register's fields and inspired-by string from `references/register-catalog.md`.
6. **DEBRIEF.** One-line check that length and register landed; offer a re-cut if not.
7. **OPTIONAL SAVE.** Only on explicit request; filename per "Saving output" below.

**Collapse rule.** When the operator specifies the register and/or the tier at invocation ("Seinfeld me on the Richard thread, medium"), skip the interview for what was specified and interview only for what is unspecified. Respect explicit parameters; never re-ask for what the operator already gave.

## Source material acquisition

Work from any of these inputs, in priority order:

1. **Explicit file input.** A session handoff or session recap `.md`. Downsample it; this is the cleanest source.
2. **Named past conversation.** Use conversation search or recent-chats retrieval to pull the named thread.
3. **The current thread's stale head.** The conversation being resumed is the one being recapped.
4. **Pasted transcript or raw notes.**

If the source is thin or ambiguous ("that thing we decided"), ask ONE clarifying question rather than filling the gap yourself.

**Fabrication rule:** the narrative shaping may exaggerate tone, never facts. Every event, decision, and open loop in the recap must be traceable to the source. Comic distortion of framing is allowed. Invented plot points are never allowed. This is a recap, not fiction about the operator's life.

## The interview

Short, warm, in the skill's own host voice: a premiere-night announcer, not a settings menu. The host voice may have personality; keep it brief.

1. **Identify the thread** being revived. Skip if it is obvious or already stated.
2. **Offer 3 to 4 register picks** as a selectable list:
   - 1 to 2 **past favorites** (registers the operator has used and liked). At v0.1.0 there is no usage-history store, so past-favorites is empty; degrade gracefully to rotation-only picks. Do not claim a favorite the operator never chose.
   - 1 to 2 **rotation picks** (registers untried or not used recently; surface variety deliberately).
   - Always allow free-text: "or name any register, or a mashup."
3. **Emotionally-heavy-thread bias.** If the thread is emotionally heavy (grief, conflict, a spiritual matter), bias the suggestions AWAY from roast-native registers (`cringe-verite`, `standup-observational`, `fourth-wall-antihero`) and TOWARD `documentary`, `novella`, or `amblin-wonder`. Do not Seinfeld a funeral. The operator may still override to any register; the bias governs what you suggest, not what you permit.

## Tier logic

Tier is a length and immersion contract measured in reading time (about 230 words per minute, silent reading).

| Tier | Name | Reading time | Word budget | Contract |
|------|------|-------------|------------|----------|
| Short | The Teaser | 60 to 90 sec | 200 to 350 | Pure hook. Open loops only, minimal arc. For threads the operator half-remembers. |
| Medium | The Cold Open | 2 to 3 min | 600 to 900 | Full arc plus native attitude plus all open loops. The default. |
| Long | The Season Recap | 4 to 6 min | 1100 to 1600 | Immersive, multi-thread, act structure. Reserved for sagas: multiple plotlines, high stakes, long gap since last contact. |

**Judgment-call doctrine.** Pick the tier from story complexity, number of open threads, stakes, and time elapsed. State the call in one line ("One plotline, low stakes, high comedy density: calling it a Medium") and proceed. The operator overrides by exception. The same doctrine extends to structure, framing device, and intensity within a register: you decide, the operator tweaks.

**Calibration anchor.** The 2026-07-17 Seinfeld-register run "The Command" (about 900 words) is the ratified gold standard for Medium feel and native-attitude intensity. Calibrate Medium output against it.

## Output contract

Every "Previously On", in every register, at every tier, contains exactly three parts. This contract is non-negotiable.

**1. Title card.** Two lines, always:
- `PREVIOUSLY ON: "<INVENTED EPISODE TITLE>"` The episode title is original, evocative, and drawn from the thread's content.
- The attribution line, italicized: `*A story recap in the <register-slug> register, inspired by <source>.*` The `<source>` string is read verbatim from the register's catalog entry, never improvised.

**2. The recap body.** Register-native narrative. Give the chronological arc of the thread: how it started, how it progressed, the insights, the turns, the decisions. Carry the native attitude of the chosen register. Register-appropriate framing devices are allowed (cold open, narrator, field-report header, case-file stamp).

**3. WHERE WE LEFT OFF.** Mandatory closing block, present in every register at every tier. Surface every open loop as a scannable short-line cliffhanger, not buried in prose. This is the functional payload: the body earns attention, this block aims it. It may be register-flavored but must stay literal enough to act on. Optionally follow with 1 to 2 "season two questions": alternate angles or reframes the operator has not considered.

**Low-fidelity inclusion contract (what MUST survive compression):** the arc, every decision made, every insight worth keeping, every open loop, and the emotional register of the original conversation.

**Deliberate exclusions (what MUST be dropped):** YAML, IDs, file paths, exact configs, schema, command syntax, metadata. If the operator needs those, close with the pointer line: *"For working state, see the session handoff."*

## Debrief and re-cut

After delivery, run a one-line check that the length and register landed. If they did not, offer a re-cut in another register or another tier. Keep the offer to one line; do not re-run the full interview unless the operator asks.

## Saving output

Default delivery is in-chat and ephemeral. This is entertainment, not archive; do not save unless asked.

On an explicit save request only, name the file per the Output Artifact Filename Convention in `nc3-meta-conventions-skill-v0-2` (referenced, not restated here):

```
{YYYY}-{MM}-{DD}_{Topic_Words}-{register-slug}-{tier}_conversation-recap.md
```

Suffix: `conversation-recap`. Example: `2026-07-17_The_Command-standup-observational-medium_conversation-recap.md`.

## Version history

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | 2026-07-17 | Initial build per 2026-07-17 design spec. |

## Help

### For the Operator

A "Previously On" is the television recap treatment applied to one of your own stale threads: a short, narratively shaped, emotionally loaded compression that restores the feeling of the conversation and surfaces the open cliffhangers. It is the appetite fix, not the state fix.

Reach for it when you have been away from a thread and coming back feels like homework. A session handoff gives you the state; this gives you back the wanting.

How to steer it:
- **Name a register** ("Seinfeld me", "war novella recap") and you get that lens.
- **Name a tier** (teaser, cold-open, season-recap) and you set the length.
- **Say nothing and let it choose.** It will interview you briefly for a register, judge the tier, state its call in one line, and proceed. Override anything by exception.

It is entertainment and ephemeral by default: nothing is saved unless you ask. When you need real working state (files, configs, schema), it points you back to the session handoff rather than pretending to carry it.

### For the Agent

Protocol instructions. The following are non-negotiable and carry into every generated string.

**Fabrication rule (verbatim):**

> Fabrication rule: the narrative shaping may exaggerate tone, never facts. Every event, decision, and open loop in the recap must be traceable to the source. Comic distortion of framing is allowed. Invented plot points are never allowed. This is a recap, not fiction about the operator's life.

**Output contract.** Every recap carries all three parts: the title card (`PREVIOUSLY ON` plus the italicized inspired-by attribution line), the register-native body, and the mandatory `WHERE WE LEFT OFF` block. The `WHERE WE LEFT OFF` block appears in every register at every tier without exception.

**Roast doctrine.** Native attitude per register; there is no global roast dial. Choosing the register IS choosing the treatment. Roast-native registers roast (the operator has authorized full native intensity); flatterers flatter; the war novella does not care about anyone's feelings because there is a war on. Do not soften a roast register or sharpen a gentle one; run the register as written in the catalog.

**Judgment-call doctrine.** You pick the tier and the structure from complexity, open-thread count, stakes, and elapsed time. State the call in one line and proceed. The operator overrides by exception.

**Register integrity rule.** Registers are style DNA with original characters and original dialogue, using the operator's own life as material. No lifted IP characters, no lifted lines, no reproduced IP, ever. The inspired-by attribution names the source lens; it never licenses lifting a character or a line. The touchstone in the catalog is a picker recognition aid only, never something to reproduce.

**Emotionally-heavy-thread bias.** When the thread is emotionally heavy (grief, conflict, a spiritual matter), bias interview suggestions away from roast-native registers (`cringe-verite`, `standup-observational`, `fourth-wall-antihero`) and toward `documentary`, `novella`, or `amblin-wonder`. Do not Seinfeld a funeral. The bias governs suggestions; the operator may still override to any register.

**Style law.** No em dashes and no en dashes anywhere, including inside generated recaps, titles, and attribution lines. Hyphens and commas only.

**Related skills:** `session-handoff` (machine state), `nc3-session-recap-skill` (structured summary), `nc3-meta-conventions-skill-v0-2` (naming, versioning, and filename conventions; referenced, not restated).

**Execution sequence:** TRIGGER, SOURCE, INTERVIEW, TIER CALL, GENERATE, DEBRIEF, OPTIONAL SAVE. Collapse the interview for any parameter the operator specified at invocation.

**Common failure modes to avoid:**
- Fabricating facts the source does not contain.
- Dropping the `WHERE WE LEFT OFF` block.
- Applying a global roast dial instead of the register's native attitude.
- Roasting an emotionally heavy thread.
- Lifting a character, a line, or a catchphrase from the inspired-by source.
- Emitting an em dash or an en dash.
