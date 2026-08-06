# Conversation Recap ("Previously On") -- Architecture Vision

**Naming note (ratified 2026-07-17, final):** the skill is named `conversation-recap` -- plain functional name, no prefix, no version in the directory name, `version: 0.1.0` in YAML frontmatter. This follows the new-generation naming standard already in field use (`session-handoff`, `project-context`, `transcript-metadata-tagger`), which supersedes the nc3-era versioned-directory convention. "Previously On" is the product brand, preserved as the title card that opens every output.

**Document type:** Architecture Vision
**Date:** 2026-07-17
**Author:** Claude (Fable 5) with Raul Soto, NeuralCube
**Status:** Draft for operator ratification
**Companion document:** `2026-07-17_conversation-recap_design-spec.md`

---

## 1. The Problem

The NeuralCube continuity stack is built for machines resuming work. Nothing in it is built for a human resuming enthusiasm.

Session handoffs and session recaps restore *state*: decisions, file paths, schema, working context. They are optimized for an agent to resume cold with zero prior context. But when the operator returns to a stale thread after days or weeks, the bottleneck is not state. It is appetite. He remembers the essence of the conversation but not the detail, not the arc, not what made it exciting. Re-reading a YAML-fronted handoff does not fix this. It is homework.

The television industry solved this problem decades ago. Nobody rewatches last season before a premiere. They watch the "Previously on..." recap: a short, emotionally loaded, narratively shaped compression that restores the *feeling* of the season and surfaces the open cliffhangers. The brain backfills the rest, with emotion attached.

## 2. The Insight

**A handoff restores state. A Previously On restores appetite. These are different products.**

Low fidelity is not a compromise here; it is the feature. The deliberate loss of operational detail is what makes the artifact consumable at low cognitive energy. The operator does not need the schema. He needs the story: how the conversation progressed, what the insights were, what questions are still open, and where the tension lives. If he then needs working state, the handoff is one document away.

## 3. The Fidelity Ladder

This skill completes a three-rung ladder that previously had an undefined bottom rung:

| Rung | Skill | Fidelity | Consumer | Restores |
|------|-------|----------|----------|----------|
| High | `session-handoff` / `nc3-session-recap-skill` (handoff modes) | Full state, YAML contract, lineage | AI agents, cold resume | State |
| Medium | `nc3-session-recap-skill` (recap output) | Structured summary, decisions, next steps | AI agents and operator | State + orientation |
| **Low** | **`conversation-recap` (this)** | **Narrative compression, open loops as cliffhangers** | **The operator, as a human being** | **Appetite + orientation** |

The rungs reference each other. A Previously On may be generated *from* a handoff or recap (downsampling) or directly from a thread. Every Previously On ends with a pointer: for working state, see the handoff.

## 4. The Ultimate Vision: The Persona Layer

Previously On is the pilot episode of something larger.

The end state is a **persona toggle layer** for the entire personal hub: a library of interaction registers the operator can flip on any conversation. "Run this session in war-novella mode." "Give me the standup register for this code review." "Documentary voice for the OCIA study notes." The default Claude voice is too dry for sustained engagement at low cognitive energy; the persona layer is the fix, and it is infrastructure, not decoration. Engagement is a productivity multiplier for this operator. That is the thesis.

Previously On proves the core components the persona layer needs:

1. **A register catalog** -- style contracts that define voice, structure, and attitude per register.
2. **A mood interview** -- a short elicitation flow that matches register to operator state.
3. **Native-attitude doctrine** -- each register carries its own posture toward the operator (see Section 6).
4. **A judgment-call doctrine** -- the AI makes the creative calls (tier, structure, intensity); the operator tweaks by exception, not by configuration.

When the persona hub is built (future skill, new-generation naming, working name `persona-hub`), the register catalog migrates from this skill into a shared reference that all persona-aware skills consume. Previously On becomes one mode among many.

## 5. The Register Doctrine (Not Fan Fiction)

