## 2024-10-11 - Centralizing Pydantic normalization with Annotated
**Learning:** Pydantic v2's `typing.Annotated` with `AfterValidator` correctly merges outer `Field(description=...)` definitions without overwriting inner constraints (like `max_length`). It is much cleaner for sharing normalization logic than duplicated `@field_validator` methods.
**Action:** Use `Annotated` with `AfterValidator` for composable string normalization (e.g. trimming and bounds checking) instead of class-level mutation methods.
