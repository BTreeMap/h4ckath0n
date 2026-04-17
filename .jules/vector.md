## 2024-05-24 - Centralize scope string parsing and formatting
**Learning:** Comma-separated scope strings were being manually parsed (split, strip, filter) across `auth.dependencies`, `auth.session_router`, and `cli.py`, leading to duplicated normalization logic and potential drift.
**Action:** Created centralized functional-style utilities `parse_scopes` and `format_scopes` in `h4ckath0n.auth.scopes` to ensure a single source of truth for deduplicating, trimming, and normalizing scope strings across the API and CLI boundaries.
