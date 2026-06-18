# Test Case Schema

Use this schema for `test-cases.json`. Prefer an object wrapper so metadata can grow without changing the case list shape.

```json
{
  "schema_version": "1.0",
  "title": "Feature or change title",
  "module": "payment",
  "source": {
    "type": "commit|range|diff|working-tree|feature|requirement|mixed",
    "refs": ["abc123"],
    "summary": "Input summary"
  },
  "cases": [
    {
      "id": "OP-01",
      "title": "Short test case title",
      "priority": "P0|P1|P2",
      "area": "Business area",
      "case_type": "base|change|regression|negative|lifecycle|logging",
      "change_state": "new|changed|unchanged|deprecated|moved-to-base",
      "base_candidate": false,
      "base_reason": "",
      "step": "Business-level step or flow being validated",
      "trigger": "Operation, input, environment, or fault injection",
      "expected": "Expected business result",
      "logs": "Expected searchable log chain or fields",
      "evidence": [
        {
          "file": "relative/path.cpp",
          "line": 123,
          "reason": "Why this code supports the case"
        }
      ],
      "notes": ""
    }
  ]
}
```

Required per case: `id`, `title`, `priority`, `area`, `step`, `trigger`, `expected`, `logs`.

Allowed status fields are for planning only. Interactive execution status is stored separately by the HTML page, not in the canonical cases.

ID guidance:

- Preserve existing IDs when updating old cases.
- Allocate new IDs with the module prefix already in use, such as `OP-22`.
- Avoid renumbering existing cases unless the user asks.

Priority guidance:

- `P0`: core success path, money movement, callback contract, data loss, unrecoverable failure, or critical log visibility.
- `P1`: important negative, lifecycle, fallback, compatibility, or regression path.
- `P2`: low-risk UI detail, rare edge case, or optional observability check.
