#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py

The script imports the h4ckath0n app, enumerates all routes, and checks that
README.md mentions each one. Routes provided by FastAPI itself (e.g. /openapi.json,
/docs, /redoc) are excluded from the check.
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI paths omitted from user docs.
FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_app_routes() -> list[tuple[str, str]]:
    """Return (method, path) pairs from the live FastAPI app."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()
    paths = openapi.get("paths", {})

    routes: list[tuple[str, str]] = []
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method in sorted(methods.keys()):
            if method.upper() == "HEAD":
                continue
            routes.append((method.upper(), path))
    return sorted(routes)


def get_app_routes_markdown() -> str:
    """Generate the markdown text for the API routes from OpenAPI."""
    from collections import defaultdict

    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()
    paths = openapi.get("paths", {})

    routes_by_tag: dict[str, list[str]] = defaultdict(list)
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            tags = op.get("tags", ["default"])
            tag = tags[0] if tags else "default"
            if tag == "default":
                tag = "System"
            elif tag == "password-auth":
                tag = "Password Auth"
            else:
                tag = tag.title()

            summary = op.get("summary", "")
            method_upper = method.upper()
            routes_by_tag[tag].append(f"- `{method_upper} {path}` — {summary}")

    lines = []
    tag_order = ["System", "Auth", "Passkey", "Password Auth", "Jobs", "Uploads", "Llm"]

    for tag in tag_order:
        if tag not in routes_by_tag:
            continue
        lines.append(f"### {tag}\n")
        for route in routes_by_tag[tag]:
            lines.append(f"{route}\n")
        lines.append("\n")

    for tag in sorted(routes_by_tag.keys()):
        if tag in tag_order:
            continue
        lines.append(f"### {tag}\n")
        for route in routes_by_tag[tag]:
            lines.append(f"{route}\n")
        lines.append("\n")

    return "".join(lines).strip() + "\n"


def main() -> int:
    readme_text = README.read_text(encoding="utf-8")

    start_marker = "<!-- BEGIN ROUTES -->"
    end_marker = "<!-- END ROUTES -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print("❌ Error: README.md is missing route markers.", file=sys.stderr)
        return 1

    prefix = readme_text[: start_idx + len(start_marker)]
    suffix = readme_text[end_idx:]

    expected_content = "\n" + get_app_routes_markdown() + "\n"
    expected_readme = prefix + expected_content + suffix

    if readme_text != expected_readme:
        print(
            "❌ README.md API routes are out of date.\n\n"
            "The Built-in routes section is generated dynamically to prevent drift.\n"
            "Run 'uv run scripts/generate_doc_routes.py' to update README.md.",
            file=sys.stderr,
        )
        return 1

    routes = get_app_routes()
    print(f"✅ All {len(routes)} API routes are correctly generated in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
