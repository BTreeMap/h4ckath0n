## 2024-05-28 - Centralize display name validation logic
**Learning:** The logic to clean and validate `display_name` is duplicated across schemas in `auth` and `auth/passkeys`.
**Action:** Extract a centralized, pure helper function or validator that acts as a single source of truth for display name normalization.
