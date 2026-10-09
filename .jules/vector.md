## 2024-05-15 - Pydantic BeforeValidator vs AfterValidator
**Learning:** `BeforeValidator` runs before Pydantic parsing. Blindly calling `.strip()` on a raw JSON value without type checking will crash with `AttributeError` for non-string types, bypassing FastAPI's normal `422` handler and returning a `500`.
**Action:** Always prefer `AfterValidator` for string manipulation when possible so Pydantic handles the coercion and basic type checking first. If `BeforeValidator` is strictly required, validate types manually (e.g. `isinstance(value, str)`) before invoking string methods.
