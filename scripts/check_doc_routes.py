#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that the API route list in README.md matches the app.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, enumerates all routes using the OpenAPI schema,
generates a markdown list of routes, and checks that README.md contains this exact
list between <!-- BEGIN ROUTES --> and <!-- END ROUTES --> markers.
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def generate_routes_markdown() -> str:
    """Generate the markdown list of routes from the OpenAPI schema."""
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes_by_tag = defaultdict(list)
    paths = app.openapi().get("paths", {})

    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, spec in methods.items():
            method = method.upper()
            summary = spec.get("summary", "")
            tags = spec.get("tags", [])
            tag = tags[0] if tags else "default"
            routes_by_tag[tag].append((method, path, summary))

    groups = [
        ("default", "Misc"),
        ("auth", "Session"),
        ("passkey", "Passkey Authentication"),
        ("password-auth", "Password Authentication (Optional)"),
        ("jobs", "Background Jobs"),
        ("uploads", "Uploads"),
        ("llm", "LLM Chat"),
    ]

    known_tags = {tag for tag, _ in groups}
    unmapped_tags = set(routes_by_tag.keys()) - known_tags
    if unmapped_tags:
        for tag in sorted(unmapped_tags):
            groups.append((tag, f"Other: {tag.capitalize()}"))

    out = []
    for tag, title in groups:
        if tag not in routes_by_tag:
            continue
        out.append(f"### {title}\n")
        for method, path, summary in sorted(
            routes_by_tag[tag], key=lambda x: (x[1], x[0])
        ):
            desc = f" — {summary}" if summary else ""
            out.append(f"- `{method} {path}`{desc}")
        out.append("")

    return "\n".join(out).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--update", action="store_true", help="Update README.md in place"
    )
    args = parser.parse_args()

    readme_text = README.read_text()
    generated_md = generate_routes_markdown()

    start_marker = "<!-- BEGIN ROUTES -->\n"
    end_marker = "<!-- END ROUTES -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print(
            "❌ README.md is missing <!-- BEGIN ROUTES --> or <!-- END ROUTES --> markers."
        )
        return 1

    start_idx = readme_text.find(start_marker) + len(start_marker)
    end_idx = readme_text.find(end_marker)

    current_md = readme_text[start_idx:end_idx].strip()

    if current_md == generated_md:
        print("✅ API routes in README.md are up to date.")
        return 0

    if args.update:
        new_readme = (
            readme_text[:start_idx] + generated_md + "\n" + readme_text[end_idx:]
        )
        README.write_text(new_readme)
        print("✅ README.md updated with latest API routes.")
        return 0

    print("❌ API routes in README.md are out of date.")
    print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
