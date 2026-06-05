---
file_role: skill-reference
topic: configure
schema_version_documented: "0.1"
skill_version: "0.1.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# The shared config-interview procedure (session-handoff v0.1.0)

This file owns the configuration interview mechanics **once**. Every config file carries only its own field guide plus a pointer to this procedure; interview logic is never duplicated into each config file. Duplicating interview logic into every config file is the scaling failure this convention exists to avoid.

When the operator loads a config file and asks to configure it ("walk me through configuring this", "configure this file", "set up my user-config"), the skill runs this procedure, uses that file's local FIELD GUIDE, and produces a new version of the file as a diff or summary for operator approval before saving. The skill never silent-overwrites a config file.

This procedure is part of the config-layer convention shared with the sister skill project-context (proposed as a cross-skill standard; see `README.md`).

## 1. When this procedure runs

| Trigger | Action |
|---|---|
| Operator loads a config file and asks to configure it | Run this procedure against that file. |
| Pre-flight detects a config file is absent | Auto-create it from its `.template` with placeholder defaults (section 5); do not run the full interview unprompted. |
| Operator asks to change a specific field | Run the procedure scoped to that field and its dependents. |

The procedure operates on one config file at a time. The file's `config_type` (user, org, redaction-policy, platform) selects which FIELD GUIDE governs.

## 2. The interview

1. **Read the target file's FIELD GUIDE.** It documents that file's fields, allowed values, and defaults. The guide is the authority for what to ask; this procedure is the authority for how to ask.
2. **Identify unpopulated and default-valued fields.** Required fields still set to `[tbd]` are the priority. Fields already at sensible defaults are mentioned but not pressed.
3. **Batch the questions.** Group related fields into a small number of questions rather than a long single-field interrogation. Aim for the fewest exchanges that still let the operator answer confidently. Lead with required fields.
4. **Confirm each answer back** in plain language before composing the file, so the operator catches a misread before it is written.
5. **Compose the new version** of the file, preserving the standard header (section 4) and the FIELD GUIDE, substituting the operator's values for placeholders and defaults.
6. **Present the result as a diff or a summary for approval** (section 3). Do not save until the operator approves.
7. **On approval, write the new version.** On any governance-relevant change, the approval summary must have flagged it (section 6).

## 3. Approval discipline (never silent-overwrite)

The skill presents the proposed config as a diff against the current file (preferred) or a clear before-and-after summary when a diff is impractical on the surface. The operator approves, edits, or cancels. The skill writes only on explicit approval.

This is the same approval-diff discipline the sister skill uses for its config edits. A config file is operator-owned; the skill proposes, the operator disposes.

## 4. The standard config-file header

Every config file (and template) carries this header:

```markdown
---
schema_version: "0.1"
_managed_by: session-handoff-skill
config_type: <user | org | redaction-policy | platform>
config_editable: true
configure_with: references/configure.md
---
# To configure: load this file and tell your AI "walk me through configuring this."
# It runs the shared interview (references/configure.md), uses the FIELD GUIDE below,
# and writes you a new version of this file for approval before saving.
#
# FIELD GUIDE (local to this file)
# ...field-by-field documentation...
```

The interview procedure preserves this header on every write. The FIELD GUIDE is descriptive content local to each file; orchestration stays here in the trusted skill, never in the config file, so an embedded field guide cannot become a prompt-injection vector.

## 5. Auto-creation (first run)

At pre-flight, for each config file the skill expects:

1. Search project knowledge for the file with `_managed_by: session-handoff-skill` and the matching `config_type`.
2. If absent, instantiate the config file from its `.template`. The `.template` files are not themselves valid config files: each wraps the rendered config inside a single fenced code block, after an SPDX header and explanatory prose. Auto-creation **extracts the content between that fence's delimiters** (the block beginning with the `---` frontmatter through the final config key), leaves the explicit defaults as shipped, leaves `[tbd]` on required-but-unpopulated fields, and writes that extracted content as the new config file. The SPDX header and the surrounding template prose are not copied into the rendered file (the rendered file is operator work product). The standard config-file header (section 4) is the first thing inside the fence, so it carries through.
3. Emit in the pre-flight report: "config/<file> auto-created with placeholder defaults; populate to enable full personalization."

Never blind-write. Auto-create only when the file is confirmed absent. The full interview runs only when the operator asks; auto-creation just lands a populated-with-defaults starting point. Platform-dependent instantiation (real `config/` directory versus a `config-` name prefix on flat surfaces) is specified in `references/platform-specific-parameters.md`.

## 6. Governance-relevant changes are flagged

Changes touching governance fields are compliance-relevant. At a public company a config change is a compliance action. The approval summary must flag, explicitly, any change to:

- sanctioned tools or sanctioned destinations (`config/org-config.md`),
- sensitivity defaults (`config/user-config.md`, `config/org-config.md`),
- redaction categories, `sensitivity_rules`, or `redaction_provider` (`config/redaction-policy.md`),
- the `sanitization_prompt` gate setting (`config/user-config.md`).

The flag reads, in substance: "This change is compliance-relevant: it alters <field>. Confirm before saving." The operator still approves through the normal diff; the flag ensures the governance impact is not buried in an otherwise routine edit.

## 7. Cross-references

- The config-layer convention and tiering: `references/governance.md`, `README.md`.
- User config fields: `config/user-config.md.template`.
- Org config fields: `config/org-config.md.template`.
- Redaction policy fields: `config/redaction-policy.md.template`, `references/redaction.md`.
- Platform parameters and config-instantiation layout: `config/platform-parameters.md`, `references/platform-specific-parameters.md`.
- Defaults the config layers override: `references/defaults.md`.
