#!/usr/bin/env -S uv run python
"""Drift-prevention check: Verify and auto-update API routes in README.md."""

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
MARKER_API_START = "<!-- BEGIN API ROUTES -->"
MARKER_API_END = "<!-- END API ROUTES -->"
MARKER_PW_START = "<!-- BEGIN PASSWORD ROUTES -->"
MARKER_PW_END = "<!-- END PASSWORD ROUTES -->"


def categorize_route(path: str, route_str: str, routes: dict):
    if path in ["/", "/health"]:
        routes["core"].append(route_str)
    elif path.startswith("/auth/session"):
        routes["session"].append(route_str)
    elif path.startswith("/jobs"):
        routes["jobs"].append(route_str)
    elif path.startswith("/uploads"):
        routes["uploads"].append(route_str)
    elif path.startswith("/llm"):
        routes["llm"].append(route_str)
    elif "password" in path or "register" in path or "login" in path:
        routes["password"].append(route_str)
    elif not path.startswith("/auth/passkey"):
        routes["other"].append(route_str)


def get_routes():
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(password_auth_enabled=True)
    app = create_app(settings)
    schema = app.openapi()

    routes = {
        "core": [],
        "session": [],
        "jobs": [],
        "uploads": [],
        "llm": [],
        "password": [],
        "other": [],
    }

    for path, methods in schema.get("paths", {}).items():
        for method, endpoint in methods.items():
            summary = endpoint.get("summary", "")
            route_str = f"- `{method.upper()} {path}` — {summary}."
            categorize_route(path, route_str, routes)

    if routes["other"]:
        # If there are uncategorized routes, the script should fail
        # and require the developer to update it.
        print(
            "❌ Error: Uncategorized API routes found. "
            "Please update scripts/check_doc_routes.py to categorize:"
        )
        for r in routes["other"]:
            print(f"  {r}")
        sys.exit(1)

    def format_section(title, lst):
        if not lst:
            return ""
        return f"### {title}\n" + "\n".join(sorted(lst))

    api_content = "\n\n".join(
        filter(
            None,
            [
                "\n".join(sorted(routes["core"])),
                format_section("Session", routes["session"]),
                format_section("Background Jobs", routes["jobs"]),
                format_section("Uploads", routes["uploads"]),
                format_section("LLM Chat", routes["llm"]),
            ],
        )
    )

    pw_content = "\n".join(sorted(routes["password"]))

    return api_content, pw_content


def main() -> int:
    fix = "--fix" in sys.argv
    readme_text = README.read_text()

    api_content, pw_content = get_routes()

    new_text = readme_text

    if MARKER_API_START in new_text:
        replacement = f"{MARKER_API_START}\n{api_content}\n{MARKER_API_END}"
        pattern = re.compile(rf"{MARKER_API_START}.*?{MARKER_API_END}", re.DOTALL)
        new_text = pattern.sub(replacement, new_text)

    if MARKER_PW_START in new_text:
        replacement = f"{MARKER_PW_START}\n{pw_content}\n{MARKER_PW_END}"
        pattern = re.compile(rf"{MARKER_PW_START}.*?{MARKER_PW_END}", re.DOTALL)
        new_text = pattern.sub(replacement, new_text)

    if new_text != readme_text:
        if fix:
            README.write_text(new_text)
            print("✅ Updated API routes in README.md")
            return 0
        else:
            print("❌ README.md API routes are out of date. Run with --fix.")
            return 1

    print("✅ API routes in README.md are up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
