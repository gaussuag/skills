#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


REQUIRED_CASE_FIELDS = [
    "id",
    "title",
    "priority",
    "area",
    "step",
    "trigger",
    "expected",
    "logs",
]

ALLOWED_PRIORITIES = {"P0", "P1", "P2"}
ALLOWED_CHANGE_STATES = {"new", "changed", "unchanged", "deprecated", "moved-to-base", ""}


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        return {"schema_version": "1.0", "cases": data}
    if not isinstance(data, dict):
        raise ValueError("root must be an object or a list of cases")
    return data


def validate(data):
    errors = []
    cases = data.get("cases")
    if not isinstance(cases, list):
        return ["root.cases must be a list"], []

    seen = set()
    for index, case in enumerate(cases):
        where = f"cases[{index}]"
        if not isinstance(case, dict):
            errors.append(f"{where} must be an object")
            continue

        for field in REQUIRED_CASE_FIELDS:
            value = case.get(field)
            if value is None or str(value).strip() == "":
                errors.append(f"{where}.{field} is required")

        case_id = str(case.get("id", "")).strip()
        if case_id:
            if case_id in seen:
                errors.append(f"{where}.id duplicates {case_id}")
            seen.add(case_id)

        priority = str(case.get("priority", "")).strip()
        if priority and priority not in ALLOWED_PRIORITIES:
            errors.append(f"{where}.priority must be one of {sorted(ALLOWED_PRIORITIES)}")

        change_state = str(case.get("change_state", "")).strip()
        if change_state not in ALLOWED_CHANGE_STATES:
            errors.append(f"{where}.change_state must be one of {sorted(ALLOWED_CHANGE_STATES - {''})}")

        evidence = case.get("evidence", [])
        if evidence and not isinstance(evidence, list):
            errors.append(f"{where}.evidence must be a list when present")

    return errors, cases


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate commit-qa-cases test-cases.json")
    parser.add_argument("json_path", type=Path)
    args = parser.parse_args(argv)

    try:
        data = load_json(args.json_path)
        errors, cases = validate(data)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(cases)} cases validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
