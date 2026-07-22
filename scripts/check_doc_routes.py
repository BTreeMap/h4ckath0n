#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that every API route in the FastAPI app is documented.

Usage (from repo root):
    uv run scripts/check_doc_routes.py [--update]

The script imports the h4ckath0n app, enumerates all routes via OpenAPI, groups them
by tags, and checks that README.md contains this text exactly between the
<!-- GENERATED_ROUTES_START --> and <!-- GENERATED_ROUTES_END --> markers.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"

MARKER_START = "<!-- GENERATED_ROUTES_START -->"
MARKER_END = "<!-- GENERATED_ROUTES_END -->"


def generate_routes_markdown() -> str:
    from h4ckath0n.app import create_app  # noqa: E402
    from h4ckath0n.config import Settings  # noqa: E402

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()

    groups = defaultdict(list)
    for path, methods in openapi.get("paths", {}).items():
        for method, operation in methods.items():
            tags = operation.get("tags")
            # If no tags, bucket to "General"
            tag = tags[0] if tags else "General"

            summary = operation.get("summary", "")
            desc = operation.get("description", "")

            # Use only the first sentence of the description
            first_sentence = desc.split(".")[0] + "." if desc else ""
            if not first_sentence:
                first_sentence = summary + "." if summary else ""

            groups[tag].append((method.upper(), path, first_sentence))

    # Order and map raw tags to nice headers
    tag_order = [
        "General",
        "auth",
        "passkey",
        "password-auth",
        "jobs",
        "uploads",
        "llm",
    ]

    header_map = {
        "General": "General",
        "auth": "Session",
        "passkey": "Passkeys",
        "password-auth": "Password Auth",
        "jobs": "Background Jobs",
        "uploads": "Uploads",
        "llm": "LLM Chat",
    }

    lines = []
    for tag in tag_order:
        if tag not in groups:
            continue

        header = header_map.get(tag, tag.title())
        lines.append(f"### {header}")

        for m, p, d in groups[tag]:
            text = f"- `{m} {p}` — {d}"
            lines.append(text)

        lines.append("")

    return "\n".join(lines).strip()


def main() -> int:
    parser = argparse.ArgumentParser(description="Check or update documented routes.")
    parser.add_argument("--update", action="store_true", help="Update README.md inline")
    args = parser.parse_args()

    readme_text = README.read_text(encoding="utf-8")
    if MARKER_START not in readme_text or MARKER_END not in readme_text:
        print(f"❌ Error: {MARKER_START} or {MARKER_END} not found in README.md")
        return 1

    generated_md = generate_routes_markdown()
    pattern = re.compile(rf"{re.escape(MARKER_START)}.*?{re.escape(MARKER_END)}", re.DOTALL)
    expected_text = f"{MARKER_START}\n\n{generated_md}\n\n{MARKER_END}"
    new_text = pattern.sub(expected_text, readme_text)

    if new_text != readme_text:
        if args.update:
            README.write_text(new_text, encoding="utf-8")
            print("✅ Updated README.md with generated API routes.")
            return 0
        else:
            print("❌ The API routes documented in README.md are out of date.")
            print("Run `uv run scripts/check_doc_routes.py --update` to fix.")
            return 1

    print("✅ All API routes are documented correctly in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
