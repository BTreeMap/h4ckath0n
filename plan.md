1. **Remove duplicated validation logic for `display_name` in `schemas.py` and `passkeys/schemas.py`.**
   - The repository's codebase contains duplicated logic for normalizing and validating `display_name`.
   - In `src/h4ckath0n/auth/schemas.py`, there is a `normalize_display_name` helper and a `@field_validator("display_name")` in `RegisterRequest`.
   - In `src/h4ckath0n/auth/passkeys/schemas.py`, there is also a `@field_validator("display_name")` in `PasskeyRegisterStartRequest`.
   - Following the FP-style thinking and memory instructions, Pydantic's `typing.Annotated` combined with `pydantic.Field` and `pydantic.AfterValidator` should be used to create reusable validation types instead of repeating `@field_validator` methods across multiple models.

2. **Implement reusable `DisplayName` type.**
   - In `src/h4ckath0n/auth/schemas.py`, import `Annotated` from `typing`, and `AfterValidator` from `pydantic`.
   - Define `DisplayName = Annotated[str, Field(max_length=DISPLAY_NAME_MAX_LENGTH), AfterValidator(normalize_display_name)]`.
   - Update `RegisterRequest` in `src/h4ckath0n/auth/schemas.py` to use `display_name: DisplayName` and remove the `@field_validator`.
   - Update `PasskeyRegisterStartRequest` in `src/h4ckath0n/auth/passkeys/schemas.py` to import `DisplayName` from `h4ckath0n.auth.schemas`, use `display_name: DisplayName`, and remove the `@field_validator`.

3. **Log critical learning as Vector in `.jules/vector.md`.**
   - Append to `.jules/vector.md` a learning about using `Annotated` and `AfterValidator` to define centralized reusable validation types instead of repeating `@field_validator` methods across multiple Pydantic models in this codebase.

4. **Run pre-commit steps.**
   - Call `pre_commit_instructions` tool to complete pre commit steps ensuring testing, verifications, review, and reflection are done.

5. **Submit PR.**
   - Commit and submit the code with a description formatted as requested by the persona.
