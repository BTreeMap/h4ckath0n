## 2024-09-01 - [FastAPI Route Extraction]
**Learning:** In recent versions of FastAPI, `app.routes` obfuscates dynamically nested endpoints inside `_IncludedRouter`. A script iterating over `app.routes` will fail to correctly extract paths and trigger `AttributeError: '_IncludedRouter' object has no attribute 'path'`.
**Action:** Always use `app.openapi().get("paths", {})` to correctly and reliably extract endpoints and their metadata for documentation drift-prevention scripts.
