## 2025-04-18 - Unify Scope Parsing
**Learning:** The codebase scatters comma-separated string parsing for `scopes` across `dependencies.py`, `session_router.py`, and `cli.py` (`_normalize_scopes` and inline `.split(",")`). This violates centralization and determinism.
**Action:** Extract a highly composable helper in `h4ckath0n.auth.scopes` with pure pipelines (`iter_scopes`, `parse_scopes`, `format_scopes`) using `collections.abc.Iterable`, `filter`, and `dict.fromkeys`. Use this source of truth universally.
