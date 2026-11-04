## 2024-10-07 - Encapsulating Pydantic Field Validation with Annotated
**Learning:** This codebase uses Pydantic v2. Validation logic (like trimming and rejecting empty strings for display names) was duplicated using `@field_validator` on multiple schemas. Pydantic v2 allows merging field-level metadata (like descriptions) with reusable annotated types containing constraints and validators.
**Action:** Used `typing.Annotated` combined with `pydantic.AfterValidator` to define a single `DisplayNameField` that centrally handles `max_length` and normalization.
