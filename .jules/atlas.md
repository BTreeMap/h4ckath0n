## 2025-04-28 - Environment Variable Documentation Parity
**Learning:** The `README.md` hand-written environment variables table often drifts from the actual configuration in `src/h4ckath0n/config.py` due to new config fields being added without updating the documentation.
**Action:** Use a script `scripts/generate_env_docs.py` that extracts Pydantic `Field` descriptions and regenerates the `README.md` table dynamically, enforcing parity via CI check.
