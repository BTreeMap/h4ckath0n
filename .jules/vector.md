## 2026-05-01 - Scope String Parsing and Normalization

**Learning:** Scope formatting and normalization was originally duplicated across multiple places (`cli.py`, `dependencies.py`, `session_router.py`) leading to inconsistent application of whitespace trimming, deduplication, and parsing logic. The previous CLI mutation logic also relied heavily on temporary mutable structures (like `set` and `list`) and inline formatting `",".join(existing)`.

**Action:** When working with the user scopes domain, ALWAYS use `parse_scopes(scopes)` and `format_scopes(iterable)` from `h4ckath0n.auth.schemas`. These pure functional utilities enforce determinism, safely handle trailing/leading spaces and empty segments, and correctly preserve order during deduplication using `dict.fromkeys(scopes)`. Avoid building ad-hoc local strings or sets.
