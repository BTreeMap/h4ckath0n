#!/usr/bin/env -S uv run python
"""Verify that every CLI command is documented in the README."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
README = REPO_ROOT / "README.md"


def get_cli_commands() -> list[str]:
    """Return a list of all operator CLI commands."""
    from h4ckath0n.cli._parser import build_parser

    parser = build_parser()
    subparsers_actions = [
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    ]
    commands = []
    for subparsers_action in subparsers_actions:
        for choice, subparser in subparsers_action.choices.items():
            sub_subparsers_actions = [
                action
                for action in subparser._actions
                if isinstance(action, argparse._SubParsersAction)
            ]
            if sub_subparsers_actions:
                for sub_subparsers_action in sub_subparsers_actions:
                    for sub_choice in sub_subparsers_action.choices:
                        commands.append(f"h4ckath0n {choice} {sub_choice}")
            else:
                commands.append(f"h4ckath0n {choice}")
    return sorted(commands)


def main() -> int:
    commands = get_cli_commands()
    readme_text = README.read_text()
    missing = []

    for cmd in commands:
        if not re.search(rf"`{cmd}", readme_text, re.IGNORECASE) and not re.search(
            rf"^\s*{cmd}", readme_text, re.IGNORECASE | re.MULTILINE
        ):
            missing.append(cmd)

    if missing:
        print("❌ The following CLI commands are not documented in README.md:\n")
        for cmd in missing:
            print(f"  {cmd}")
        return 1

    print(f"✅ All {len(commands)} CLI commands are documented in README.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
