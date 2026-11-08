#!/usr/bin/env -S uv run python
"""Update the API route table in README.md dynamically."""

from __future__ import annotations

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)


def get_generated_table() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)

    routes: list[tuple[str, str, str]] = []
    paths = app.openapi().get("paths", {})
    for path, methods in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, details in methods.items():
            if method.upper() == "HEAD":
                continue
            routes.append((method.upper(), path, details.get("summary", "")))

    routes.sort(key=lambda x: (x[1], x[0]))

    lines = [
        "| Method | Path | Summary |",
        "|---|---|---|",
    ]
    for method, path, summary in routes:
        lines.append(f"| `{method}` | `{path}` | {summary} |")

    return "\n".join(lines) + "\n"


def main() -> int:
    readme_text = README.read_text()
    start_marker = "<!-- route-table-start -->\n"
    end_marker = "<!-- route-table-end -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("Markers not found in README.md")
        return 1

    start_idx = readme_text.index(start_marker) + len(start_marker)
    end_idx = readme_text.index(end_marker)

    new_table = get_generated_table()

    new_readme = readme_text[:start_idx] + new_table + readme_text[end_idx:]
    README.write_text(new_readme)
    print("✅ README.md route table updated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
