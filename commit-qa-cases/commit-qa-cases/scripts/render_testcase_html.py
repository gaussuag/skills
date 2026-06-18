#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent
DEFAULT_TEMPLATE = SKILL_DIR / "assets" / "interactive-testcase-template.html"


def load_cases(path: Path):
    with path.open("r", encoding="utf-8-sig") as handle:
        data = json.load(handle)
    if isinstance(data, list):
        data = {"schema_version": "1.0", "title": "QA Test Cases", "cases": data}
    if "cases" not in data or not isinstance(data["cases"], list):
        raise ValueError("input JSON must contain a cases list")
    return data


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    return value.strip("-") or "qa-cases"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render interactive HTML from test-cases.json")
    parser.add_argument("json_path", type=Path)
    parser.add_argument("output_html", type=Path)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--title", default="")
    parser.add_argument("--summary", default="")
    parser.add_argument("--bom", action="store_true", help="write UTF-8 with BOM")
    args = parser.parse_args(argv)

    data = load_cases(args.json_path)
    template = args.template.read_text(encoding="utf-8-sig")

    title = args.title or data.get("title") or "QA Test Cases"
    summary = args.summary or data.get("summary") or data.get("source", {}).get("summary") or "Interactive QA test-case execution page."
    data.setdefault("storage_key", slugify(f"{title}-{args.output_html.stem}"))

    json_text = json.dumps(data, ensure_ascii=False, indent=2).replace("</", "<\\/")
    rendered = (
        template.replace("__TITLE__", html.escape(title))
        .replace("__SUMMARY__", html.escape(summary))
        .replace("__CASES_JSON__", json_text)
    )

    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    encoding = "utf-8-sig" if args.bom else "utf-8"
    args.output_html.write_text(rendered, encoding=encoding)
    print(f"OK: rendered {len(data['cases'])} cases to {args.output_html}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
