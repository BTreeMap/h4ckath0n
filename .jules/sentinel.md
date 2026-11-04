## 2026-10-03 - Missing HSTS Header in API Template
**Vulnerability:** The API template in `packages/create-h4ckath0n/templates/fullstack/api/app/middleware.py` was missing the `Strict-Transport-Security` (HSTS) header for production environments.
**Learning:** The `CSPMiddleware` handles multiple security headers but HSTS was omitted, leaving applications scaffolded from this template vulnerable to protocol downgrade attacks.
**Prevention:** Always verify that `Strict-Transport-Security` is included in security header middleware for production deployments.
