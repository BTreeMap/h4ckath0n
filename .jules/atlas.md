## 2024-06-08 - Config Docs Drift
**Learning:** Env vars are frequently missing from documentation because there is no mechanism to enforce documenting them when they are added to `Settings` in `src/h4ckath0n/config.py`. Using backticks when searching prevents substring match issues.
**Action:** Created `scripts/generate_config_docs.py` to auto-generate the complete env var table in `docs/configuration/index.md` from `Settings.model_fields`, and `scripts/check_config_drift.py` to ensure all vars remain documented.
