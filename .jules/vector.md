## 2024-07-31 - Centralizing Domain Operations
**Learning:** The CLI tool repeated string-based manipulation of comma-separated "scopes" across sub-commands instead of treating them as value objects with centralized operations.
**Action:** When extracting such logic, look for the lowest-level parsing utility (e.g., `parse_scopes` and `serialize_scopes` in `authz.py`) and compose new pure helpers on top of it.
