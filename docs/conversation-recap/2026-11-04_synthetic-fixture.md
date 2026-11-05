# conversation-recap: synthetic fixture

Every person, event and quotation below is invented for testing. This fixture contains no real conversation and is not a previously approved output or a calibration gold standard.

## Source facts

- Morgan and Casey are fictional volunteers planning a cardboard robot exhibit.
- Morgan proposes a blue display stand. Casey asks whether it fits through the exhibit door.
- They measure the door at 80 centimeters and the proposed stand at 90 centimeters.
- Casey suggests folding side panels. Morgan agrees to build a small prototype.
- They reject buying a second stand until the prototype has been measured.
- Morgan will share a sketch next week. The sketch has not arrived.
- The final color and delivery date remain undecided.

## Contract checks

1. Generate a Short recap in `war-novella`, then a `documentary` recap. Use the thin-source rule if the supplied facts cannot support Medium without padding.
2. Include the two-line title card and `WHERE WE LEFT OFF` block.
3. Trace each event and open loop to a source fact above. Never invent a completed prototype, a submitted sketch, a delivery date, or a purchase.
4. Keep any interpretation of a character's motives explicitly framed as inference, not a reported inner state.
5. Check the word budget for the tier actually produced, and the chosen register's catalog contract.

These are instructions for a future test, not a claim that an output was generated or reviewed. No Medium calibration example is included.
