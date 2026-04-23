## 2024-04-16 - Centralized Scope Parsing Pipeline
**Learning:** Parsing and formatting comma-separated strings (like scopes) using inline `.split(",")` leads to duplicated normalization logic and inconsistent behaviors.
**Action:** Extract logic into centralized, pure, highly composable helper pipelines (e.g., `parse_scopes` and `format_scopes` using `iter`, `filter`, `map`, and `dict.fromkeys`) rather than scattering mutation or split logic inline.
