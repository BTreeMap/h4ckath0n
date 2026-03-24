## 2025-03-24 - Prevent User Enumeration via Timing Attack
**Vulnerability:** User enumeration timing attack in `authenticate_user`.
**Learning:** Non-existent users or passkey-only users triggered an early return, bypassing the expensive Argon2 password hashing. An attacker could measure response times to determine if an email is registered.
**Prevention:** Always perform a dummy password hash (`hash_password(password)`) when a user is not found or lacks a password hash to ensure consistent execution time.