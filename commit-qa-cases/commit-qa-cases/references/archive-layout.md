# Archive Layout

All generated QA assets live under the repository workspace:

```text
docs/
  qa-case/
    base-case/
    <run-slug>/
      source.json
      analysis.md
      test-cases.json
      test-cases.md
      test-cases.html
```

Create `docs/qa-case` if it does not exist.

## Run Slug

Use:

```text
YYYY-MM-DD-<module-or-feature>-<short-ref-or-kind>
```

Examples:

- `2026-06-18-overseas-payment-c85a700`
- `2026-06-18-webview-runtime-feature`
- `2026-06-18-login-working-tree`

Keep slugs lowercase and filesystem-safe. If a folder exists, append `-2`, `-3`, etc.

## Required Files

- `source.json`: source type, refs, commands or inputs inspected, assumptions, generated time.
- `analysis.md`: business impact, evidence, coverage matrix, base-case decisions.
- `test-cases.json`: canonical structured cases.
- `test-cases.md`: readable QA cases.
- `test-cases.html`: interactive execution page when requested or useful.

## Encoding

Follow repository rules. If the current repo requires UTF-8 with BOM for new files, write generated docs with BOM.
