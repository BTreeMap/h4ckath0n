
## 2024-05-24 - Fix User Enumeration via Timing Attack
**Vulnerability:** User enumeration is possible via timing attacks during password authentication because `verify_password` is not called when the user does not exist or lacks a password.
**Learning:** When mitigating timing attacks during authentication (e.g., using `argon2-cffi`), the dummy password verification must use a structurally valid Argon2id hash string (e.g., `$argon2id$v=19$...`). Invalid formats trigger an early `InvalidHashError` or `VerifyMismatchError` exception bypassing the timing mitigation and allowing user enumeration.
**Prevention:** Always ensure a timing-safe path using a valid dummy hash is taken when early exiting authentication checks based on missing records or un-hashed users.
