# Base Case Policy

`docs/qa-case/base-case` stores durable project-level QA cases that should survive individual commits.

## Promote to Base Case When

- It covers a core business flow that should be regressed often.
- It is important for release confidence.
- It does not depend on a one-off commit detail.
- The expected behavior is stable and confirmed by code or product requirements.
- It applies to a module, feature family, or exported SDK capability.

## Do Not Promote When

- It only verifies a temporary compatibility branch.
- It depends on one specific bug reproduction that is not a permanent contract.
- It is product-ambiguous or still under discussion.
- It is too implementation-specific to remain stable.

## Storage

Store base cases by module:

```text
docs/qa-case/base-case/<module>/base-cases.json
docs/qa-case/base-case/<module>/base-cases.md
```

Use `scripts/update_base_cases.py` for JSON merging when possible. Mention every base-case add or update in the final response.
