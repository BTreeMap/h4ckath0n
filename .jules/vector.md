
## 2024-03-05 - Centralize string list handling for roles/scopes
**Learning:** The codebase was previously parsing and formatting comma-separated scope strings manually across various files (e.g., `dependencies.py`, `cli.py`, `session_router.py`) using `.split(",")`, `.strip()`, and `filter(None)`. This ad-hoc string manipulation invites drift and duplicate empty-string/whitespace bugs.
**Action:** Created `parse_scopes` and `format_scopes` pure functions in `src/h4ckath0n/auth/scopes.py` to act as the single source of truth for scope parsing, deduplicating, and serializing. In the future, prefer central functional utilities when converting lists to database text columns.
