## 2024-05-18 - Extract pure helper for field validation
**Learning:** Pydantic validators can be shared by assigning `field_validator("field_name")(pure_function)` directly, removing the need for duplicated classmethods across different schemas.
**Action:** Use this pattern to extract and reuse pure validation helpers for shared concepts (like display names) instead of repeating inline `@field_validator` methods.
