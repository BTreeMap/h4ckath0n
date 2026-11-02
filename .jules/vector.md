## 2026-11-02 - Pydantic Field Configuration Merging

**Learning:** Pydantic V2 cleanly merges `Field` constraints defined within an `Annotated` type alias with `Field` metadata provided at the attribute assignment level (e.g., `Field(..., description="...")`).

**Action:** When extracting shared normalization or validation logic in Pydantic schemas, utilize `Annotated` aliases over repetitive `@field_validator` hooks to create composable types without sacrificing OpenAPI schema fidelity.
