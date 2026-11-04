## 2024-05-18 - Display Name Centralization
**Learning:** This codebase uses Pydantic v2 and values functional programming. The `display_name` validation is duplicated across multiple schemas using boilerplate `@field_validator`. This can be centralized cleanly using `typing.Annotated` and `pydantic.AfterValidator`, which is more idiomatic for FP-style reusable types in Pydantic v2.
**Action:** Replace duplicated `@field_validator` hooks with a single `Annotated` type definition in `auth/schemas.py`, and reuse it across endpoints.
