## 2024-06-29 - Config Docs Drift Prevention
**Learning:** Hardcoded environment variables in README.md quickly drift from Pydantic `BaseSettings` definitions, as seen with 16 missing settings (like Redis, Storage, and Email) in this repo.
**Action:** Use inline `pydantic.Field(default=..., description="...")` in the config loader and a generation script to parse `Settings.model_fields`. Add a CI step that runs `git diff --exit-code README.md` to guarantee the docs match the code exactly.
