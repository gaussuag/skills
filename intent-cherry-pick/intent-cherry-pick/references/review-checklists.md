# intent-cherry-pick Review Checklists

Use these checklists when planning, prechecking, implementing, and checking an intent cherry-pick.

## Planning Checklist

- Identify source branch, source commit/range, target branch, and requested scope.
- Read source commit message and diff.
- Read source parent for changed files when needed.
- Inspect target equivalents before planning edits.
- Expand call chains when callbacks, public APIs, events, threads, global state, or multiple similar entry points are involved.
- Check git history when behavior is ambiguous, target/source implementations diverge, or code looks like compatibility logic.
- Produce Source Fact Lock and Target Fact Lock.
- Classify each source hunk/fact as L0, L1, L2, or L3.
- Mark L2/L3 items as requiring explicit human confirmation.
- State skipped source hunks and why.
- State expected deviations from source shape.
- Define code-review-level Intent Tests.

## Precheck Checklist

Precheck must independently inspect code facts and may not simply accept the plan.

- Does the plan preserve source implementation facts?
- Does the plan protect target branch facts?
- Is any source hunk or fact missing?
- Is any out-of-scope source dependency being imported?
- Is target mapping correct?
- Are fidelity levels correct?
- Are all L2/L3 adaptations explicitly confirmed by the human?
- Does the plan contain optimization, refactoring, renaming, cleanup, formatting churn, or scope expansion?
- Does the plan avoid pushing temporary branches to remotes?
- Are Intent Tests sufficient?

Return only:

- `PASS`
- `PASS_WITH_NOTES`
- `BLOCK`

If `BLOCK`, state evidence and the human decision needed. Do not prescribe a new unapproved implementation.

## Intent Test Checklist

Perform after implementation without running builds or project tests by default.

- Source Fact Preservation Test: every applicable source fact is present in the result.
- Target Fact Preservation Test: protected target facts remain true.
- Scope Boundary Test: changed files and behavior match approved scope.
- Fidelity Test: actual diff matches approved L0/L1/L2/L3 classifications.
- Call-chain Reasoning Test: relevant call paths support the intended behavior.
- Negative Path Test: paths not changed by the source intent remain unchanged.
- No-improvement Test: no opportunistic optimization, refactor, rename, cleanup, broad formatting, or expanded behavior exists.
- Record Consistency Test: plan, diff, record, and commit appendix agree.

## Check Checklist

Check must independently inspect actual diff and relevant code facts.

- Is the actual diff faithful to the approved Fusion Plan?
- Are Source Fact Lock items preserved?
- Are Target Fact Lock items protected?
- Are any target facts implicitly superseded?
- Did implementation introduce unapproved L2/L3 adaptation?
- Did implementation import excluded dependencies or source-branch-only code?
- Did implementation add optimization, refactoring, renaming, cleanup, broad formatting, or scope expansion?
- Were Intent Tests performed at code-review level?
- Is the workflow record accurate and precise?
- Is the commit message appendix short and correctly linked to the record?
- If merge-back completed, was the local temporary branch safely cleaned up or intentionally kept with a reason?

Return only:

- `PASS`
- `PASS_WITH_NOTES`
- `BLOCK`

If `BLOCK`, state exact deviations and the human decision needed. Do not authorize automatic self-repair.
