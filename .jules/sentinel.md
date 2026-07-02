## 2024-05-08 - Fixed user enumeration timing attack in authentication

**Vulnerability:**
The `authenticate_user` function performed an early return when a user was not found by email or didn't have a password hash, avoiding the slow Argon2 password verification. This allowed an attacker to enumerate valid email addresses by measuring the server's response time (invalid users returned quickly, valid users returned slowly).

**Learning:**
Mitigating timing attacks with Argon2 requires the dummy hash to be a structurally valid Argon2id hash string (e.g., `$argon2id$v=19$...`). Using an invalid format like `$argon2id$dummy` triggers an early `InvalidHashError` exception in `argon2-cffi`, bypassing the intended timing mitigation.

**Prevention:**
Always execute the slow hashing/verification step even when intermediate checks fail. When using Argon2, generate a valid dummy hash for the application and verify the provided password against it when the real user or hash is not available. Ensure the dummy hash is declared at the module level *after* imports to prevent Ruff formatting errors (E402).
