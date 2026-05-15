## 2025-04-12 - Centralize parsing and formatting logic for database text columns
**Learning:** When converting sequences like comma-separated scopes to and from database text columns, repeating ad-hoc string manipulation (like `.split(",")`, `.strip()`, or `filter(None)`) across modules causes minor subtle divergence and bug risks.
**Action:** Extract this logic into small, pure helper functions (e.g. `parse_scopes`, `format_scopes`) with clear boundaries. Deduplication that preserves order should be favored using `dict.fromkeys()` over `set()`.
