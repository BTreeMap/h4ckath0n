## 2026-03-25 - Centralize database text column transformations

**Learning:** The codebase repeatedly performed ad-hoc string manipulation (`.split(",")`, `.strip()`, `filter()`) on the `scopes` database column across multiple files (`cli.py`, `dependencies.py`, `session_router.py`). This led to duplicated logic and inconsistent edge-case handling.
**Action:** Centralize transformation of iterable database columns into pure FP helpers (`parse_scopes`, `format_scopes`) to ensure a single source of truth for normalization, deduplication, and edge cases.