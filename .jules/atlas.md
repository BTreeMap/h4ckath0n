## 2024-03-15 - [Env Var Doc Drift]
**Learning:** The configuration table in README.md drifts from the actual pydantic-settings `Settings` model in `src/h4ckath0n/config.py` because there was no programmatic check ensuring new environment variables are documented.
**Action:** Add a CI step that dynamically lists the keys of the `Settings` model and asserts they appear in the `README.md` configuration table.
