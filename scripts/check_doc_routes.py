#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes in README.md are up to date.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--fix]

The script imports the h4ckath0n app, enumerates all routes using OpenAPI,
generates a markdown list of routes, and checks that README.md contains
exactly this generated block between <!-- BEGIN ROUTES --> and <!-- END ROUTES -->.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_app_routes_markdown() -> str:
    """Generate markdown list of routes from the live FastAPI app's OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    grouped: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    for path, methods in paths.items():
        for method, op in methods.items():
            tags = op.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            # Title case the tag, replacing hyphens with spaces for readability
            tag_name = tag.replace("-", " ").title()
            if tag_name == "Default":
                tag_name = "Core"
            elif tag_name == "Llm":
                tag_name = "LLM"
            grouped[tag_name].append((method.upper(), path, op.get("summary", "")))

    lines = []
    for tag in sorted(grouped.keys()):
        lines.append(f"### {tag}")
        for method, path, summary in grouped[tag]:
            lines.append(f"- `{method} {path}` — {summary}")
        lines.append("")

    return "\n".join(lines).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fix", action="store_true", help="Update README.md with generated routes"
    )
    args = parser.parse_args()

    generated_md = get_app_routes_markdown()
    readme_text = README.read_text(encoding="utf-8")

    begin_marker = "<!-- BEGIN ROUTES -->\n"
    end_marker = "<!-- END ROUTES -->"

    if begin_marker not in readme_text or end_marker not in readme_text:
        print(f"❌ Could not find {begin_marker.strip()} or {end_marker} in README.md")
        return 1

    before, rest = readme_text.split(begin_marker, 1)
    old_content, after = rest.split(end_marker, 1)

    new_readme_text = f"{before}{begin_marker}{generated_md}{end_marker}{after}"

    if readme_text != new_readme_text:
        if args.fix:
            README.write_text(new_readme_text, encoding="utf-8")
            print("✅ Updated README.md with generated API routes.")
            return 0
        else:
            print("❌ API routes in README.md are out of date!")
            print("Run `uv run scripts/check_doc_routes.py --fix` to update them.")
            return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
