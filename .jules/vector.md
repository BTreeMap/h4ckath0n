## 2024-10-24 - Centralized Pydantic validation via Annotated types
**Learning:** Pydantic models in this repository often duplicate `@field_validator` hooks for shared fields (like `display_name`). Using `Annotated` with `AfterValidator` (e.g., `Annotated[str, Field(max_length=...), AfterValidator(normalize_display_name)]`) removes this duplication while preserving declarative schema constraints.
**Action:** Default to extracting reusable `Annotated` definitions instead of scattering identical `@field_validator` methods across multiple models.
