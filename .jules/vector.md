## 2025-02-12 - Centralize scope parsing
**Learning:** The codebase previously duplicated list-to-comma-string parsing and normalization for user scopes in dependencies, CLI, and routers.
**Action:** Extracted pure functional helpers `parse_scopes` and `format_scopes` into `src/h4ckath0n/auth/scopes.py` to serve as the single source of truth for scope list conversion and normalization.
