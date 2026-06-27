## 2025-02-24 - Centralize Field Validation with BeforeValidator
**Learning:** Duplicated `@field_validator` methods for strings that require normalization (like stripping whitespace and checking for emptiness) can cause bugs or drift across multiple schemas.
**Action:** Use Pydantic V2's `Annotated` with `BeforeValidator` to extract these normalizations into pure, shared helpers. Always check `if isinstance(v, str):` in `BeforeValidator` since it receives raw inputs.
