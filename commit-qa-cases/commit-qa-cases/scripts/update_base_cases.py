#!/usr/bin/env python3
import argparse
import json
import re
from pathlib import Path


def load_json(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        return {"schema_version": "1.0", "cases": data}
    return data


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return value.strip("-") or "general"


def case_to_markdown(case):
    lines = [
        f"### {case.get('id', '')} {case.get('title', '')}".rstrip(),
        "",
        f"- Priority: {case.get('priority', '')}",
        f"- Area: {case.get('area', '')}",
        f"- Type: {case.get('case_type', 'base')}",
        f"- Step: {case.get('step', '')}",
        f"- Trigger: {case.get('trigger', '')}",
        f"- Expected: {case.get('expected', '')}",
        f"- Logs: {case.get('logs', '')}",
    ]
    reason = case.get("base_reason", "")
    if reason:
        lines.append(f"- Base reason: {reason}")
    return "\n".join(lines)


def write_markdown(path: Path, module: str, cases):
    lines = [f"# Base QA Cases: {module}", ""]
    for case in cases:
        lines.append(case_to_markdown(case))
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8-sig")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Merge base_candidate cases into docs/qa-case/base-case")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("base_case_root", type=Path)
    parser.add_argument("--module", default="")
    parser.add_argument("--bom", action="store_true", help="write JSON as UTF-8 with BOM")
    args = parser.parse_args(argv)

    data = load_json(args.json_path)
    module = slugify(args.module or data.get("module") or "general")
    target_dir = args.base_case_root / module
    target_dir.mkdir(parents=True, exist_ok=True)
    json_path = target_dir / "base-cases.json"
    md_path = target_dir / "base-cases.md"

    existing = {"schema_version": "1.0", "module": module, "cases": []}
    if json_path.exists():
        existing = load_json(json_path)
        existing.setdefault("cases", [])
        existing["module"] = module

    by_id = {str(case.get("id")): case for case in existing.get("cases", []) if case.get("id")}
    added = 0
    updated = 0
    for case in data.get("cases", []):
        if not case.get("base_candidate"):
            continue
        if case.get("change_state") == "deprecated":
            continue
        merged = dict(case)
        merged["case_type"] = "base"
        merged["change_state"] = "unchanged"
        case_id = str(merged.get("id", "")).strip()
        if not case_id:
            continue
        if case_id in by_id:
            updated += 1
        else:
            added += 1
        by_id[case_id] = merged

    cases = sorted(by_id.values(), key=lambda item: str(item.get("id", "")))
    existing["cases"] = cases
    encoding = "utf-8-sig" if args.bom else "utf-8"
    json_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding=encoding)
    write_markdown(md_path, module, cases)
    print(f"OK: base cases module={module} added={added} updated={updated} total={len(cases)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
