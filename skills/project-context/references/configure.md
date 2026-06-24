---
file_role: skill-reference
topic: configure
schema_version_documented: "0.5"
skill_version: "0.7.0"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->
<!-- Copyright 2026 Raul J. Soto -->

# Configure (project-context v0.7.0)

This file is the single owner of the configuration interview mechanics. The three config files (`user-config.md`, `org-config.md`, `platform-specific-parameters.md`) each point here via their `configure_with: references/configure.md` frontmatter. Interview logic lives here once and is NOT duplicated into the config files; each config file carries only its own local FIELD GUIDE (what its fields mean), while this file owns how the interview is run.

This separation is part of the config/references convention (principle P4): operator-editable files live in `config/`, skill-owned files (including this one) live in `references/`. A file's location declares ownership.

## 1. When this runs

The operator loads a config file and asks the assistant to walk them through it ("configure this", "walk me through user-config", "help me set up org-config", "update my platform parameters"). The assistant then runs the interview defined here, using the loaded file's local FIELD GUIDE for field meanings, allowed values, and defaults.

This flow is configuration, not a context operation. It does not write `pc-NNNN-*` files, does not run the merge classifier, and does not emit a post-flight set-integrity directive. It produces a new version of one config file for operator approval.

## 2. Read location (base name, never a hardcoded path)

The skill reads and writes config files by base name (`user-config.md`, `org-config.md`, `platform-specific-parameters.md`), never by a hardcoded `config/` path.

- On filesystem platforms (Codex), the files live in `config/` and the skill reads `config/<name>.md`. (Cowork is also filesystem-based but its profile is deferred per SKILL.md; do not rely on a Cowork profile this cycle.)
- On flat platforms (Claude.ai, ChatGPT), the operator uploads the files and the skill reads `<name>.md` from project knowledge.

`config/platform-specific-parameters.md` documents `config_read_location` per platform. The directory is an unzip-time discoverability device for the human; base-name reads serve the skill at runtime. There is no `config-` prefix scheme and no naming-degradation logic.

## 3. The interview

1. **Load and parse.** Read the target config file. Parse its frontmatter (`config_type`, `schema_version`, the schema 0.5 header) and its body. Identify the current value of every field from the file's FIELD GUIDE.

2. **Batch the questions.** Ask about fields in batches grouped by the file's sections (for `user-config.md`: operator, defaults, conventions, privacy, contact). Do not ask one field per turn. For each batched group, show the current value and the allowed values from the FIELD GUIDE, and ask what the operator wants. Skip fields the operator does not want to change; carry their current value forward.

3. **Honor required fields.** The FIELD GUIDE marks REQUIRED fields. If a required field is still `[tbd]` after the interview, keep `[tbd]` (do not invent a value) and note it; the rendered file is permitted with placeholders but the skill emits the unpopulated-required-fields pre-flight note.

4. **Validate against the FIELD GUIDE.** Reject values outside a field's allowed set; re-ask. Do not silently coerce. Preserve the schema 0.5 config header (`schema_version: "0.5"`, `_managed_by`, `config_type`, `config_editable: true`, `configure_with`) verbatim; the interview changes field values in the body, not the header contract.

5. **Produce a diff or change summary for approval.** Before writing, show the operator a diff (or a structured change summary) of every field that would change: field, old value, new value. The operator approves, edits, or cancels. **Never overwrite silently.**

6. **Flag compliance-relevant changes.** If any changed field is a governance field, mark it `compliance-relevant` in the change summary so the operator (and any org reviewer) sees it explicitly. Governance fields:
   - `user-config.md`: `privacy.default_sensitivity`.
   - `org-config.md`: `sanctioned_tools`, `compliance.default_sensitivity`, `compliance.regulatory_scope`.
   - `platform-specific-parameters.md`: changes here are capability data, not governance; no compliance flag.

   Example change-summary line for a governance field:

   ```
   compliance-relevant: org-config.md compliance.default_sensitivity
     "internal" -> "confidential"
   ```

7. **Write the new version on approval.** Produce the updated file with the same base name. Rendered config files do NOT carry the SPDX header (that is template-only). On filesystem platforms, write to `config/<name>.md`. On flat platforms, present the file for the operator to download and upload, replacing the prior version.

## 4. What the interview never does

- It never writes a value the operator did not approve.
- It never changes the schema 0.5 config header contract (`config_editable`, `configure_with`, `config_type`, `schema_version`, `_managed_by`).
- It never edits a config file outside this approved flow. Config files are operator-owned; auto-creation (rendering a template with `[tbd]` placeholders when the file is absent) is the only unprompted write, and it writes placeholders only.
- It never duplicates field documentation. Field meanings live in each config file's FIELD GUIDE; this file owns only the mechanics.

## 5. Auto-creation (absent config file)

When a config file is absent at pre-flight, the skill renders the matching `config/*.template` into the operator's project as the base-name file with `[tbd]` placeholders for required fields and skill defaults inline elsewhere, and notes the auto-creation in the pre-flight report. Auto-creation does not run the full interview; it instantiates the template. The operator runs the interview later to populate it.

## 6. Cross-references

- Config-file frontmatter (schema 0.5 header): `references/schema.md` section 2.1.
- The three config templates and their FIELD GUIDES: `config/user-config.md.template`, `config/org-config.md.template`, `config/platform-specific-parameters.md.template`.
- Resolution order (user > org > defaults): `references/defaults.md`.
- Pre-flight auto-creation note and config base-name reads: `references/preflight.md`, `references/operations.md` section 4.
