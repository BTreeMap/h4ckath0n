## 2025-02-28 - Timing Attack in Password Authentication
**Vulnerability:** User enumeration is possible because `authenticate_user` returns early without performing a password hash verification when a user does not exist or lacks a password.
**Learning:** When using `argon2-cffi` to mitigate timing attacks by hashing a dummy password, the dummy hash must be a structurally valid Argon2id string (e.g., `$argon2id$v=19$...`). Using an invalid format triggers an early `InvalidHashError`, bypassing the timing mitigation.
**Prevention:** Always define and use a structurally valid dummy hash in authentication routines to ensure consistent computation times.
