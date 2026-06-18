---
name: commit-qa-cases
description: Use only when the user explicitly invokes commit-qa-cases or asks to use this skill to generate or update QA test cases from commits, commit ranges, diffs, working-tree changes, feature requirements, or code changes. Analyze current repository behavior and business impact, archive structured QA cases under docs/qa-case, update base cases when appropriate, and optionally render an interactive HTML test-case page. Do not use for general testing questions unless explicitly requested.
---

# Commit QA Cases

## Purpose

Generate durable QA test-case assets from code changes or feature requirements. Treat commits, diffs, and requirements as input clues; write test cases against the current repository behavior and the user's stated business intent.

This skill is explicitly invoked only. Do not use it for casual QA discussion, code review, debugging, or generic testing questions unless the user names this skill or asks to trigger it.

## Required Workflow

1. Confirm the input type: commit, commit range, diff, working-tree change, PR/branch comparison, feature requirement, or old cases plus new change.
2. Read repository instructions such as `AGENTS.md` before writing files.
3. Inspect the change source, then inspect the current final code for the affected behavior. Do not rely on diff hunks alone.
4. Produce a business-impact analysis: changed user flows, success paths, failure paths, callbacks, logs, lifecycle behavior, external dependencies, regressions, and unresolved assumptions.
5. Generate a coverage matrix before final cases. Each important behavior or risk should map to at least one test case.
6. Write cases using the schema in `references/testcase-schema.md`.
7. Archive outputs under `docs/qa-case/<run-slug>/`. Create `docs/qa-case/` if needed. Follow `references/archive-layout.md`.
8. Evaluate base-case candidates. Update `docs/qa-case/base-case/` only for durable, important cases. Follow `references/base-case-policy.md`.
9. Render Markdown and, unless the user opts out, an interactive HTML page from the structured cases.
10. Validate generated artifacts and report exactly what checks ran.

## Analysis Rules

- A commit is a locator, not the source of truth. If later commits changed the behavior, use the current final behavior and mention the difference.
- For runtime SDK or client business changes, cover slow, failed, partial, duplicate, canceled, concurrent, and lifecycle-interrupted paths, not only success.
- For logging-sensitive requests, include expected log chain assertions and enough fields for QA to search failures.
- Do not invent exact log names, callback codes, API fields, or business statuses unless confirmed from code or user-provided requirements.
- Preserve existing user-authored cases when updating. Mark cases as unchanged, changed, new, deprecated, or moved-to-base where appropriate.

## Outputs

Create these files for every run:

- `source.json`: input source, commit refs, requirement summary, date, and assumptions.
- `analysis.md`: business changes, risks, code evidence, coverage matrix, and base-case decisions.
- `test-cases.json`: canonical structured cases.
- `test-cases.md`: readable QA document.
- `test-cases.html`: interactive page when HTML output is requested or useful.

## Resources

- Read `references/change-analysis-workflow.md` for commit/diff/requirement analysis steps.
- Read `references/qa-generation-rules.md` before writing cases.
- Read `references/testcase-schema.md` before producing JSON.
- Read `references/archive-layout.md` before creating files under `docs/qa-case`.
- Read `references/base-case-policy.md` before changing `docs/qa-case/base-case`.
- Read `references/sdk-runtime-risk-checklist.md` when the changed code affects SDK runtime behavior.
- Use `scripts/render_testcase_html.py` to render `test-cases.html` from `test-cases.json`.
- Use `scripts/validate_testcase_json.py` to validate structured cases.
- Use `scripts/update_base_cases.py` to merge approved base-case candidates.

## Validation

Run the lightweight checks appropriate to the repo and outputs:

- Validate `test-cases.json` with `scripts/validate_testcase_json.py`.
- Render HTML with `scripts/render_testcase_html.py` when HTML output is generated.
- Check generated HTML script syntax when Node.js is available.
- Run `git diff --check` for modified files in the workspace.
- If repo rules require encoding such as UTF-8 with BOM for new files, verify it.
- Do not claim a full build passed unless one was actually run.
