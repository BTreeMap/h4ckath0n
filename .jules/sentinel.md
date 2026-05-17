## 2024-06-25 - Fix user enumeration via timing attack in auth service
**Vulnerability:** User enumeration timing attack in `authenticate_user` allows attackers to determine if an email is registered by timing how long the request takes.
**Learning:** If a user is not found or has no password hash, returning early without hashing the password creates a noticeable timing difference compared to when a valid user is found and verified.
**Prevention:** Ensure consistent execution time by performing dummy password hashing (`hash_password(password)`) when a user is not found or lacks a password hash (e.g., passkey-only users). Avoid early returns that bypass expensive cryptographic operations.
