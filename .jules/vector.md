## 2025-05-29 - Shared Validations in Pydantic

**Learning:** When using Pydantic `field_validator`, duplication of the validation function definition (e.g. `_clean_display_name`) can be eliminated by exposing a single module-level pure helper (e.g. `clean_display_name`) and passing it to `field_validator` via functional application (e.g. `_clean_display_name = field_validator("display_name")(clean_display_name)`).

**Action:** Look out for duplicated `field_validator` classmethods and extract them into shared pure functions to apply across multiple Pydantic schemas.
