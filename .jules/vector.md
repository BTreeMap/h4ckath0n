## 2024-11-20 - Centralize Pydantic Validation with Annotated types
**Learning:** This codebase uses Pydantic. Refactoring repeated validation/normalization logic in Pydantic schemas by centralizing the logic into reusable `typing.Annotated` types combined with `pydantic.AfterValidator` is preferable over duplicating `@field_validator` methods across multiple models.
**Action:** Use `typing.Annotated` and `pydantic.AfterValidator` to wrap shared validation logic in Pydantic models.
