#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that API routes in README.md match the live app.

Usage (from repo root):
    uv run scripts/check_doc_routes.py
    uv run scripts/check_doc_routes.py --update
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

FRAMEWORK_PATHS = frozenset(
    {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
)

TAG_ORDER = ["", "passkey", "password-auth", "auth", "jobs", "uploads", "llm"]
TAG_NAMES = {
    "": "Base",
    "passkey": "Passkeys",
    "password-auth": "Password Auth",
    "auth": "Session",
    "jobs": "Background Jobs",
    "uploads": "Uploads",
    "llm": "LLM Chat",
}


def generate_routes_markdown() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(database_url="sqlite+aiosqlite://", password_auth_enabled=True)
    app = create_app(settings)

    routes_by_tag = defaultdict(list)
    paths = app.openapi().get("paths", {})

    for path, path_item in paths.items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in path_item.items():
            tags = op.get("tags", [""])
            tag = tags[0] if tags else ""
            summary = op.get("summary", "")
            routes_by_tag[tag].append((method.upper(), path, summary))

    # Identify any tags not in TAG_ORDER
    unknown_tags = set(routes_by_tag.keys()) - set(TAG_ORDER)
    if unknown_tags:
        raise ValueError(f"Unknown tags found in OpenAPI schema: {unknown_tags}. Please add them to TAG_ORDER.")

    lines = []
    for tag in TAG_ORDER:
        if tag not in routes_by_tag:
            continue

        group_name = TAG_NAMES.get(tag, tag.title())
        lines.append(f"### {group_name}")
        lines.append("")
        lines.append("| Method | Path | Description |")
        lines.append("|--------|------|-------------|")

        for method, path, summary in sorted(routes_by_tag[tag], key=lambda x: x[1]):
            lines.append(f"| `{method}` | `{path}` | {summary} |")

        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--update", action="store_true")
    args = parser.parse_args()

    readme_text = README.read_text(encoding="utf-8")

    start_marker = "<!-- BEGIN GENERATED ROUTES -->"
    end_marker = "<!-- END GENERATED ROUTES -->"

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker)

    if start_idx == -1 or end_idx == -1:
        print(f"❌ Could not find {start_marker} and {end_marker} in README.md")
        return 1

    generated_content = generate_routes_markdown()
    expected_section = f"{start_marker}\n\n{generated_content}\n\n{end_marker}"

    actual_section = readme_text[start_idx : end_idx + len(end_marker)]

    if actual_section == expected_section:
        print("✅ API routes in README.md are up to date.")
        return 0

    if args.update:
        new_readme = (
            readme_text[:start_idx]
            + expected_section
            + readme_text[end_idx + len(end_marker) :]
        )
        README.write_text(new_readme, encoding="utf-8")
        print("✅ Updated README.md with latest API routes.")
        return 0

    print("❌ API routes in README.md are out of date.")
    print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
