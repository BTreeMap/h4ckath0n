#!/usr/bin/env -S uv run python
"""Update the API routes section in README.md from the OpenAPI schema."""

from __future__ import annotations

import collections
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_openapi_routes() -> str:
    """Generate Markdown for API routes from the live FastAPI app."""
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    openapi_paths = app.openapi().get("paths", {})

    tags_to_routes = collections.defaultdict(list)

    for path, path_item in openapi_paths.items():
        if path in {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}:
            continue
        for method, op in path_item.items():
            method_upper = method.upper()
            if method_upper == "HEAD":
                continue
            tags = op.get("tags", ["default"])
            summary = op.get("summary", "")
            tags_to_routes[tags[0]].append((method_upper, path, summary))

    lines = []
    for tag, routes in sorted(tags_to_routes.items()):
        tag_name = tag.replace("-", " ").title()
        if tag == "default" or not tag:
            tag_name = "Core"
        lines.append(f"### {tag_name}")
        for method, path, summary in routes:
            if summary:
                lines.append(f"- `{method} {path}` — {summary.lower()}")
            else:
                lines.append(f"- `{method} {path}`")
        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    readme_text = README.read_text()

    start_marker = "<!-- api-routes-start -->"
    end_marker = "<!-- api-routes-end -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print(f"Error: Could not find {start_marker} and {end_marker} in README.md")
        return 1

    generated = get_openapi_routes()

    pattern = re.compile(rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}", re.DOTALL)
    new_text = pattern.sub(f"{start_marker}\n\n{generated}\n\n{end_marker}", readme_text)

    if new_text != readme_text:
        README.write_text(new_text)
        print("Updated README.md with generated API routes.")
    else:
        print("README.md API routes are already up to date.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
