## 2024-06-27 - Timing Attack Mitigation with Argon2-cffi
**Vulnerability:** Email enumeration was possible because authenticating a non-existent user returned immediately without hashing the password, revealing whether the email existed based on response time.
**Learning:** When mitigating timing attacks using a dummy hash with `argon2-cffi`, the dummy hash must be a fully valid, structurally correct Argon2id string. If an invalid format is used, `argon2.PasswordHasher.verify` fails fast with a decoding error, completely bypassing the intended processing delay.
**Prevention:** Always use a structurally valid Argon2 hash string (e.g., generated via `PasswordHasher().hash("dummy")`) for constant-time comparisons when a user or hash is not found.
