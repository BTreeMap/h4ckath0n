# Atlas Journal: Critical Learnings

## 2026-02-28 - API route substring matching is unreliable for drift checks

**Learning:** Checking whether a path string appears *anywhere* in a README causes false negatives
when one route's path is a substring of another (e.g. `/auth/passkeys/{key_id}` inside
`/auth/passkeys/{key_id}/revoke`). The drift check must match `METHOD /path` as a combined token,
ideally inside backtick delimiters, to avoid this trap.

**Action:** Always match method+path together in drift checks. Use `` `METHOD /path` `` patterns
that mirror the actual markdown formatting.

## 2023-10-27 - Automated Document Verification
**Learning:** Attempting to verify documentation drift by searching for inline substrings or isolated `METHOD /path` regex matches is prone to false positives/negatives, especially for grouped paths or partial matches. The most robust technique to prevent documentation drift for endpoints is to generate the entire markdown API route table directly from the OpenAPI schema, encapsulate it between HTML comments in `README.md`, and verify exact content equality in tests.
**Action:** When verifying documentation for API endpoints, always favor regenerating the content and diffing the text exactly between distinct boundary markers (e.g. `<!-- BEGIN ROUTES -->`).
