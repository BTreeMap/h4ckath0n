# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2026-03-01 - Avoid False Positives in Table Column Matches

**Learning:** When asserting presence of markdown table routes using a regular expression like `\|\s*\`GET\`\s*\|\s*\`/path\`\s*\|`, the regex correctly matches only exactly bounded cells, effectively solving the issue where substring matching triggers false positives.
**Action:** Always combine the `METHOD` and `path` into a strict pattern that mirrors its structural context (like a table row or code block) rather than relying on loose string matching in documentation.
