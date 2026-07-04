
## 2024-05-18 - Centralize string normalization logic for domain types
**Learning:** Normalization of domain specific types, such as scopes (trimming, deduplication, filtering empty strings), scattered across ad-hoc loops and sets is an anti-pattern that creates subtle bugs and duplicated logic.
**Action:** Extract a pure, composable `clean_scopes(Iterable[str]) -> list[Scope]` helper function to serve as a single source of truth for scope parsing rules, and replace inline parsing at call sites.
