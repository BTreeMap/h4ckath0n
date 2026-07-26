#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--fix]

The script imports the h4ckath0n app, extracts all routes via OpenAPI, and verifies
that the Markdown table under "Built-in routes" in README.md is completely in sync.
If out of sync and --fix is passed, it overwrites the generated table in README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def get_app_routes_table() -> str:
    """Return the generated Markdown table for API routes."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    lines = ["| Method | Path | Summary |", "|---|---|---|"]
    paths = app.openapi().get("paths", {})

    for path, methods in sorted(paths.items()):
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in sorted(methods.items()):
            summary = details.get("summary", "")
            lines.append(f"| `{method.upper()}` | `{path}` | {summary} |")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify or fix API routes documentation.")
    parser.add_argument("--fix", action="store_true", help="Fix README.md in-place")
    args = parser.parse_args()

    readme_content = README.read_text()

    marker_start = "<!-- BEGIN API_ROUTES -->"
    marker_end = "<!-- END API_ROUTES -->"

    if marker_start not in readme_content or marker_end not in readme_content:
        print(
            "❌ Markers <!-- BEGIN API_ROUTES --> or <!-- END API_ROUTES --> "
            "not found in README.md."
        )
        return 1

    before = readme_content.split(marker_start)[0]
    after = readme_content.split(marker_end)[1]

    expected_table = get_app_routes_table()
    expected_content = f"{before}{marker_start}\n{expected_table}\n{marker_end}{after}"

    if readme_content != expected_content:
        if args.fix:
            README.write_text(expected_content)
            print("✅ README.md updated with accurate API routes.")
            return 0
        else:
            print("❌ README.md API routes are out of sync.")
            print("Run `uv run scripts/check_doc_routes.py --fix` to update.")
            return 1

    print("✅ API routes in README.md are fully up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
