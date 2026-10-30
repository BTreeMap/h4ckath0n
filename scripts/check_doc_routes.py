#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API route table in README.md is up to date.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script generates a markdown table of routes from the OpenAPI schema and checks
that the section between <!-- route-table-start --> and <!-- route-table-end -->
in README.md matches it exactly.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_openapi_routes_table() -> str:
    """Return the generated markdown table of routes from OpenAPI."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    paths = app.openapi().get("paths", {})
    routes: list[tuple[str, str, str]] = []

    for path, methods in paths.items():
        for method, info in methods.items():
            summary = info.get("summary", "")
            routes.append((method.upper(), path, summary))

    # Sort by path, then method
    routes.sort(key=lambda x: (x[1], x[0]))

    lines = [
        "| Method | Path | Description |",
        "|---|---|---|",
    ]
    for m, p, s in routes:
        lines.append(f"| `{m}` | `{p}` | {s} |")

    return "\n".join(lines)


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update",
        action="store_true",
        help="Update README.md with the generated table",
    )
    args = parser.parse_args()

    table_content = get_openapi_routes_table()
    readme_text = README.read_text()

    start_marker = "<!-- route-table-start -->"
    end_marker = "<!-- route-table-end -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(
            "❌ Markers <!-- route-table-start --> and "
            "<!-- route-table-end --> not found in README.md"
        )
        return 1

    prefix = readme_text[: start_idx + len(start_marker)]
    suffix = readme_text[end_idx:]
    current_table = readme_text[start_idx + len(start_marker) : end_idx].strip()

    if current_table == table_content:
        print("✅ API route table in README.md is up to date.")
        return 0

    if args.update:
        new_readme = f"{prefix}\n{table_content}\n{suffix}"
        README.write_text(new_readme)
        print("✅ Updated API route table in README.md.")
        return 0

    print(
        "❌ API route table in README.md is out of date. "
        "Run `uv run scripts/check_doc_routes.py --update` to fix."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
