## 2024-04-22 - Extract duplicated string normalization into composable pipelines
**Learning:** Parsing and normalizing comma-separated scopes strings is duplicated across `dependencies.py`, `session_router.py`, and `cli.py`, leading to ad-hoc list and set creation, and inconsistent semantics.
**Action:** Extracted the logic into a new centralized, pure, highly composable helper pipeline (`iter_scopes`, `parse_scopes`, `format_scopes`) using `iter`, `filter`, `map`, and `dict.fromkeys` for order-preserving deduplication, as aligned with the repository's FP style preference.
