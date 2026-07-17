#!/usr/bin/env -S uv run python
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"
FRAMEWORK_PATHS = frozenset({"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"})


def generate_routes_table() -> str:
    from h4ckath0n.app import create_app
    from h4ckath0n.config import Settings

    settings = Settings(
        database_url="sqlite+aiosqlite://",
        password_auth_enabled=True,
    )
    app = create_app(settings)
    openapi = app.openapi()

    out = []
    out.append("| Method | Path | Summary |")
    out.append("|---|---|---|")

    routes = []
    for path, methods in openapi.get("paths", {}).items():
        if path in FRAMEWORK_PATHS:
            continue
        for method, op in methods.items():
            summary = op.get("summary", "")
            routes.append((method.upper(), path, summary))

    for method, path, summary in routes:
        out.append(f"| `{method}` | `{path}` | {summary} |")

    return "\n".join(out)


def update_readme(dry_run: bool = False) -> int:
    readme_text = README.read_text()
    table = generate_routes_table()

    pattern = re.compile(r"(<!-- BEGIN API ROUTES -->).*?(<!-- END API ROUTES -->)", re.DOTALL)

    if not pattern.search(readme_text):
        print("Could not find <!-- BEGIN API ROUTES --> in README.md")
        return 1

    def repl(m):
        return f"{m.group(1)}\n{table}\n{m.group(2)}"

    new_readme = pattern.sub(repl, readme_text)

    if dry_run:
        if new_readme != readme_text:
            print(
                "❌ README.md is out of date. Run `scripts/generate_doc_routes.py` to update it."
            )
            return 1
        print("✅ README.md API routes are up to date.")
        return 0

    README.write_text(new_readme)
    return 0


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    sys.exit(update_readme(dry_run=args.check))
