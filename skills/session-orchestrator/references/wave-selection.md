# Wave selection: deciding what can run concurrently

A **wave** is a set of issues built in parallel across separate orchestrator and builder sessions.
The only thing that makes a wave safe is that its members cannot touch the same file.

This is a mechanical procedure. Run it; do not eyeball it.

## Procedure

1. **Fetch every candidate issue body in full.** Not the title, not the list view. The paths live in
   the body, and a truncated fetch produces a confidently wrong answer.

2. **Extract the full repository paths each issue names.** `services/api/src/lib/util.js`, not
   `util.js`. Include paths named in code blocks, acceptance criteria, and linked diffs.

3. **Classify each issue:**
   - **Path-bearing** — names one or more concrete files.
   - **Path-free** — written at the requirements level, names no files. *These are not safe; they
     are unanalyzed.* See "The blind spot" below.

4. **Pairwise-disjoint test.** Two path-bearing issues may run concurrently only if their full-path
   sets share no member. Compare paths as strings, in full. A shared basename in different
   directories is **not** a collision.

5. **Add the shared-surface check.** Even with disjoint file sets, two issues collide if they both
   change a shared contract: a schema, a generated file, a lockfile, a workflow file, a public
   interface one of them consumes. Ask explicitly: *do these two change the same contract?*

6. **Assign one orchestrator per issue, or per genuinely safe batch.** Batching is an optimization,
   and it is only worth it when the members are small and provably disjoint.

7. **Order what cannot be parallelized.** Sequence collisions explicitly rather than hoping. State
   which issue runs first and why.

## The blind spot

The method reads paths. An issue with no paths gives it nothing to read, and "no collision found"
is indistinguishable from "no analysis possible."

A batch was run on that basis and two of its issues collided on a shared renderer, forcing a
sequential re-run.

**Rule: a path-free issue collides with everything until someone names its surface.** The cheap fix
is to name the likely files in the issue before wave selection — a two-minute edit that converts an
unanalyzable issue into an analyzable one. Do that rather than gambling.

## What a false collision costs

A basename-level pass reported a collision between two issues over `util.js` that lived in different
services. Acting on it would have serialized two independent builds and spent a session for nothing.

False collisions cost time. Missed collisions cost a merge conflict, a half-built branch, and the
trust in the report that said the batch was safe. **Both failures come from the same shortcut**, so
do the full-path comparison properly rather than tuning which error you would rather have.

## Recording the selection

The wave's rationale goes into the durable project record, not the chat: which issues, which paths,
which pairs were disjoint, what was deliberately sequenced and why. The next wave's selection starts
from that record — and when something collides anyway, that record is what tells you which
assumption was wrong.
