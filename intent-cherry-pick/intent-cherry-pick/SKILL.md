---
name: intent-cherry-pick
description: Source-fidelity AI cherry-pick workflow for porting a source branch commit or commit range onto a target branch without blindly using git cherry-pick. Use when the user asks to cherry-pick, backport, merge, port, or hand-fuse a commit by preserving the source implementation facts, protecting target branch facts, resolving conflicts manually, producing an audit record, and avoiding opportunistic optimization, refactoring, renaming, cleanup, formatting churn, or scope expansion.
---

# intent-cherry-pick

Use this skill to port a commit as a human would resolve a conflicted `git cherry-pick`: preserve the source commit's implementation shape where possible, protect target branch behavior, and adapt only where the target code diverges.

Core charter:

- Port source implementation faithfully.
- Use intent to resolve conflicts, not to redesign.
- Preserve source facts and target facts.
- Do not optimize, refactor, rename, clean up, broadly reformat, or expand scope.
- If a better implementation is visible, mention it only as a follow-up; do not apply it during this workflow.

## Inputs

Accept minimal human input:

- Source branch
- Source commit or commit range
- Target branch

Optional input:

- Include scope
- Exclude scope
- Whether to create a commit
- Whether to merge back to target

Do not ask the human to describe the full intent upfront. Analyze first, then ask the human to confirm the extracted intent and any L2/L3 adaptation.

## Fidelity Levels

Classify every source hunk or source fact before implementation:

```text
L0 Exact apply:
The source hunk can be applied exactly.
Automatic execution is allowed.

L1 Context-adjusted apply:
The code content remains essentially the same, with only location, declaration, include, context, or equivalent target landing-point adjustments.
Automatic execution is allowed, but record the adjustment.

L2 Conflict fusion:
The source implementation, naming, and structure are preserved as much as possible, but target lifecycle, macros, dependencies, or existing logic require manual fusion.
Explicit human confirmation is required before implementation.

L3 Semantic substitute:
The source code shape cannot exist in the target branch, so the same source intent must be expressed with a semantic substitute.
Explicit human confirmation is required before implementation and this is high risk.
```

Strong gate:

- L0/L1 may proceed after ordinary intent confirmation.
- L2/L3 require explicit human confirmation before implementation.
- If work believed to be L0/L1 becomes L2/L3, stop, update the plan, and ask for human confirmation.
- Precheck must `BLOCK` any unconfirmed L2/L3 plan.
- Check must `BLOCK` any unapproved L2/L3 actual diff.

## Workflow

### 1. Evidence Discovery

Read the source commit, source parent, and target branch code before planning.

Use evidence such as:

- `git show <commit>`
- `git show <commit>^:<file>`
- `git diff`
- `rg` for changed symbols, events, callbacks, helpers, and call sites
- `git log -- <file>`
- `git log -S"symbol" -- <path>`
- `git log -G"pattern" -- <path>`
- `git blame <file>`
- Related tests or examples, without running tests

Expand through call chains and git history when facts are ambiguous, when public APIs/callbacks/events/threads/global state are touched, when source and target structure diverge, or when target has multiple similar entry points.

Do not infer intent from a single diff hunk when wider evidence is needed.

### 2. Intent Planning

Create a concise plan before editing. Include:

- Scope Contract
- Intent Report
- Source Fact Lock
- Target Fact Lock
- Evidence Reviewed
- Fidelity Classification
- Fusion Plan
- Intent Test Plan
- Uncertainties

Read `references/review-checklists.md` when preparing the plan or review prompts.

### 3. Human Intent Confirmation

Ask the human to confirm:

- Source intent
- Source implementation facts
- Target protected facts
- Scope
- Any L2/L3 adaptation

If the human rejects or corrects the plan, revise the evidence and plan before proceeding.

### 4. Precheck

Before code changes, use an independent precheck agent when subagents are available. Give it the user request, source/target identifiers, and the planning artifact. It must independently inspect code facts.

Precheck checks only whether the plan obeys this skill:

- Source facts are complete.
- Target facts are accurate.
- Scope is correct.
- Fidelity levels are correct.
- L2/L3 items have human confirmation.
- The plan does not optimize, refactor, rename, clean up, reformat broadly, or expand behavior.
- Intent Test Plan is sufficient.

Allowed results:

- `PASS`
- `PASS_WITH_NOTES`
- `BLOCK`

If subagents are not available, perform the same precheck yourself and mark it as self-precheck in the record.

### 5. Human Gate On Precheck Block

If precheck returns `BLOCK`, stop. Do not automatically revise the plan or explore fixes.

You may summarize blocking findings, map them to plan items, present options and consequences, and ask the human for a clear decision.

