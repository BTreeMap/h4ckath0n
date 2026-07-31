#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API routes in README.md are up-to-date.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, generates the expected route documentation
from the OpenAPI schema, and checks that it matches the block in README.md
between the <!-- BEGIN_API_ROUTES --> and <!-- END_API_ROUTES --> markers.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
BEGIN_MARKER = "<!-- BEGIN_API_ROUTES -->"
END_MARKER = "<!-- END_API_ROUTES -->"


def generate_routes_markdown() -> str:
    """Return generated markdown for all API routes based on OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    schema = app.openapi()

    routes_by_tag = defaultdict(list)
    for path, path_item in schema.get("paths", {}).items():
        for method, op in path_item.items():
            tags = op.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            heading = tag.replace("-", " ").title()
            if heading == "Default":
                heading = "General"

            summary = op.get("summary", "")
            if summary:
                summary = summary.replace("\n", " ")
            routes_by_tag[heading].append((method.upper(), path, summary))

    lines = []
    for heading in sorted(routes_by_tag.keys()):
        lines.append(f"### {heading}")
        lines.append("")
        for method, path, summary in sorted(routes_by_tag[heading]):
            if summary:
                lines.append(f"- `{method} {path}` — {summary}")
            else:
                lines.append(f"- `{method} {path}`")
        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md in place")
    args = parser.parse_args()

    readme_text = README.read_text()
    if BEGIN_MARKER not in readme_text or END_MARKER not in readme_text:
        print(f"❌ {BEGIN_MARKER} or {END_MARKER} missing in README.md")
        return 1

    start_idx = readme_text.find(BEGIN_MARKER) + len(BEGIN_MARKER)
    end_idx = readme_text.find(END_MARKER)

    expected_md = "\n" + generate_routes_markdown() + "\n"
    current_md = readme_text[start_idx:end_idx]

    if current_md == expected_md:
        print("✅ API routes in README.md are up-to-date.")
        return 0

    if args.update:
        new_text = readme_text[:start_idx] + expected_md + readme_text[end_idx:]
        README.write_text(new_text)
        print("✅ Updated API routes in README.md.")
        return 0

    print("❌ API routes in README.md are out of date.")
    print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
