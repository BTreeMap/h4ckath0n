## 2024-05-20 - Pydantic V2 Annotated Fields
**Learning:** Pydantic V2 in this repository perfectly merges `typing.Annotated` validation constraints (like `Field(max_length=...)` and `AfterValidator(...)`) with localized attribute metadata (like `description="..."`) declared on the model's field itself.
**Action:** When centralizing normalization/validation logic across different Pydantic models with shared constraints but different metadata, use `Annotated` types instead of duplicating `@field_validator` methods.
