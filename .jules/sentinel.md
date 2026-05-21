## 2025-05-21 - User Enumeration Timing Attack
**Vulnerability:** User enumeration timing attack vulnerability in `authenticate_user` function.
**Learning:** Returning early when a user isn't found or has no password hash creates a timing difference, allowing an attacker to determine if an email is registered by timing the login request.
**Prevention:** Always perform constant-time validation paths. Execute a dummy verification step with a pre-computed constant hash when returning early to normalize response times.