Registers are **stylistic DNA, not licensed characters**. Ratified 2026-07-17.

Each register captures the narrative machinery of its inspiration -- the paranoia of simulation-noir, the pettiness-spiral of cringe-comedy verite, the doorbell-timing of 70s farce -- using original characters, original dialogue, and the operator's own life as the material. No lifted characters, no lifted lines, no reproduced IP.

This is the legally clean version and the more durable one: it becomes a **house style library** owned by the operator, not a costume rack borrowed from studios. The catalog is extensible; new registers are added by writing a new style contract, not by negotiating with a franchise.

## 6. The Roast Doctrine

Ratified 2026-07-17: **no global roast dial.** Each register carries its native attitude toward the protagonist.

- Cringe-comedy verite and observational standup are structurally required to make the protagonist complicit. They roast. Hard. The operator has explicitly authorized full native intensity ("lay it on me").
- Golden-age heroism flatters. Dark-vigilante noir broods. The war novella does not care about anyone's feelings because there is a war on.
- Attitude is a property of the register, selected at interview time. Choosing the register IS choosing the treatment.

Calibration reference: the Seinfeld-register test run of 2026-07-17 ("The Command") is the ratified gold standard for native-attitude comedy intensity.

## 7. The Constitution Underneath

All registers share an invisible moral spine: a Catholic worldview governing what the stories value -- fidelity, repentance, mercy, the dignity of persons, consequences that mean something. This is the author's perspective, not the story's sermon. It is never announced, never evangelized in-text, and never visible unless the operator or an audience member asks where the stories come from. If asked, the answer is given plainly.

**Future research item:** integration with the `soul.md` concept from the OpenClaw repository as the formal mechanism for encoding this constitution across the persona layer. The operator will direct a repo review in a future session. Until then, the constitution lives as prose doctrine in the register catalog preamble.

Explicit exclusion: no Star Trek register.

## 8. Success Criteria

A Previously On succeeds when:

1. The operator finishes it (completion is the metric; if he skims, the tier or register was wrong).
2. He can state the open loops from memory afterward without re-reading the thread.
3. He *wants* to resume the work. Appetite restored is the entire point.
4. It never sends him back to the raw thread to figure out what happened. If it does, fidelity was too low even for low.

## 9. Roadmap

| Phase | Deliverable | Status |
|-------|------------|--------|
| 0 | Concept test runs (Curb register, Seinfeld register) in live conversation | Complete, 2026-07-17 |
| 1 | `conversation-recap` v0.1.0 built in Claude Code per design spec | Next |
| 2 | Field use across stale threads; register rotation; tier calibration | -- |
| 3 | Register catalog extraction into shared reference; `persona-hub` v0.1.0 | -- |
| 4 | OpenClaw `soul.md` review; constitution encoding mechanism | -- |
| 5 | Persona toggles as conversation-level switches across the hub | -- |

## 10. Decisions Requiring Operator Ratification

1. ~~Skill name~~ **RATIFIED 2026-07-17 (final):** `conversation-recap`, version 0.1.0 in frontmatter, new-generation naming standard. Rejected along the way: `nc3-session-previously-on-skill` (clever, not descriptive), `nc3-session-story-recap-skill` (operator veto), `session-recap` (collides with existing production skill). Disambiguation from `nc3-session-recap-skill` is carried by the YAML descriptions: structured/state recap vs. narrative/story recap.
   **Ecosystem debt surfaced by this decision:** two naming generations coexist. New generation (plain name + frontmatter `version:`): `session-handoff`, `project-context`, `transcript-metadata-tagger`, now `conversation-recap`. Legacy (versioned directory names): all `nc3-*` and `per-*` skills. `nc3-meta-conventions-skill` requires a v0-3 bump to document the new-generation standard and a migration posture for legacy skills. Tracked in the session handoff.
2. Persona hub future name: `persona-hub` (new-generation naming, version in frontmatter).
3. Tier boundaries as defined in the design spec Section 4.
