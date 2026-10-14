#!/usr/bin/env -S uv run python
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "scripts"))

# ruff: noqa: E402
import check_doc_env

README = REPO_ROOT / "README.md"


def main():
    readme_text = README.read_text()
    expected_table = check_doc_env.generate_expected_table()

    start_marker = "<!-- START_ENV_VARS -->"
    end_marker = "<!-- END_ENV_VARS -->"

    if start_marker not in readme_text or end_marker not in readme_text:
        print("Markers not found in README.md")
        return 1

    start_idx = readme_text.find(start_marker)
    end_idx = readme_text.find(end_marker) + len(end_marker)

    prefix = readme_text[:start_idx]
    suffix = readme_text[end_idx - len(end_marker) :]
    new_readme = f"{prefix}{start_marker}\n{expected_table}\n{suffix}"
    README.write_text(new_readme)
    print("README.md updated.")


if __name__ == "__main__":
    sys.exit(main())
