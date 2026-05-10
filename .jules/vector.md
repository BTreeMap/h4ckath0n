## 2024-05-10 - Centralized user scopes normalization
**Learning:** The codebase stored user scopes as comma-separated strings, but parsing/formatting logic was duplicated across domain schemas, CLI arguments, and dependencies, making determinism ad hoc and leading to order-related test instability or subtle parsing variations.
**Action:** Extract a pure, order-preserving functional pipeline (`parse_scopes`, `format_scopes`) in `schemas.py` and reuse it as the single source of truth across CLI, router parsing, and dependency validations.
