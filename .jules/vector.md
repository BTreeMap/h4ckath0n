## $(date +%Y-%m-%d) - Centralize String Normalization
**Learning:** `user.scopes` was parsed inconsistently using ad-hoc `filter(None, map(str.strip, string.split(",")))` or list comprehensions or sets. Sets destroyed determinism during CLI mutations.
**Action:** Centralize order-preserving deduplication for comma-separated fields into pure formatters/parsers in their domain schema.
