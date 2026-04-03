## 2024-04-03 - Centralize semantic string splitting
**Learning:** Normalizing and splitting comma-separated database fields (like scopes) was duplicated across the CLI, auth dependencies, and routers using slightly different `split(",")` logic, risking semantic drift and ordering/trimming edge case bugs.
**Action:** Extracted pure `parse_scopes` and `format_scopes` functions into `src/h4ckath0n/auth/scopes.py`. This moves us to explicit FP-style transformation pipelines and centralizes the edge-case handling for empty items and whitespace.
