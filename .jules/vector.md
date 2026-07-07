## 2026-07-07 - Centralize scope parsing
**Learning:** Extracted multiple places doing parsing arrays, splitting them by commas, and deduplicating arrays manually by updating  to support variadic inputs. This makes parsing of scopes consistent everywhere. Ruff linting fails when fixing imports sometimes and running `ruff format` after checking code helps.
**Action:** Next time prefer modifying core extraction utility rather than trying to replicate same logic on callers and running checks multiple times.
## 2026-07-07 - Centralize scope parsing
**Learning:** Extracted multiple places doing parsing arrays, splitting them by commas, and deduplicating arrays manually by updating parse_scopes to support variadic inputs. This makes parsing of scopes consistent everywhere. Ruff linting fails when fixing imports sometimes and running ruff format after checking code helps.
**Action:** Next time prefer modifying core extraction utility rather than trying to replicate same logic on callers and running checks multiple times.
