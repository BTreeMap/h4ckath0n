## 2024-10-28 - Missing Strict-Transport-Security (HSTS) Header
**Vulnerability:** Missing `Strict-Transport-Security` (HSTS) header in the `CSPMiddleware` within `packages/create-h4ckath0n/templates/fullstack/api/app/middleware.py`.
**Learning:** A missing HSTS header allows attackers to downgrade HTTPS connections to HTTP via Man-in-the-Middle (MitM) attacks. Although CSP headers are present, defense-in-depth requires enforcing HTTPS, particularly in production environments.
**Prevention:** Ensure `Strict-Transport-Security: max-age=31536000; includeSubDomains` is unconditionally appended to all responses, enforcing HTTPS for all interactions.
