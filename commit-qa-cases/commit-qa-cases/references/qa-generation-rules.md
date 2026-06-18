# QA Generation Rules

Generate business-level cases, not line-by-line code cases.

## Case Requirements

Each case should include:

- Business scenario
- Operation or trigger condition
- Expected business result
- Expected logs or observability
- Code evidence when generated from code changes

## Coverage Requirements

Cover these paths when relevant:

- Primary success path
- Business failure path
- Network or external dependency failure
- Empty, malformed, or missing server response
- User cancellation or close path
- Fallback or degradation path
- Duplicate invocation or replacement path
- Lifecycle interruption such as uninit, destroy, process exit, or page close
- Logging-only abnormal path
- Regression path for unchanged base functionality

## Precision Rules

- Do not invent exact log names, callback codes, server fields, or config keys without evidence.
- If behavior is inferred from code, say it is inferred and cite the evidence.
- If behavior is product-ambiguous, create a case with `notes` explaining the assumption.
- Prefer stable business steps over implementation details in `step`.

## Updating Existing Cases

When old cases are supplied:

- Preserve valid cases.
- Modify expected results and logs when behavior changed.
- Mark obsolete cases as `deprecated` instead of silently deleting them when useful for review.
- Add new cases for new risks.
- Keep IDs stable.
