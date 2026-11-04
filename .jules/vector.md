## 2023-10-27 - `parse_scopes` explicitly supports iterable input and deduplicates naturally
**Learning:** `parse_scopes` allows `str | Iterable[str]`. This means that you can pass multiple scope iterables (or merged iterables via `(*a, *b)`) back to `parse_scopes`, and it handles both the flattening of comma-separated components and deduplication efficiently, without explicitly materializing an intermediate set. Wait, `add_scopes` concatenates list elements but `parse_scopes` preserves order and deduplicates. In `parse_scopes`:
```python
    cleaned = (part.strip() for item in source for part in item.split(","))
    return [Scope(part) for part in dict.fromkeys(p for p in cleaned if p)]
```
`dict.fromkeys` ensures deduplication! So `parse_scopes((*parse_scopes(existing), *parse_scopes(to_add)))` works perfectly, returning a deduplicated, ordered list!

**Action:** When working with DB string fields representing collections, prefer creating a pure, centralized FP-style transformation helper module (like `authz.py`) instead of keeping mutation and state manipulations ad-hoc in CLI or domain code. Leverage Python's `dict.fromkeys` and iterables for order-preserving stable deduplication without having to construct a `set` just to get O(1) deduplication if you need ordering.
