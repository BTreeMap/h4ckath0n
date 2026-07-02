# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.
## 2024-06-22 - Centralizing environment variable documentation

**Learning:** When centralizing environment variable documentation for Pydantic V2 `BaseSettings`, using `pydantic.Field(default=..., description="...")` inline allows automated scripts to parse `Settings.model_fields` and generate accurate markdown tables, preventing drift between the config loader and the README. If `field.default` is `PydanticUndefined`, the dynamic default value can be retrieved by accessing `getattr(field, 'default_factory', None)`.
**Action:** For configuration-heavy projects, always define descriptions directly on the configuration models using Pydantic's Field and use a script to automatically verify or update the documentation tables using markdown markers.
