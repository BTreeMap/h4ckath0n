# Bolt Journal: Critical Learnings

## 2026-03-12 - Using Sets for O(1) Lookups in Scope Checks

**Learning:** `require_scopes` in `dependencies.py` iterates over a list of scopes for each request. Converting `user_scopes` to a set provides O(1) lookups, optimizing authorization checks on every authenticated request.
**Action:** Always convert lists to sets for O(1) membership testing in frequent operations, especially authorization.
