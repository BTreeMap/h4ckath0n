
## 2025-04-09 - Centralize sequence parsing for database text columns
**Learning:** Parsing comma-separated lists from text columns was scattered across multiple files using ad-hoc `split(",")` logic, leading to inconsistent handling of whitespace and deduplication order.
**Action:** Centralized the logic using pure functional helpers (`parse_scopes`, `format_scopes`) that handle splitting, stripping, and deterministic deduplication via `dict.fromkeys`.
