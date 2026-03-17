## 2024-05-24 - Env Var Drift Prevention
**Learning:** README env var tables drift quickly from `src/h4ckath0n/config.py`. Redis, Storage, and Email configurations added to `Settings` are missing from the manual README table.
**Action:** Replace manual env var tables in markdown with a dynamically generated block based on `pydantic-settings` to ensure exact parity between code and documentation. Create a test script similar to `check_doc_routes.py` to verify or auto-update this block.
