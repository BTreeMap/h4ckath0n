## 2026-06-10 - Centralize Pydantic Validation Logic via Annotated
**Learning:** When refactoring duplicated `@field_validator` logic in Pydantic V2 into reusable types, using `typing.Annotated` with `pydantic.functional_validators.AfterValidator` preserves custom `ValueError` messages compared to `StringConstraints`, avoiding test failures that depend on exact exception text.
**Action:** Extract reusable `AfterValidator` annotations instead of repeating `@field_validator` methods, especially when maintaining specific error messages is important.
