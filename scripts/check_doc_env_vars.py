#!/usr/bin/env -S uv run python
"""Drift-prevention check: verify that all environment variables are documented."""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from h4ckath0n.config import Settings  # noqa: E402

README = REPO_ROOT / "README.md"

# Fields that we do not require in user docs
FRAMEWORK_FIELDS = frozenset()


def check_env_vars_in_readme() -> list[str]:
    readme_text = README.read_text()
    missing: list[str] = []

    for field_name in Settings.model_fields:
        if field_name in FRAMEWORK_FIELDS:
            continue

        env_var = "H4CKATH0N_" + field_name.upper()

        # Look for the exact backticked env var
        if f"`{env_var}`" not in readme_text:
            if env_var == "H4CKATH0N_OPENAI_API_KEY" and "`OPENAI_API_KEY`" in readme_text:
                pass
            else:
                missing.append(env_var)

    return missing


def main() -> int:
    missing = check_env_vars_in_readme()
    if missing:
        print("❌ The following environment variables are NOT documented in README.md:\n")
        for env_var in missing:
            print(f"  {env_var}")
        print("\nAdd these variables to the Configuration section in README.md.")
        return 1

    print(
        f"✅ All {len(Settings.model_fields)} environment variables are documented in README.md."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
