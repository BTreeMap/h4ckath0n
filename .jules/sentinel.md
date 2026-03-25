## 2024-05-24 - Fix User Enumeration via Timing Attack
**Vulnerability:** User enumeration timing attack in `authenticate_user`.
**Learning:** The authentication logic skipped expensive password hashing (`verify_password`) when a user email was not found. This allowed an attacker to enumerate valid email addresses based on response times.
**Prevention:** Always perform a dummy password hash (`hash_password(password)`) when an email is not found to ensure consistent execution time.
