# The verification rules

**Read this file before either mode.** The three-layer model is scaffolding; these ten rules are
the method. Every one of them was learned by a session that got it wrong first, and each is written
here as *statement → the incident → the test you actually run*.

The incidents are cited to make the rules stick. The rules are what travels: none of them depend on
the repository they were learned in.

---

## 1. Merged is not deployed

**Statement.** Merging a protection into the trunk does not put it in the path of a live request.
Until you have exercised the running system, you know the code exists — nothing more.

**The incident.** An input guard merged with nine green tests. It sat undeployed for a full day
while the live endpoint accepted a formula-injection payload and returned `200`. The service had no
CI deploy step; nothing in the merge was wrong, and nothing about the merge made it true.

**The test.** When a gate or report asserts that a protection is *active*, verify it against the
deployed artifact — a version endpoint, a build marker, a deploy log, a live request that should now
fail. If you verified the merge only, **say "merge verified, deployment not verified" in those
words.** Silence reads as a stronger claim than you made.

**The inverse case is real too.** Infrastructure deployed from a branch and merged afterward means
the trunk now describes something that already exists. "Merged ≠ deployed" does not apply in that
direction; what is unverified instead is whether a fresh run from the trunk is *idempotent* against
the live estate. Name which direction you are in.

---

## 2. A response code is not evidence of a write's outcome

**Statement.** A `200` means the request was accepted. It says nothing about what was stored, how it
was interpreted, or whether it will be dangerous when read back.

**The incident.** A write that should have been rejected returned `200`. Reading the cell back in
the `values` representation looked clean. So did `text`. Only the `formulas` representation showed
the payload had been stored as a live formula.

**The test.** Read the value back **in the representation that would expose the failure**, not the
one that renders nicely. Ask: if this had gone wrong, which view would show it? Query that one. A
verification that cannot fail is not a verification.

---

## 3. Verify from the consumer's vantage point

**Statement.** A reference is only real if the party who must follow it can open it. Existence on
your side is not availability on theirs.

**The incident.** A handoff cited a Cowork session's project memory as the contract for a build. The
file existed and was correct. It was also unreadable from any session on the host machine, so the
builder had a dead pointer dressed as a citation.

**The test.** Before shipping a reference, ask *which process opens this, and can it?* Cross-platform
contracts ship as **files in a location the reader can read** — a repository path, an outbox file, a
PR body. Never a memory store, never "as we discussed", never a link into a conversation that ends.

---

## 4. A shell snippet inside a handoff is shipped code

**Statement.** Commands you paste into a handoff are not illustration. They will be run verbatim, by
an agent that trusts them, as the evidence for a gate.

**The incident.** A gate carried `curl A || curl B | grep pattern`. The pipe binds tighter than the
`||`, so the `grep` only ever applied to the fallback branch — on the normal path it never ran. Had
the gate tripped, its "evidence" would have been unfiltered YAML that looked exactly like diligence.

**The test.** Read every command in a handoff as code under review: precedence, quoting, exit codes,
what happens on the *success* path as well as the failure path. Prefer explicit sequencing to clever
one-liners. Where a gate must produce evidence, make the failure mode loud.

**And when a builder reports a defect in a handoff, fix the file, not just the conversation.** The
file is what the next session pastes. A correction that lives only in chat is a defect you have
agreed to ship again.

---

## 5. Compare full paths, never basenames

**Statement.** Concurrency safety is decided on full repository paths. Basenames create false
collisions and hide real ones.

**The incident.** A basename pass reported a collision between two issues over `util.js` — different
directories, different modules, no conflict whatsoever. Run sequentially, that false positive would
have cost a session.

**The test.** Parse each issue for the **full paths** it names and require the sets to be pairwise
disjoint before running work concurrently. Details and the failure taxonomy are in
`wave-selection.md`.

**Know the blind spot.** Issues written at the requirements level name no paths at all, so the
method sees no collision because it sees nothing. Two such issues collided on a shared renderer and
the batch had to be unwound. **An issue with no paths is not "safe" — it is unanalyzed.** Treat it
as colliding with everything until someone names its surface.

---

## 6. No closing keyword when the acceptance criterion is post-merge

**Statement.** `Fixes #N` in a PR body closes the issue the instant the PR merges — before any
post-merge verification has run.

**The incident.** Auto-close beat the verification step once. It was survivable only because
everything happened to pass; the issue had already closed while the thing it tracked was still
unproven.

**The test.** If the acceptance criterion includes anything that happens *after* the merge — a
deploy, a live check, a scheduled run — reference the issue without a closing keyword and close it
by hand once the criterion is met.

**Also: closing keywords ignore negation.** "This does not fix #123" registers #123 as closed. The
parser sees the keyword and the reference; it does not read the sentence. Never put a bare issue
reference near a closing verb in prose — write "issue 123" or link it explicitly.

---

## 7. A deviation a later block depends on is an issue, not a paragraph

**Statement.** If a downstream block of work will need to know that something was done differently,
the deviation needs a tracked record with its own lifecycle. A commit message is not that.

**The incident.** A deviation lived only in a commit message and a README line. Review caught it
before the dependent block started; nothing in the process would have.

