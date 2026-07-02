## 2024-05-15 - Environment Variable Docs Drift
**Learning:** Env vars defined in Pydantic Settings drift from README.md easily.
**Action:** Add a CI step calling `scripts/check_env_vars.py` to assert that all fields on `Settings` are explicitly documented in `README.md`.
