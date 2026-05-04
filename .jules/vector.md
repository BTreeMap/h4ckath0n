## 2024-05-04 - Centralizing Scope Normalization
**Learning:** The codebase repeatedly performed ad hoc, manual normalization of the `scopes` string using string manipulations like `filter(None, map(str.strip, scopes.split(",")))` across API dependencies, route handlers, and the CLI. These were mutable and duplicated.
**Action:** Extract pure transformation helpers like `parse_scopes` and `format_scopes` inside the relevant domain schemas (e.g. `h4ckath0n.auth.schemas`) to centralize logic and ensure deterministic behavior across the app without circular dependencies.
