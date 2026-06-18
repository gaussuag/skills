# Intent Cherry-Pick Record

Use this template for durable repository records under:

```text
docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<source-short-hash>-to-<target-branch>.md
```

Keep headings in English. Write section body text in the dominant language of the triggering human prompt. Preserve source commit messages exactly.

## Summary

- Source Branch:
- Source Commit:
- Source Range:
- Target Branch:
- Result Branch:
- Final Commit:
- Status:
- Date:

Briefly state what was ported and whether the workflow completed.

## Source Commit

- Hash:
- Branch:
- Parent:

```text
<original source commit title and body, unchanged>
```

## Scope

- Included:
- Excluded:
- Explicit Non-goals:
- Allowed Files/Modules:
- Do Not Port:

## Intent

- Problem:
- Source Before Behavior:
- Source After Behavior:
- Required Facts:
- Non-goals:

## Source Fact Lock

List implementation and behavior facts introduced or changed by the source commit.

## Target Fact Lock

List target branch facts that must remain true after the port.

## Evidence Reviewed

- Diff:
- Source Parent:
- Target Code:
- Call Chains:
- Git History:
- Related Symbols:
- Related Tests or Examples:
- Uncertainties:

## Fidelity Classification

For each source hunk or source fact:

- Item:
- Level: L0 / L1 / L2 / L3
- Reason:
- Human Confirmation Required:
- Human Confirmation Status:

## Fusion Plan

- Files:
- Strategy:
- Expected Source-shape Deviations:
- Skipped Source Hunks:
- Target Facts Protected:

## Precheck

- Result: PASS / PASS_WITH_NOTES / BLOCK
- Reviewer: independent / self-precheck
- Findings:
- Human Direction Required:

## Human Decisions

Record only decisions relevant to scope, intent, L2/L3 approval, review blocks, or merge/commit policy.

## Implementation

- Changed Files:
- Adaptations:
- Skipped Source Hunks:
- Deviations From Source Shape:
- Target Facts Intentionally Superseded:

## Intent Tests

- Source Fact Preservation Test:
- Target Fact Preservation Test:
- Scope Boundary Test:
- Fidelity Test:
- Call-chain Reasoning Test:
- Negative Path Test:
- No-improvement Test:
- Record Consistency Test:

Do not report unrun builds or tests as passed.

## Check

- Result: PASS / PASS_WITH_NOTES / BLOCK
- Reviewer: independent / self-check
- Findings:
- Human Direction Required:

## Cleanup

- Temporary Branch:
- Remote Tracking:
- Local Branch Deleted:
- Remote Branch Deleted: no
- Reason If Kept:

Record whether the local workflow branch was safely deleted after merge back. This workflow must not push or delete remote branches.

## Remaining Risks

List residual code-review-level risks and human-run validation still needed.
