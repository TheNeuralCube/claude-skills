# Deliverable contract

Single source for the output document contract. Mode files reference this file and do not restate it. Every Core Sample deliverable guarantees everything below.

## Output YAML frontmatter schema

Every deliverable begins with this frontmatter. Every field populated; no empty fields.

```yaml
---
title: <document title>
date: <YYYY-MM-DD>
skill: nc3-data-core-sample-skill-v0-1
target: <artifact identifier: repo name, URL set, document set, product name>
lens: <survey | craft | review | security | plan>
sensitivity: <open | internal | confidential | restricted>
consumer: execution-class
provenance: <one line stating what was read, at what depth, and what was excluded>
gap_count: <integer, the count of INFORMATION GAP markers in the body>
---
```

Rules for the fields:

| Field | Rule |
|---|---|
| title | Human-readable; names the target and the lens |
| date | Session date, ISO 8601 |
| skill | Exactly `nc3-data-core-sample-skill-v0-1` |
| target | Unambiguous identifier a cold reader can resolve to the artifact |
| lens | One lens tag per file; survey emits two files, each with lens `survey` |
| sensitivity | Operator-stated, or `internal` as documented default with a note |
| consumer | Always `execution-class`; deliverables never assume frontier capability in the reader |
| provenance | One line; the body's provenance section carries the detail |
| gap_count | Recomputed after the final edit pass; must match the body |

## Operator document conventions checklist

Apply every item to every deliverable. A miss on any item is a defect.

1. No em dashes (U+2014) and no en dashes (U+2013) anywhere. Use hyphens, colons, or restructure the sentence.
2. No empty fields. Anything unknown gets an explicit `[INFORMATION GAP: <exact question a cheaper session or the operator should answer>]` marker.
3. TL;DR at the top of the document and at the top of any long section.
4. Tables for enumerable content: findings, inventories, configs, assumptions, phases.
5. Sentence case headers.
6. Effort classes only; never model names. Write "execution-class session", never a vendor model name.
7. Self-contained: an execution session with only this file and the artifact can act. No references to "our conversation" or session-local context.

## Traceability rule

Every factual claim in a deliverable is traceable to a file path, URL, or document section, cited inline. A claim that cannot be traced becomes an INFORMATION GAP entry, never plausible filler. Absence of evidence is stated as absence, not silently skipped.

## Dash-check command

Run against every produced file before shipping; the command must return nothing:

```bash
grep -n "$(printf '\342\200\224\\|\342\200\223')" <file>
```

The octal UTF-8 escapes are U+2014 and U+2013; they work byte-wise in any grep. Where PCRE grep is available, `grep -n -P '\x{2014}|\x{2013}' <file>` is equivalent. Escaped forms are used here deliberately so this file passes its own check.
