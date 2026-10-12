## 2023-10-12 - Centralized Display Name Validation
**Learning:** Pydantic v2 `AfterValidator` and `Annotated` should be used to extract duplicate normalization logic out of class-level `@field_validator` blocks and into a reusable, declarative field type, which centralizes the semantics.
**Action:** When a normalization strategy applies to multiple fields across different schemas (e.g. `display_name`), encapsulate it using `typing.Annotated` combined with `pydantic.AfterValidator` instead of repeating the `@field_validator` boilerplate.
