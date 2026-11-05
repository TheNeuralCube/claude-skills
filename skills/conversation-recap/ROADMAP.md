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
| **Register-specific calibration anchors** | Candidate. Publish explicitly synthetic, reviewed examples for each register and tier; none is currently an approved calibration anchor. |
| **Automatic source acquisition from a handoff file** | Partial. The skill accepts an explicit handoff file as its cleanest source, but does not go looking for one. Auto-discovery awaits the same surface capabilities the sister skills are waiting on. |

## Conditions for v1.0.0

The skill stays at 0.x until public synthetic examples are reviewed and support repeatable calibration.

1. Real use across at least three distinct registers and all three tiers, without a fabrication-rule or interiority-clause violation.
2. The `WHERE WE LEFT OFF` block proves it actually restores orientation, meaning the operator acts on it rather than re-reading the source.
3. The emotionally-heavy-thread bias is exercised on a genuinely heavy thread and judged correct.
4. At least two reviewed synthetic calibration examples across registers and tiers.

## Known limitations

- **Missing public calibration.** Registers and tiers are specified, but no approved calibration output is bundled.
- **No usage history.** Past-favorite picks are specified and unavailable. This is a graceful degradation, not a defect, but the interview is thinner than designed.
- **Ephemerality is a deliberate constraint, not a gap.** Recaps are not archived, indexed, or made searchable. If a recap needs to persist, the operator asks for the save explicitly and owns the file from there.
