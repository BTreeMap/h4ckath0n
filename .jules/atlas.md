## 2024-06-16 - Prevent configuration drift with generated docs
**Learning:** Environment variables documented by hand in `README.md` drift from `src/h4ckath0n/config.py`.
**Action:** Use `pydantic.Field` descriptions on `BaseSettings` properties and a Python script (`scripts/check_doc_config.py`) to parse `Settings.model_fields` and generate a markdown table using `<!-- CONFIG_DOCS_START -->` markers in the README. Integrate the check into CI.
