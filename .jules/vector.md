## 2024-04-10 - Centralize sequence transformation for database text columns
**Learning:** The codebase frequently serializes/deserializes lists (like scopes) to/from database text columns. Ad-hoc string manipulation (`.split(",")`, `.strip()`) across different files causes logic duplication and risks order destruction when using `set()` for deduplication.
**Action:** Use centralized, pure functional utilities (e.g., `parse_scopes`, `format_scopes`) that rely on `dict.fromkeys(iterable)` to preserve order when deduplicating, avoiding scattered mutation and duplication.
