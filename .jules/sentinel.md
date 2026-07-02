## 2024-07-02 - Mitigating Argon2 Timing Attacks
**Vulnerability:** The password authentication endpoint was vulnerable to user enumeration via timing attacks because it returned early for non-existent users without performing an expensive hash verification.
**Learning:** When mitigating timing attacks using a dummy hash with `argon2-cffi`, the dummy hash must be a fully valid, structurally correct Argon2id string. If an invalid format is used, `argon2.PasswordHasher.verify` fails fast with a decoding error, completely bypassing the intended processing delay.
**Prevention:** Always use a real, pre-generated Argon2id hash of a known string (like an empty string) as the dummy hash to ensure the verification function consumes the expected amount of CPU time.
