## 2024-04-08 - Env Var Docs Drift
**Learning:** Env vars drift heavily because they are defined in `src/h4ckath0n/config.py` using `pydantic-settings` but the list in README.md is hand-written and out of date (missing Redis, Storage, Email, and Demo settings).
**Action:** Replace the hand-written env var list in README.md with a generated section from a docs-check script (`scripts/check_doc_env_vars.py`), run via CI, that parses Pydantic model fields and ensures the README stays in sync.
