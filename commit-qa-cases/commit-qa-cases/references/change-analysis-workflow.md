# Change Analysis Workflow

Use this workflow before generating cases.

## 1. Classify Input

Classify the request as one or more of:

- Single commit
- Commit range
- Branch or PR diff
- Working-tree change
- Feature requirement
- Old cases plus new change

If the input is a requirement, identify the likely code areas with `rg` and repository structure before writing cases.

## 2. Inspect Source

For commits and ranges, inspect:

- `git show --stat --oneline <ref>`
- `git show --name-only <ref>`
- Relevant hunks with `git show --unified=<n> <ref> -- <files>`

For working-tree changes, inspect:

- `git status --short`
- `git diff --stat`
- Relevant `git diff -- <files>`

## 3. Confirm Final Behavior

Always inspect current final code after reading the diff. Later commits may have changed or removed intermediate behavior.

Use `rg` for symbols, log names, callbacks, event reporting, configuration flags, request calls, and state transitions.

## 4. Extract Business Impact

Summarize:

- New or changed user-visible flows
- Changed callback or API contract
- Changed logs, metrics, or event fields
- Success path
- Failure and fallback paths
- User cancellation or abandonment paths
- Retry, duplicate, concurrency, and lifecycle behavior
- External dependencies such as network, browser, WebView, disk, registry, process, thread, timer, or OS APIs
- Unclear or product-confirmation-needed behavior

## 5. Build Coverage Matrix

Create a compact matrix before final cases:

| Risk or behavior | Case IDs | Evidence | Notes |
|---|---|---|---|

Every P0 behavior should map to at least one case. If a P0 risk has no practical test path, call it out in `analysis.md`.
