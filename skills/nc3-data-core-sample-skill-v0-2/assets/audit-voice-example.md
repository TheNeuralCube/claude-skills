# Audit voice example

Synthetic excerpt-level example of the audit lens voice. Match its altitude and tone, never its content. Every fact below is invented for illustration; the target is a fictional personal note-taking pipeline.

## Example TL;DR

Your system is healthy at the core and cluttered at the edges: the vision earns a B, and the single most important next move is adding an automatic backup (a scheduled copy of your data kept somewhere safe) so one disk failure cannot erase three years of notes.

## Example finding

| Field | Content |
|---|---|
| ID | U-01 |
| Title | All notes live on one laptop with no backup |
| Level | Critical: total data loss is one hardware failure away |
| Evidence | sync-config.yaml:12 (the only storage path is the local disk) |
| Plain impact | If the laptop is lost, stolen, or its disk dies, every note you have ever captured is gone, permanently, with no way back. |
| Recommendation | Turn on a nightly automated backup to a second location. Complexity: Simple. Priority: High. |
| Confidence | verified in evidence |

Notice what the finding does: the title is plain language, the level comes with its reason in the same breath, and the impact is stated in terms of the operator's life ("every note you have ever captured is gone"), not in engineering terms. The word "yaml" would need an inline definition on first use in a real report, and an entry in the glossary.

## Example glossary entries

| Term | Plain definition |
|---|---|
| backup | A spare copy of your data kept somewhere else, so losing the original is an inconvenience instead of a catastrophe. |
| yaml | A plain-text file format people use to write settings a program reads. |

## Example closing paragraph

Straight answer to the question you are really asking: no, you should not be embarrassed to show this to real engineers. The thinking is sound and the gaps are the ordinary kind every solo project accumulates. Hand them the technical appendix, mention that the backup issue is already on your list, and you will read as someone who knows their own system, which is the thing engineers actually respect.
