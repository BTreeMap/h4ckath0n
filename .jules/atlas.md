## 2024-05-01 - Docs Env Vars Drift
**Learning:** Env vars described in the README drift quickly as new fields are added to `Settings` in `src/h4ckath0n/config.py`. For example, `H4CKATH0N_REDIS_URL`, `H4CKATH0N_SMTP_HOST`, `H4CKATH0N_STORAGE_DIR`, etc., were added to code but never documented in the README table.
**Action:** Use a script `scripts/generate_env_docs.py` to auto-generate the markdown table for env vars directly from `Settings.model_fields`, add `--check` support for CI, and integrate into the main CI pipeline to prevent future drift.

## 2024-05-01 - Docs Env Vars Drift
**Learning:** Env vars described in the README drift quickly as new fields are added to `Settings` in `src/h4ckath0n/config.py`. For example, `H4CKATH0N_REDIS_URL`, `H4CKATH0N_SMTP_HOST`, `H4CKATH0N_STORAGE_DIR`, etc., were added to code but never documented in the README table.
**Action:** Use a script `scripts/generate_env_docs.py` to auto-generate the markdown table for env vars directly from `Settings.model_fields`, add `--check` support for CI, and integrate into the main CI pipeline to prevent future drift.

## 2024-05-01 - Docs Env Vars Drift

**Learning:** Env vars described in the README drift quickly as new fields are added to `Settings` in `src/h4ckath0n/config.py`. For example, `H4CKATH0N_REDIS_URL`, `H4CKATH0N_SMTP_HOST`, `H4CKATH0N_STORAGE_DIR`, etc., were added to code but never documented in the README table.

**Action:** Use a script `scripts/generate_env_docs.py` to auto-generate the markdown table for env vars directly from `Settings.model_fields`, add `--check` support for CI, and integrate into the main CI pipeline to prevent future drift.
