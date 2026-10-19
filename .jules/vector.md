## 2023-10-18 - Reusable Pydantic Validators with Annotated
**Learning:** To eliminate duplicated `@field_validator` methods across multiple models, extract the validation logic into a reusable type using `typing.Annotated` and `pydantic.functional_validators.AfterValidator` (e.g., `Annotated[str, AfterValidator(my_func)]`).
**Action:** Use this pattern to centralize validation logic across auth schemas.
