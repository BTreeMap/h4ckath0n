#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes in README.md are generated and up-to-date.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, generates a markdown list of all routes,
and ensures that README.md contains the exact generated text between
<!-- BEGIN ROUTES --> and <!-- END ROUTES -->.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def generate_routes_md() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    routes_by_tag: dict[str, list[str]] = {}
    for path, methods in paths.items():
        for method, op in methods.items():
            tags = op.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            if tag not in routes_by_tag:
                routes_by_tag[tag] = []

            summary = op.get("summary", "")
            routes_by_tag[tag].append(f"- `{method.upper()} {path}` — {summary}")

    lines: list[str] = []

    tags = sorted(routes_by_tag.keys())
    if "default" in tags:
        tags.remove("default")
        tags.insert(0, "default")

    for tag in tags:
        if tag != "default":
            title = tag.replace("-", " ").title()
            lines.append(f"### {title}\n")
        for route in routes_by_tag[tag]:
            lines.append(route)
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    expected_content = generate_routes_md()

    readme_text = README.read_text()

    begin_marker = "<!-- BEGIN ROUTES -->\n"
    end_marker = "<!-- END ROUTES -->"

    if begin_marker not in readme_text or end_marker not in readme_text:
        print(
            "❌ Could not find <!-- BEGIN ROUTES --> or <!-- END ROUTES --> in README.md"
        )
        return 1

    start_idx = readme_text.find(begin_marker) + len(begin_marker)
    end_idx = readme_text.find(end_marker)

    actual_content = readme_text[start_idx:end_idx]

    if actual_content == expected_content:
        print("✅ API routes in README.md are up-to-date.")
        return 0
    else:
        if args.update:
            new_readme_text = (
                readme_text[:start_idx] + expected_content + readme_text[end_idx:]
            )
            README.write_text(new_readme_text)
            print("✅ Updated API routes in README.md.")
            return 0
        else:
            print("❌ API routes in README.md are out of date.")
            print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
            return 1


if __name__ == "__main__":
    sys.exit(main())
