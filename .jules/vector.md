## 2024-05-24 - Centralized Pydantic DisplayName Validation
**Learning:** Pydantic v2 gracefully merges constraints and validations from an `Annotated` type combining `Field` (e.g., `max_length`) and `AfterValidator` with additional metadata defined at the class level (e.g., `Field(description="...")`).
**Action:** Use `typing.Annotated` along with `AfterValidator` and `Field` to centralize scattered field normalization/validation methods when data shaping logic is repeated across schemas.
