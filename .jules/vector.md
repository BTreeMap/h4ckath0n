## YYYY-MM-DD - Centralize scope parsing
**Learning:** `parse_scopes` was being duplicated across CLI handling and route dependencies (e.g., ad-hoc comma splitting and whitespace stripping).
**Action:** Enhance `parse_scopes` to handle iterables of strings (`str | Iterable[str]`) and route all scope inputs (CLI, variadic dependencies) through it to prevent edge-cases where commas embedded in list items bypass deduplication.
