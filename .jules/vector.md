## 2025-04-03 - Centralize DB text column parsing/formatting

**Learning:** This repo frequently stores lists/sequences (like user scopes) in single text columns. Previously, ad-hoc string manipulation (like `.split()`, `.strip()`, and manual deduplication) was repeated across auth dependencies, API routers, and CLI utilities.
**Action:** When converting lists or sequences to and from database text columns, use centralized, pure functional utilities (e.g., shared parsing and formatting helpers) rather than repeating ad-hoc string manipulation across multiple files.