## 2024-04-25 - Env Vars Generation Parity
**Learning:** Hardcoded environment variables in README.md quickly drift from the actual `Settings` schema. This repository uses pydantic `BaseSettings`, making it possible to inspect and automatically generate the environment variables documentation.
**Action:** Replace the static table in `README.md` with generated content and add a script (`scripts/generate_env_docs.py`) to prevent drift. Integrate this check into CI to catch missing/stale documentation automatically.

## 2024-04-25 - Env Vars Generation Parity
**Learning:** Hardcoded environment variables in README.md quickly drift from the actual `Settings` schema. This repository uses pydantic `BaseSettings`, making it possible to inspect and automatically generate the environment variables documentation.
**Action:** Replace the static table in `README.md` with generated content and add a script (`scripts/generate_env_docs.py`) to prevent drift. Integrate this check into CI to catch missing/stale documentation automatically.
