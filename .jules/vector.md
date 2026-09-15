## 2024-05-12 - Centralize Validation with Annotated
**Learning:** When refactoring repeated validation or normalization logic in Pydantic schemas, prefer centralizing the logic into reusable `typing.Annotated` types combined with `pydantic.AfterValidator` (e.g., `Annotated[str, Field(...), AfterValidator(func)]`) rather than duplicating `@field_validator` methods across multiple models.
**Action:** Replace `@field_validator` hooks with reusable `Annotated` types for centralized semantics and cleaner models.
