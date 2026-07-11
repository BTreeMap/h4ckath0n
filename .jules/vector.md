## 2025-05-24 - Centralize and Harden Scope Parsing

**Learning:** Scope parsing in `h4ckath0n` involved ad-hoc comma splitting logic scattered across dependencies and CLI handlers. The existing `parse_scopes` was strictly typed for `str`, leading to duplicated manual collection lists and redundant set parsing when building requirements arrays.

**Action:** Upgraded `parse_scopes(str | Iterable[str])` to robustly accept, split, flatten, trim, and deduplicate iterables of scopes. This allows dependencies and CLI wrappers to just feed raw arguments to the central parser without manually breaking strings first. Reduces bugs related to embedded commas in CLI args.
