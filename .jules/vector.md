## 2024-03-24 - Centralize scopes formatting and parsing
**Learning:** List and sequence string conversions to/from database text columns were scattered with inline `split`, `join`, and `filter` logic, leading to duplicate semantics and bug-prone edge cases.
**Action:** Created centralized pure functional utilities `parse_scopes` and `format_scopes` in `h4ckath0n.auth.scopes` to consistently manage trimming, deduplication, and order preservation when mapping to sequence strings.
