# Evidence protocol

Read discipline per artifact type. One evidence pass serves all selected lenses; never re-read the artifact per lens. Evidence notes accumulate with citations as the read proceeds, so a mid-flight checkpoint preserves value.

## Universal rules

1. Diagnostic-first: no conclusions before evidence. Read, then judge.
2. One shared evidence base; every selected lens renders from it.
3. Unverifiable claims become `[INFORMATION GAP: ...]` entries, never filler.
4. Record what was NOT reviewed; it feeds the provenance section of every deliverable (see [deliverable-contract.md](deliverable-contract.md)).
5. Every evidence note carries a citation: file path (with line where useful), URL, or document section.

## Code

1. Inventory first: tree, file sizes, entry points, documentation surfaces. Produce an internal read plan before deep reading.
2. Full read of load-bearing files: every file on the main execution paths, all documentation, all config, tests, CI, deployment definitions.
3. Evidence notes with file citations as you go; patterns claimed later must point at files.
4. Very large targets: if a full read at frontier depth is disproportionate (indicative threshold: several hundred thousand lines, or when the read plan projects context exhaustion before analysis), flag the scope anomaly once, propose a stratified read (full read of core paths, sampled read of leaf code, stated in provenance), then proceed with the stated approach. Do not ask permission; the flag is advisory.

## Documents

1. Complete read of every provided document. No skimming.
2. Citations by document name and section.
3. Cross-document contradictions are recorded as findings or gaps, not silently reconciled.

## Websites

1. Enumerate the surface first: from the operator's stated scope, or from site navigation if unstated.
2. Systematic fetch of the enumerated surface; record each URL visited.
3. Citations are URLs.
4. Note dynamic content limits explicitly: client-rendered content, auth walls, and personalization that a static fetch cannot observe become provenance caveats or gaps.

## Products and architectures

1. Gather every provided artifact: diagrams, specs, screenshots, demo access, marketing pages.
2. Analyze what is demonstrable from the artifacts; gap what is undemonstrable rather than inferring it into existence.
3. Citations name the specific artifact.
