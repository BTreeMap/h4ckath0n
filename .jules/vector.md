
## 2024-07-03 - Pydantic Field Validation with Helpers
**Learning:** When using a helper function in a Pydantic V2 `@field_validator`, assigning it directly (e.g. `_clean_field = field_validator('field')(classmethod(helper))`) can cause mypy type-checking errors.
**Action:** Always wrap reusable helper functions inside a `@classmethod` decorated method in the model (e.g. `def _clean_field(cls, v): return helper(v)`).
