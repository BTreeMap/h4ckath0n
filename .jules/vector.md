
## 2024-05-19 - Centralized scope parsing logic
**Learning:** Comma-separated scope strings were being inconsistently parsed inline using `filter(None, map(str.strip, scopes.split(",")))` across CLI and API dependencies.
**Action:** Centralized parsing into pure helpers `parse_scopes` and `format_scopes` in `src/h4ckath0n/auth/scopes.py`. Always use these helpers for deterministic, order-preserving scope normalization.
