## YYYY-MM-DD - [Title]
**Learning:** [Important repo-specific insight]
**Action:** [How to apply or avoid this next time]

## 2024-05-16 - Centralize String Normalization
**Learning:** The project had repeated string normalization logic (split by comma, strip whitespace, remove empty elements, dedupe) for user scopes scattered across FastAPI dependencies and CLI operations. This duplication increased the risk of subtle bugs.
**Action:** Extract the shared parsing logic into a central, functional-style utility (`parse_scopes` / `format_scopes`) using pure helper functions, preserving existing project conventions (like deterministic ordering when deduplicating).
