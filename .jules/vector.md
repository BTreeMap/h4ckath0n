## 2024-06-05 - Centralize Pydantic Validation
**Learning:** Pydantic duplicated validation logic like `@field_validator` can be cleanly refactored into reusable explicit type definitions using `typing.Annotated` with `AfterValidator`.
**Action:** Always favor `Annotated` with `AfterValidator` to centralize validation logic rather than scattering duplicated `field_validator` methods across schemas.
