## 2026-04-20 - Centralize scope parsing/formatting helper
**Learning:** Parsing comma-separated scopes strings inline (e.g. `user.scopes.split(",")`) was duplicated across modules.
**Action:** Extracted `parse_scopes` and `format_scopes` into pure composable helpers in `src/h4ckath0n/auth/scopes.py`.
