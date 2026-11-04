## 2024-10-21 - Pydantic Field Validation with Annotated Types

**Learning:** When standardizing Pydantic validations across multiple models in a codebase, extracting the logic into an `Annotated` type with an `AfterValidator` prevents duplicated `@field_validator` boilerplates and keeps the semantics in one central source of truth.

**Action:** Use `typing.Annotated[type, Field(...), AfterValidator(...)]` when replacing duplicated custom validation logic across Pydantic schemas.
