
## 2026-03-30 - Mitigate User Enumeration Timing Attack in Auth
**Vulnerability:** The authentication flow returned early if a user was not found or had no password, causing a measurable timing difference compared to when a valid user with a password was checked. This allowed attackers to enumerate valid email addresses.
**Learning:** Argon2 hashing is intentionally slow and CPU-intensive. Skipping the verification step for invalid users creates a large timing disparity.
**Prevention:** Always perform a dummy password verification using a static dummy hash even when the user is not found to normalize the response time.
