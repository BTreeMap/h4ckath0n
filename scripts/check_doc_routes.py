#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one. Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def generate_routes_markdown() -> str:
    from collections import defaultdict

    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    schema = app.openapi()

    paths = schema["paths"]
    tags = defaultdict(list)
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            tag = op.get("tags", ["default"])[0]
            summary = op.get("summary", "")
            tags[tag].append((method.upper(), path, summary))

    lines = []
    for tag in sorted(tags.keys()):
        lines.append(f"### {tag.capitalize()}")
        for method, path, summary in tags[tag]:
            lines.append(f"- `{method} {path}` — {summary}")
        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="Check or fix API routes documentation drift."
    )
    parser.add_argument("--fix", action="store_true", help="Fix README.md in-place.")
    args = parser.parse_args()

    expected_md = generate_routes_markdown()
    readme_text = README.read_text()

    pattern = re.compile(
        r"(<!-- BEGIN API ROUTES -->\n).*?(<!-- END API ROUTES -->)", re.DOTALL
    )

    if not pattern.search(readme_text):
        print(
            "❌ Could not find <!-- BEGIN API ROUTES --> and <!-- END API ROUTES --> in README.md."
        )
        return 1

    if args.fix:
        new_readme = pattern.sub(rf"\g<1>{expected_md}\n\g<2>", readme_text)
        README.write_text(new_readme)
        print("✅ Updated API routes in README.md.")
        return 0

    # Check for drift
    current_match = pattern.search(readme_text)
    if not current_match:
        print(
            "❌ Could not find <!-- BEGIN API ROUTES --> and <!-- END API ROUTES --> "
            "in README.md."
        )
        return 1

    current_md = (
        current_match.group(0)
        .replace("<!-- BEGIN API ROUTES -->\n", "")
        .replace("<!-- END API ROUTES -->", "")
    )

    if current_md.strip() != expected_md.strip():
        print("❌ API routes in README.md are out of sync with the codebase.")
        print("Run `uv run scripts/check_doc_routes.py --fix` to update it.")
        return 1

    print("✅ API routes in README.md match the codebase.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
