<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Usage

How to run `conversation-recap` and what to expect. See `SKILL.md` for the full pipeline and `references/register-catalog.md` for the registers.

## Before you start

- Output is **in-chat and ephemeral by default.** This is entertainment, not archive. Nothing is saved unless you ask.
- The skill needs a source it can trace. It works from a handoff file, a named past conversation, the current thread's stale head, or a pasted transcript. If the source is thin or ambiguous, it asks one clarifying question rather than filling the gap itself.
- It will not carry working state. File paths, configs, schema, and IDs are contractually excluded. If you need those, ask for a session handoff instead.

## The fastest path

Say "previously on" or "catch me up" and name the thread. The skill interviews you briefly for a register, judges the tier, states its call in one line, and writes the recap.

```
previously on the Richard thread
```

## Steering it

Every parameter you supply at invocation is skipped in the interview. Supply none, some, or all.

| You say | What you set |
|---|---|
| "Seinfeld me on the vendor thread" | register only; the skill judges the tier |
| "recap me in war-novella, season recap" | register and tier; the interview is skipped entirely |
| "teaser on the migration thread" | tier only; the skill interviews for a register |
| "catch me up on Q3 planning" | nothing; full interview, then a stated tier call |
| "war-novella x mockumentary on the audit" | a mashup; permitted without a catalog entry |

## Picking a tier

Say the tier name, or let the skill call it. It picks from story complexity, open-thread count, stakes, and elapsed time, then tells you in one line: "One plotline, low stakes, high comedy density: calling it a Medium."

| Tier | Ask for it as | Reading time | Best for |
|---|---|---|---|
| Short | "teaser" | 60 to 90 sec | a thread you half-remember and need re-pointed at |
| Medium | "cold open" | 2 to 3 min | the default; a full arc with all open loops |
| Long | "season recap" | 4 to 6 min | a saga with multiple plotlines and a long gap |

If the source cannot fill the tier you asked for without invention, the skill drops to the tier the source supports and says so. That is the thin-source rule working, not a failure: it will never pad or invent connective beats to reach a word floor.

## Picking a register

The interview offers 3 to 4 picks: rotation picks surfaced for variety, plus free text. Each is presented as its slug plus a touchstone in parentheses, for example "standup-observational (Seinfeld-style)" or "simulation-noir (Matrix-style)".

You are never limited to what is offered. Name any of the 24 registers, or describe what you want.

**On emotionally heavy threads** (grief, conflict, a spiritual matter) the suggestions bias toward `documentary`, `novella`, and `suburban-wonder`, and away from the roast-native registers. You can still override to any register; the bias governs what is suggested, not what is permitted.

**On roast intensity:** there is no global roast dial. Choosing the register is choosing the treatment. Roast-native registers roast at full native intensity. If you want it gentler, pick a gentler register.

## What you get back

Three parts, every time:

1. A title card: `PREVIOUSLY ON: "<AN INVENTED EPISODE TITLE>"` plus an italicized attribution line.
2. The recap body in your chosen register, carrying the arc of the thread.
3. A `WHERE WE LEFT OFF` block listing every open loop as a scannable cliffhanger, optionally followed by one or two "season two questions" that reframe what you have not considered.

## After delivery

The skill runs a one-line check that the length and register landed and offers a re-cut. Take it if the register missed:

```
re-cut that as documentary, teaser
```

A re-cut does not re-run the full interview unless you ask for it.

## Saving

Say so explicitly. The file is named:

```
{YYYY}-{MM}-{DD}_{Topic_Words}-{register-slug}-{tier}_conversation-recap.md
```

For example `2026-07-17_The_Command-standup-observational-medium_conversation-recap.md`.

## When to use something else

| You want | Use |
|---|---|
| working state a future agent can resume cold | `session-handoff` |
| a structured, agent-consumable summary | your structured-summary skill; none ships in this repo |
| a reflective personal record | your journaling skill; none ships in this repo |

If you ask this skill for any of those, it names the gap and stops rather than smuggling machine state into a narrative recap.
