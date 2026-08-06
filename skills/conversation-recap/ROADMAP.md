<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->
# Roadmap

Deferred items and future direction for `conversation-recap`. Nothing here is committed; the list records intent and the conditions under which each item would be taken up.

## Deferred from v0.1.0

| Item | Disposition |
|---|---|
| **Usage-history store for past-favorite registers** | Deferred, platform-dependent. The interview is specified to offer 1 to 2 "past favorites" alongside rotation picks, but there is no store to read at v0.1.x, so the skill degrades to rotation-only and is forbidden from claiming a favorite the operator never chose. Taken up when a durable per-operator preference store exists on the target surface. |
| **Register usage rotation memory** | Deferred with the above. "Not used recently" currently means "the agent's judgment inside one session" rather than a tracked fact. |
| **Additional registers** | Open by design. The extensibility rule takes a new register as an appended catalog entry (slug, DNA, narrative contract, native attitude, inspired-by, touchstone, one original exemplar line) plus a MINOR bump. No code change is involved. |
| **Mashup catalog entries** | Not planned. Mashups are already permitted at generation time without an entry; cataloguing them would multiply the table without adding capability. |
| **Register-specific calibration anchors** | Candidate. One ratified gold standard exists ("The Command", Seinfeld register, Medium). Anchors for other registers and tiers would tighten calibration, but each costs a real run to produce. |
| **Automatic source acquisition from a handoff file** | Partial. The skill accepts an explicit handoff file as its cleanest source, but does not go looking for one. Auto-discovery awaits the same surface capabilities the sister skills are waiting on. |

## Conditions for v1.0.0

v0.1.x stays at 0.x because the output is calibrated against a single ratified run.

1. Real use across at least three distinct registers and all three tiers, without a fabrication-rule or interiority-clause violation.
2. The `WHERE WE LEFT OFF` block proves it actually restores orientation, meaning the operator acts on it rather than re-reading the source.
3. The emotionally-heavy-thread bias is exercised on a genuinely heavy thread and judged correct.
4. At least one additional calibration anchor beyond "The Command".

## Known limitations

- **Single calibration anchor.** Medium-tier feel is calibrated against one run in one register. Other registers and tiers are specified but not anchored against a ratified example.
- **No usage history.** Past-favorite picks are specified and unavailable. This is a graceful degradation, not a defect, but the interview is thinner than designed.
- **Ephemerality is a deliberate constraint, not a gap.** Recaps are not archived, indexed, or made searchable. If a recap needs to persist, the operator asks for the save explicitly and owns the file from there.