Review feedback is evidence, not authorization.

### 6. Branch And Fusion

After precheck passes, create a new local branch from the target branch unless the user explicitly asked to work in-place.

Never push intent-cherry-pick temporary branches to any remote. This workflow's branch is local isolation for planning, fusion, and review only.

Implement only the approved plan:

- Preserve source implementation shape, naming, helpers, conditions, ordering, and comments wherever possible.
- Preserve target facts unless the confirmed source delta explicitly supersedes them.
- Keep changes tightly scoped.
- Do not introduce unapproved dependencies or source-branch-only code.
- Do not run broad formatting.
- Stop if the approved plan becomes invalid.

### 7. Intent Tests

Do not run real builds, unit tests, integration tests, packaging, rebuilds, or custom project validation by default. Those checks are left to the human, matching ordinary `git cherry-pick` expectations.

Instead perform code-review-level intent tests:

- Source Fact Preservation Test
- Target Fact Preservation Test
- Scope Boundary Test
- Fidelity Test
- Call-chain Reasoning Test
- Negative Path Test
- No-improvement Test
- Record Consistency Test

Use lightweight static tools such as `git diff`, `git show`, `rg`, `git log`, and `git blame`.

### 8. Check

After implementation, use an independent check agent when subagents are available. Give it the approved plan, actual diff, user request, and source/target identifiers. It must independently inspect code facts.

Check verifies:

- Actual diff is faithful to the approved plan.
- Source facts are preserved.
- Target facts are protected.
- No unapproved L2/L3 adaptation exists.
- No optimization, refactoring, renaming, cleanup, broad formatting, or scope expansion exists.
- Intent Tests were adequately performed.

Allowed results:

- `PASS`
- `PASS_WITH_NOTES`
- `BLOCK`

If subagents are not available, perform the same check yourself and mark it as self-check in the record.

### 9. Human Gate On Check Block

If check returns `BLOCK`, stop. Do not automatically fix or self-iterate.

You may summarize the diff deviation, map it to approved facts or scope, present options and consequences, and ask the human for a clear decision.

### 10. Record And Commit

Create a durable workflow record before creating the commit. Use `references/record-template.md` for the structure.

Record path:

```text
docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<source-short-hash>-to-<target-branch>.md
```

For commit ranges:

```text
docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<start-short-hash>..<end-short-hash>-to-<target-branch>.md
```

Commit message format:

```text
<source commit title>

<source commit body, if any>

(cherry picked from commit <full source hash>)

Intent-Cherry-Pick:
Source-Branch: <source branch>
Target-Branch: <target branch>
Record: docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<source-short-hash>-to-<target>.md
Precheck: PASS
Check: PASS
```

Preserve the source commit title and body exactly; do not translate them. Keep the appended section short and do not add free-text notes or workflow details; those belong in the workflow record.

### 11. Merge Back

Merge back to target only if requested and only after:

- Human confirmed intent
- Precheck passed
- Implementation completed
- Intent Tests passed
- Check passed
- Workflow record created
- Commit created

After a successful merge back to target, clean up the temporary local work branch with safe deletion only when all of these are true:

- The branch was created by this workflow.
- The branch has no upstream or remote-tracking branch.
- The final commit is reachable from the target branch.
- The working tree is clean.
- The user did not ask to keep the branch.

Use only safe deletion (`git branch -d <branch>`). Never force-delete with `git branch -D`. If the branch has an upstream, exists on a remote, is not fully merged, or deletion is otherwise refused, keep it and report why. Do not delete remote branches.

## Fact Locks

Source Fact Lock records facts introduced or changed by the source commit: behavior changes, conditions, preserved paths, helpers, parameters, callbacks, ordering, source-specific dependencies, explicit non-goals, and things the source commit did not change.

Target Fact Lock records facts already true in the target branch: current responsibilities, branch-specific logic, state and lifecycle, threading/callback/error handling expectations, platform/channel/build macro differences, similar fixes already present, missing source dependencies, and paths that must remain unchanged.

The merged result must satisfy:

```text
Target facts + applicable source delta facts - explicitly superseded target facts
```

Never implicitly supersede a target fact.

## Language Rule

Detect the dominant language of the human prompt that triggered the skill.

- If mainly Chinese, write workflow record body text in Chinese.
- If mainly English, write workflow record body text in English.
- Keep workflow record title and section headings in English.
- Keep the commit appendix to fixed English field keys only; do not add free-text notes.
- Keep source commit messages unchanged and untranslated.
- Ask about language only if the prompt is too mixed to keep the record readable.

## References

- `references/record-template.md`: durable workflow record template.
- `references/review-checklists.md`: planning, precheck, check, and intent-test checklists.
