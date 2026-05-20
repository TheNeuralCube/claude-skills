# Example: populated `user-config.md`

The block below is a realistic example of a user's `user-config.md` after they've made a few personal overrides. It is illustrative only — these are NOT recommended defaults for everyone. See `references/user-config-template.md` for the full template and explanation of each setting.

Generated-output examples do NOT carry SPDX headers.

```yaml
# ============================================================
# project-context — user configuration
# ============================================================
# Personal overrides for Sarah Chen's project-context deployment.
# Reload by re-uploading this file to the Project.
# ============================================================


# I'm comfortable handling more proposals per session than the default 10.
# I'd rather clear backlog faster than have it stack across sessions.
proposal_cap_per_session: 15


# I trust my own quality judgment for routine work and want speed.
# I have read the auto-mode warning in operations/default.md and
# acknowledge that every record I create this way is tagged auto in the
# audit trail.
merge_policy: auto


# Sticking with default token budgets — I'm on Claude Opus 4.7 which has
# plenty of headroom.
# active_file_token_target: 30000
# active_file_soft_warning: 50000
# active_file_hard_ceiling: 80000


# Scoring tweak: I want a slightly more aggressive demotion threshold so
# the active file stays denser. I tested 5.5 over two weeks and it worked
# for my volume of work.
scoring:
  demotion_threshold: 5.5


# Identify myself in the audit trail since the platform doesn't yet
# expose authenticated identity.
user_identifier: "sarah.chen"


# I find the per-session audit summary useful as a check on auto-mode.
brief:
  include_audit_summary: true
  show_token_budget: true
  show_demotion_list: true
```

## What this configuration does

- Sarah sees up to 15 gated proposals per session instead of 10. (Her `merge_policy: auto` makes this moot for most sessions, but it would matter if she changed to `hybrid` later.)
- Auto-mode is on, so every change applies without per-proposal approval. The auto-mode warning fires once per session. Every record Sarah creates carries `audit.approval_mode: auto` and `audit.approved_by: "sarah.chen"`.
- The demotion threshold is `5.5` instead of `5.0`. Records with weight between `5.0` and `5.5` will be proposed for DEMOTE in Sarah's deployment but would stay active for users on the default.
- The operator brief at the end of each session includes an audit summary, the active-file token budget, and the list of demoted records by ID.

## What this configuration does NOT do

- It does not change the schema. Files Sarah produces are valid `schema_version: "0.3"` files readable by anyone in the org.
- It does not change governance defaults. Sensitivity, retention, and frameworks come from `org-config.md` or upstream.
- It does not override the auto-mode warning. The warning still fires once per session.
- It does not affect other users. Each user has their own `user-config.md` in their own Project deployment.

## Org-config interaction

If Sarah's `org-config.md` sets `allow_user_auto: false`, the `merge_policy: auto` in her `user-config.md` is rejected at load time and the skill falls back to the org-level policy. The skill surfaces a one-line note in the operator brief explaining that the user-level `auto` was overridden by org policy.

This is the only setting where `org-config.md` has hard veto over `user-config.md`. For every other setting, `user-config.md` wins per the documented resolution order.
