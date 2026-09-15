## 2024-07-23 - Centralize Scope Transformations
**Learning:** When handling user scope inputs, ad-hoc `parse_scopes` and `serialize_scopes` logic is prone to drift and mutation complexity.
**Action:** Always use centralized pure helpers (`normalize_scopes`, `add_scopes`, and `remove_scopes`) in `h4ckath0n.auth.authz` to ensure consistent deduplication, order preservation, and validation.
