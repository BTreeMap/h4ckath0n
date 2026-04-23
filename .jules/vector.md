## 2025-02-18 - Extract pure scopes helpers
**Learning:** The codebase previously duplicated comma-separated string normalization logic for `user.scopes` across dependencies, API routes, and the CLI layer using ad-hoc `split(",")`, `strip()`, and `filter(None, ...)` pipelines. This creates subtle drift and makes the logic harder to test in isolation.
**Action:** Create centralized, pure functional helpers (`parse_scopes` and `format_scopes`) with robust unit tests, and replace ad-hoc mutation and splitting across call sites to ensure a single source of truth for text-column array shaping.
