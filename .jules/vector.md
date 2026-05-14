
## 2024-05-14 - Centralise scope normalisation and parsing
**Learning:** The project stores scopes as comma-separated strings in the database, leading to ad hoc `scopes.split(",")` and local normalisation logic scattered across the codebase.
**Action:** Extract and standardise string normalisation into pure helpers (`parse_scopes`, `format_scopes`, `normalize_scope_list`) within a dedicated `scopes.py` module to ensure consistent semantics, deterministic ordering, and reusability, especially for authorization dependencies and CLI mutation logic.