**Its corollary.** When an issue's scope shrinks, **re-scope it rather than closing it** and folding
the residue into another issue's acceptance criteria. Acceptance criteria die when their issue
closes — anything parked there is deleted on a schedule you are not watching.

**The test.** Ask: does a future session need to discover this without being told? If yes, it is a
filed issue with a title that surfaces in a search, not a sentence inside an artifact someone would
have to already be reading.

---

## 8. Verify reports against the source before propagating them

**Statement.** A summary you pass along becomes your claim. Downstream readers cannot see whose
verification it originally was.

**The incident.** Three orchestrator reports, two overstated claims. One belonged to a sibling
session, which inferred a merge state rather than checking it. **One was the quarterback's own** — a
severity assessment for a job that had already self-healed.

**The test.** Before a report enters a durable record or a downstream handoff, check the claims that
matter against the source of truth: the tree, the PR, the live system. Apply this to your own
reports with more suspicion than to others', because there is nobody downstream of you doing it.

---

## 9. Name who can lift each constraint, and put unverified items in the PR body

**Statement.** A constraint with no named authority gets lifted by whoever is most inconvenienced by
it. An unverified item recorded only in chat disappears when the conversation ends.

**The incident.** Constraints written as flat prohibitions with no owner, and residual risk reported
into a chat thread that no later session could read.

**The test.** Every constraint in a handoff names who can lift it — the operator, the quarterback,
nobody. And every item that was *not* verified goes into the **PR body**, where the merge decision
is made, not into the report that dies with the session. **Merging is not shipping**; the PR body is
the last durable surface before the decision.

---

## 10. A gate encodes a branch model and a tool's real predicate — not a name and not your reading

**Statement.** A repo-state gate encodes a branch **model**, not a branch **name** — and the
**tool's actual predicate**, not the drafter's mental model of it. It must confirm that the content it
targets exists on the branch it writes to, and that its commands test what the drafter thinks they
test.

**The incidents — three, because the same mistake has three faces.**

- **The gate inverted the model it was written for.** A package drafted under one branch model ran
  after that model was retired, so its "safe" branch check sent routine records straight onto curated
  trunk — the exact placement the retired model existed to prevent.
- **A remediation gate was unsatisfiable on its own branch.** It required content to be present that
  the remediation itself had not yet added, so the gate could only pass after the work it was gating.
  A gate that cannot pass before the work is not a gate; it is a comment.
- **`git branch -d` measured something other than what the gate claimed.** The gate read `-d` as
  *merged into HEAD*; git tests *merged into UPSTREAM* when a branch has an upstream. It refused a
  branch that git itself reported as merged to HEAD, and the package had pre-drafted that refusal as
  proof that containment verification had failed. **A fail-closed refusal was misread as evidence of
  stranded work** — the most expensive kind of misreading, because it argues for exactly the
  destructive override (`-D`) that the refusal was protecting against. The refusal cleared once the
  stale upstream ref was gone, still under `-d`.

**The test.** For every gate: (1) **name which branch-model epoch it stands in** — if the model has
changed since drafting, the gate is stale even when its commands are correct; (2) verify content
targets with **git object reads on the branch being written** (`git show <branch>:<path>`), never a
working-tree read and never an assumption that a merge landed; (3) for any command whose refusal *or*
success the gate interprets, **state the tool's actual predicate in the gate text**, so the next
reader checks the claim instead of inheriting it. If a gate refuses, the first hypothesis is that the
gate is wrong, not that the tree is broken.

**10b — the allowlisted invocation is part of the gate surface.** A permission allowlist entry
naming `Bash(cmd /c outbox\hub-push.cmd)` silently opened a shell and pushed **nothing**, while the
same script invoked from PowerShell pushed correctly. The failure is not merely a broken command: an
agent *obeying the permission rule* selects exactly the broken path, and the allowlist makes the
wrong choice the compliant one. Worse, it fails quietly — a shell that opens and exits looks like
success. **The test:** the invocation form named in an Approvals row, a settings allowlist, or a
handoff is **verified by execution, not assumed**, and a form known to be broken is either fixed or
removed from the allowlist — leaving it there converts a permission grant into a trap.

---

## Quick reference

| # | Rule | The question it forces |
|---|---|---|
| 1 | Merged is not deployed | Did I exercise the running system, or just the trunk? |
| 2 | A code is not an outcome | Did I read it back in the view that would expose failure? |
| 3 | Consumer's vantage point | Can the party who must act on this actually open it? |
| 4 | A snippet in a handoff is shipped code | Would this command survive code review? Did I fix the file? |
| 5 | Full paths, never basenames | Do I know the paths, or do I just have no paths? |
| 6 | No closing keyword post-merge | Does acceptance finish after the merge? |
| 7 | A deviation is an issue | Will a future session need to discover this unaided? |
| 8 | Verify before propagating | Whose verification is this, and did anyone check it? |
| 9 | Name the authority; PR body | Who can lift this, and where does the unverified part live? |
| 10 | A gate encodes a model, not a name | Which branch-model epoch is this gate in, and does the command test what I think it tests? |
| 10b | The allowlisted invocation is gate surface | Did I *run* the exact invocation form the allowlist names, or assume it works? |
