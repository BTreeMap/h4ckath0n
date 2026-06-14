## 2024-06-14 - Extract shared display name normalization to reusable AfterValidator
**Learning:** We have duplicated `@field_validator` logic in both `auth/schemas.py` and `auth/passkeys/schemas.py` that raises custom `ValueError` exceptions for empty display names.
**Action:** Extract this logic into a centralized `typing.Annotated` type with `AfterValidator`. Based on project conventions, use `AfterValidator` rather than `StringConstraints` to preserve the exact custom `ValueError` exception ("Display name must not be empty") that existing tests might rely upon.
