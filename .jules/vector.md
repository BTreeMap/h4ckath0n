## 2024-10-15 - Centralize validation with Annotated types
**Learning:** Pydantic v2 allows extracting duplicated `@field_validator` methods into reusable `Annotated[..., AfterValidator(...)]` types, preserving Field constraints.
**Action:** Use this pattern to centralize repeated field normalization (like display name cleaning) into a single functional type boundary.
