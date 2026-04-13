## 2024-04-13 - Centralize Scope Parsing
**Learning:** Parsing comma-separated lists to and from database text columns was being repeatedly re-implemented across different modules, leading to subtle style variations and potential drift.
**Action:** Extracted pure, functional helpers into `h4ckath0n.auth.scopes` for parsing and formatting. These helpers are tested directly, ensuring consistent deduplication, whitespace stripping, and order preservation across the codebase.
