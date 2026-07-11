## 2025-02-18 - Prevent timing attacks in user authentication
**Vulnerability:** User enumeration via timing attack in `authenticate_user`.
**Learning:** Returning early when a user is not found skips the expensive password hashing verification, allowing an attacker to enumerate valid email addresses based on response times.
**Prevention:** Always perform a dummy password hash verification when the user is not found or has no password hash set, ensuring constant-time responses.
