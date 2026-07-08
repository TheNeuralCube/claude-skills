# Security lens: security review

## Deliverable

`{date}_{slug}_security-review_core-sample.md`, frontmatter and conventions per [../references/deliverable-contract.md](../references/deliverable-contract.md), lens `security`.

## Consumer

Execution-class, cold; a security-literate reader can defend every rating from the cited evidence alone.

## Required sections

1. TL;DR verdict with the risk posture in one paragraph.
2. System trust-boundary sketch: table or described diagram of actors, boundaries, and the data classifications crossing each.
3. Authn/authz analysis: mechanisms, token lifecycles, principal propagation, failure handling.
4. Input surfaces and injection analysis: SQL, command, template; for AI systems, prompt injection and tool-abuse paths explicitly.
5. Secret and key handling: storage, rotation, exposure in configs, builds, and logs.
6. Data-flow sensitivity: where regulated or sensitive data moves; logging exposure.
7. Defense-in-depth scoring per surface: layers present vs single points of enforcement.
8. Dependency and supply-chain notes: pinning, provenance, CI permissions.
9. Findings, using the same schema as [review.md](review.md), with severity mapped to exploitability x impact.
10. Prioritized remediation sequence.
11. Explicit out-of-scope statement: no penetration testing, static analysis only, snapshot caveat (findings reflect the artifact as read on the stated date).
12. War game section.

## Rules

1. Never fabricate vulnerabilities to appear thorough. A clean surface is reported as clean with the evidence that supports it.
2. Absence of evidence is stated as such, or gapped, never inferred into a finding.
3. Do not produce exploit code; produce defense guidance.

## Evidence emphasis

Full read per [../references/evidence-protocol.md](../references/evidence-protocol.md), weighted toward auth code, input handling, config, CI permissions, dependency manifests, and logging paths.

## War-game applicability

Full protocol per [../references/war-game-protocol.md](../references/war-game-protocol.md). The pre-mortem takes the form: "if this system is breached in 12 months, the three most likely vectors are", each with a mitigation or accepted-risk line.

## Quality bar

A security-literate reader can defend every severity rating from the cited evidence alone. Every input surface enumerated or explicitly gapped. The remediation sequence is executable in order by an execution-class session.
