
## 2025-02-12 - Centralized validation with Pydantic Annotated
**Learning:** Pydantic V2 allows replacing duplicated `@field_validator` logic with reusable `typing.Annotated` types using `AfterValidator`.
**Action:** Use `Annotated` + `AfterValidator` to centralize and compose validation rules, rather than repeating `@field_validator` decorators across models.
