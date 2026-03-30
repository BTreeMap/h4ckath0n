
## 2024-05-24 - Centralize and normalize scope parsing
**Learning:** Repeated ad-hoc string manipulations (like `filter(None, map(str.strip, user.scopes.split(",")))`) for scope validation and CLI updates introduce bug risks and inconsistency.
**Action:** Extracted pure functional utilities `parse_scopes` and `format_scopes` in `src/h4ckath0n/auth/scopes.py` to handle deduplication (preserving order) and serialization safely across the codebase.
