## 2024-05-18 - Centralize display name validation using Pydantic Annotated
**Learning:** Pydantic v2's `Annotated` with `AfterValidator` can be used to centralize both structural constraints (`max_length`) and behavioral normalizations (e.g., stripping whitespace) into a single reusable type alias, avoiding duplicated `@field_validator` methods across request schemas.
**Action:** When validation logic is duplicated across multiple Pydantic models in this codebase, prefer extracting it into a reusable `Annotated` field definition.
