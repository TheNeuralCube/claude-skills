# Survey lens: as-built design spec + as-built build spec

## Deliverables

Two files:

1. `{date}_{slug}_design-spec_core-sample.md`
2. `{date}_{slug}_build-spec_core-sample.md`

Both carry the frontmatter and conventions in [../references/deliverable-contract.md](../references/deliverable-contract.md), lens `survey`.

## Consumer

Execution-class, cold. The reader has only these files and the artifact.

## Required sections: design spec

1. TL;DR and reading order (which document to read first, for what purpose).
2. System purpose and architecture planes, as a table (plane, responsibility, key components).
3. Topology and deployment shape.
4. Core design patterns: each named, located (file citation), and justified (why the author chose it, as evidenced). Target 5 to 10.
5. Primary lifecycle trace: one real flow traced end to end through the code or system.
6. Interface contracts worth preserving (APIs, schemas, file formats, invariant boundaries).
7. Model/effort tiering, if the artifact is AI-relevant; otherwise state not applicable in one line.
8. Gap analysis table: as-built vs stated or evident intent, each row with severity.
9. Optimizations and recommendations, ranked by leverage, each tagged FIX (improve in place) or PORT (worth lifting elsewhere).
10. Provenance.

## Required sections: build spec

1. Repo/artifact layout and toolchain.
2. Startup or entry wiring, in execution order.
3. Component map table: name, size, responsibility, key exports.
4. The core engine explained: whatever loop, pipeline, or render path is load-bearing, with the implementation details that matter.
5. Extension recipes as found in the artifact (how the author adds a new X).
6. Inventory tables: tools, endpoints, pages, config, as applicable.
7. Configuration surface table with defaults.
8. CI/CD and deployment.
9. Testing conventions.
10. Invariants never-do list, as documented in the artifact.
11. Provenance, with an explicit statement of what was NOT reviewed.

## Evidence emphasis

Complete structural read per [../references/evidence-protocol.md](../references/evidence-protocol.md). Every load-bearing file opened. Config and CI read, not skimmed. Every pattern claim cites a file.

## War-game applicability

Mandatory for the recommendations section of the design spec: run [../references/war-game-protocol.md](../references/war-game-protocol.md) against those recommendations (red-team, assumptions ledger, consumer simulation, fluff purge). The descriptive sections do not require red-teaming but do require the traceability rule.

## Quality bar

An execution session could navigate the artifact cold from the build spec alone. Every pattern claim cites a file. The design spec explains why the system is shaped this way; the build spec explains where everything is and how to work in it.
