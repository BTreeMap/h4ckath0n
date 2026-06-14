
## 2025-04-28 - Centralize Scope String Normalization
**Learning:** The database model `user.scopes` stores scopes as a comma-separated string. The logic to parse, manipulate, deduplicate, and format these strings was duplicated across multiple layers (CLI, dependencies, routers) with subtle variations that occasionally destroyed order or failed to trim whitespace correctly.
**Action:** When working with serialized collections (like CSV strings in the DB), extract pure `parse_*` and `format_*` pipelines into a domain-specific `schemas.py` module early to avoid circular imports and establish a single deterministic source of truth.
