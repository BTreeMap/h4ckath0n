## 2024-05-18 - Centralize User Scopes Parsing
**Learning:** In h4ckath0n, the parsing and formatting of user scopes was duplicated in multiple places with slight variations (`filter` with map vs list comprehensions, preserving order with sets vs lists vs keys). Scope structures are strings stored in the database.
**Action:** Centralize the logic in `src/h4ckath0n/auth/schemas.py` and use two pure helper functions `parse_scopes(raw: str) -> list[str]` and `format_scopes(scopes: Iterable[str]) -> str`. Use them everywhere scopes are read or updated for clarity and determinism.
