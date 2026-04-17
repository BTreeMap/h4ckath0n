## 2024-04-17 - Centralize scope parsing/normalization

**Learning:** Comma-separated scope string parsing is duplicated and inconsistent across `src/h4ckath0n/auth/dependencies.py`, `src/h4ckath0n/auth/session_router.py`, and `src/h4ckath0n/cli.py`. Sometimes it uses sets, sometimes list comprehensions, and sometimes `filter(None, map(str.strip, ...))`. This lack of centralization causes correctness risks around deduplication and order-preservation, and violates the repo's FP-style preferences.

**Action:** Extract pure helpers `parse_scopes` and `format_scopes` in a common auth utilities file (e.g., `src/h4ckath0n/auth/scopes.py`) and update all call sites to use them to enforce deterministic order and safe handling.
