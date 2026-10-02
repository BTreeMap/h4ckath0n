## 2024-05-24 - Pydantic Annotated Fields for Shared Validation
**Learning:** In Pydantic v2, we can centralize shared validation and OpenAPI constraints (like `max_length`) using `typing.Annotated` combined with `pydantic.Field` and `pydantic.AfterValidator`. Any additional `Field` metadata added at the model attribute level (e.g., `Field(description="...")`) will be merged successfully without overwriting the inner `Field` constraints.
**Action:** Use this pattern to replace duplicated `@field_validator` methods across multiple models.
