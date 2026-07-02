## 2025-05-03 - Timing Attack Mitigation in Authentication
**Vulnerability:** User enumeration vulnerability via timing attack in `authenticate_user`. The function returned early for non-existent users, skipping the expensive password hash verification and allowing attackers to identify valid emails by measuring response times.
**Learning:** Python web applications using Argon2 or bcrypt can easily leak user existence if the authentication flow does not perform constant-time operations for both valid and invalid users.
**Prevention:** Always verify a structurally valid dummy hash (e.g., `$argon2id$...`) when a user is not found to equalize the response time of the authentication endpoint.
