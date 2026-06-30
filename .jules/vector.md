## 2025-05-16 - Centralize Required Display Name Validation
**Learning:** Extracting Pydantic validation logic for required fields must not overwrite optional field validation helpers, and standalone helpers must be called inside `@classmethod` wrappers to avoid mypy errors.
**Action:** Centralize duplicated string validation logic by extracting `clean_required_display_name` into `h4ckath0n.auth.schemas` and importing it into `h4ckath0n.auth.passkeys.schemas`.
