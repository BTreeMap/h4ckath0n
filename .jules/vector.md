
## 2024-04-27 - Centralized scope parsing pipeline
**Learning:** Parsing comma-separated string logic like scopes was scattered with inline `.split(",")` calls causing brittle and repeated edge-case handling across CLI and routers.
**Action:** Centralized extraction and normalization logic into pure helper pipelines (`h4ckath0n.scopes`) to maintain FP style composability and provide one robust source of truth.
