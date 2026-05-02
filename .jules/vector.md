## 2024-05-01 - Centralize scope parsing and formatting semantics

**Learning:** Ad-hoc list comprehension and filtering (e.g. `[s for s in user.scopes.split(",") if s]`) and set mutations were scattered across CLI, routers, and dependencies for managing scopes. In a Python repo heavily favoring functional programming, `dict.fromkeys(filter(None, map(str.strip, ...)))` creates a robust pure helper for order-preserving deduplication that replaces scattered mutation.

**Action:** Whenever a composite string format (like scopes or roles) is modified or read across multiple layers (CLI, routers, dependencies), centralize it into pure `parse_X` and `format_X` functional helpers rather than writing manual loops or set operations at each call site.
