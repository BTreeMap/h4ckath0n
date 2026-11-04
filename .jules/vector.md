## 2024-08-27 - Centralize Pydantic Validation with Annotated
**Learning:** The codebase previously duplicated `@field_validator` methods across multiple models to apply string normalization (e.g. `normalize_display_name`).
**Action:** When refactoring repeated validation or normalization logic in Pydantic schemas, prefer centralizing the logic into reusable `typing.Annotated` types combined with `pydantic.AfterValidator` (e.g., `Annotated[str, Field(...), AfterValidator(func)]`) rather than duplicating `@field_validator` methods across multiple models.
