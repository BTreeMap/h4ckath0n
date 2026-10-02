## 2024-09-19 - Centralize Pydantic Validation with Annotated
**Learning:** Pydantic v2's `typing.Annotated` combined with `Field` and `AfterValidator` effectively merges specific constraint data and common normalization logic (like display name rules).
**Action:** Prefer composable `Annotated` aliases over repetitive `@field_validator` methods when shared normalization or validation is used in multiple models.
