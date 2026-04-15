## 2025-04-15 - Centralized pure scope normalizer
**Learning:** Found scattered and subtly different `split(",")` logic across CLI, dependencies, and routers for user scopes.
**Action:** Always extract string formatting and normalization parsing logic into centralized, pure, highly composable helper pipelines (`iter`, `filter`, `dict.fromkeys`).
