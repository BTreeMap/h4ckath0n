## 2024-04-07 - Centralized FP Scope Parsing
**Learning:** When converting lists or sequences to and from database text columns (like comma-separated scopes), use centralized, pure functional utilities (e.g., the shared parsing and formatting helpers in `h4ckath0n.auth.scopes`) rather than repeating ad-hoc string manipulation (like `.split()`, `.strip()`, or `filter()`) across multiple files.
**Action:** Extracted `parse_scopes` and `format_scopes` to ensure a single source of truth for scope string normalization and deterministic formatting logic.
