## 2025-02-28 - Centralize Scope Normalization
**Learning:** Parsing and formatting comma-separated strings (like scopes) inline using `.split(",")` across modules causes duplicate parsing logic, implicit side-effects, and order-stability risks.
**Action:** Always extract such string normalization into centralized, pure, highly composable helper pipelines (e.g. `parse_scopes`, `normalize_scopes` using `filter`, `map`, `dict.fromkeys`) rather than scattering it across files.
