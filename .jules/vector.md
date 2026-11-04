## 2025-02-28 - Pydantic Field Normalization with Annotated

**Learning:** When standardizing request validation in Pydantic v2 (e.g., trimming `display_name` and verifying length constraints across multiple schemas like auth and passkeys), using repetitive `@field_validator` hooks causes logic duplication and boilerplate drift.
**Action:** Extract the common constraints into a reusable type via `Annotated[str, Field(...), AfterValidator(...)]`. This cleanly functionalizes the parsing and normalization, providing a single source of truth for properties like `DISPLAY_NAME_MAX_LENGTH` and eliminating imperative setup code in the dependent schemas.
