## 2024-05-14 - Centralize Pydantic validation logic
**Learning:** Pydantic schema validation using repeated `@field_validator` hooks creates duplicated boilerplate across models that share the same field semantics (like `display_name`).
**Action:** Refactor repeated validation or normalization logic into reusable `typing.Annotated` types combined with `pydantic.AfterValidator` (e.g., `Annotated[str, Field(...), AfterValidator(func)]`) to centralize the rules in one declarative place.
