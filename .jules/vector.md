## 2024-03-20 - Centralize scope string parsing pipelines
**Learning:** Comma-separated scope parsing and formatting was scattered across the CLI, auth endpoints, and dependency checks, using manual chained transformations like `filter(None, map(str.strip, scopes.split(",")))`. This creates duplication and risk of subtle bugs (like empty parts or order instability).
**Action:** Always use pure, centralized parsing functions (e.g., `parse_scopes`, `format_scopes`) for normalizing string-encoded domain properties rather than repeating mutation-heavy or chained string operations inline.
