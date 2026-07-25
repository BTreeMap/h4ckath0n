#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, enumerates all routes using the OpenAPI schema,
and ensures that the generated routes exactly match the content between the
<!-- ROUTE_LIST_START --> and <!-- ROUTE_LIST_END --> markers in README.md.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

# FastAPI internal paths that we do not require in user docs.
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def get_openapi_routes() -> dict[str, list[tuple[str, str, str]]]:
    """Extract routes grouped by tag from the live FastAPI OpenAPI schema."""
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    paths = app.openapi().get("paths", {})

    routes_by_tag: dict[str, list[tuple[str, str, str]]] = {}
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in methods.items():
            if method.upper() == "HEAD":
                continue
            tags = details.get("tags", [])
            tag = tags[0] if tags else "default"
            if tag not in routes_by_tag:
                routes_by_tag[tag] = []
            routes_by_tag[tag].append((method.upper(), path, details.get("summary", "")))

    return {k: sorted(v, key=lambda x: x[1]) for k, v in routes_by_tag.items()}


def generate_routes_markdown(routes_by_tag: dict[str, list[tuple[str, str, str]]]) -> str:
    """Generate the markdown text for the routes."""
    lines = []
    tag_order = ["default", "auth", "passkey", "password-auth", "jobs", "uploads", "llm"]
    tags = sorted(
        routes_by_tag.keys(),
        key=lambda t: tag_order.index(t) if t in tag_order else len(tag_order),
    )

    for tag in tags:
        routes = routes_by_tag[tag]
        tag_title = tag.replace("-", " ").title()
        if tag.lower() == "default":
            lines.append("### Core")
        elif tag.lower() == "llm":
            lines.append("### LLM Chat")
        elif tag.lower() == "passkey":
            lines.append("### Passkeys")
        else:
            lines.append(f"### {tag_title}")

        for method, path, summary in routes:
            description = f" — {summary}" if summary else ""
            lines.append(f"- `{method} {path}`{description}")
        lines.append("")
    return "\n".join(lines).strip()


def extract_routes_from_readme() -> str:
    readme_text = README.read_text()
    start_marker = "<!-- ROUTE_LIST_START -->\n"
    end_marker = "\n<!-- ROUTE_LIST_END -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        return None

    return readme_text[start_idx + len(start_marker) : end_idx].strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true", help="Update README.md in place.")
    args = parser.parse_args()

    routes_by_tag = get_openapi_routes()
    generated = generate_routes_markdown(routes_by_tag)
    current = extract_routes_from_readme()

    if current is None:
        print("❌ Could not find markers.")
        return 1

    if current != generated:
        if args.update:
            readme_text = README.read_text()
            start_marker = "<!-- ROUTE_LIST_START -->\n"
            end_marker = "\n<!-- ROUTE_LIST_END -->"
            start_idx = readme_text.find(start_marker)
            end_idx = readme_text.find(end_marker)

            new_readme_text = (
                readme_text[: start_idx + len(start_marker)] + generated + readme_text[end_idx:]
            )
            README.write_text(new_readme_text)
            print("✅ Updated API routes in README.md.")
            return 0
        else:
            print("❌ API routes in README.md are out of date or incorrectly formatted.")
            print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
            return 1

    print("✅ All API routes are documented correctly in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
