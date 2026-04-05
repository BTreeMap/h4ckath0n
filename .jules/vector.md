## 2025-02-18 - Centralized string/list sequence conversions

**Learning:** When dealing with string serialization of arrays/lists in the database (e.g. `user.scopes` storing a comma-separated string), deduplication and string manipulation (`split`, `strip`, `filter`) can easily become repeated ad-hoc across modules (e.g. `auth/dependencies.py`, `auth/session_router.py`, `cli.py`). Using `set()` for deduplication also risks destroying ordering.

**Action:** Extract a pure functional parser/formatter (`parse_scopes`, `format_scopes`) using `dict.fromkeys()` for stable deduplication, creating a single centralized pipeline for sequence conversions.