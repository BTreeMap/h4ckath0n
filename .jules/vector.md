## 2024-05-14 - Scopes normalization
**Learning:** The logic to normalize comma-separated strings of scopes into lists or deduplicated strings is repeated in multiple places (e.g., `src/h4ckath0n/auth/dependencies.py`, `src/h4ckath0n/auth/session_router.py`, `src/h4ckath0n/cli.py`), sometimes with slightly varying semantics.
**Action:** Extract a centralized utility in `src/h4ckath0n/auth/scopes.py` for parsing and normalizing scope strings, making behavior deterministic across the codebase.
