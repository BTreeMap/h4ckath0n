## 2024-07-05 - User Enumeration Timing Attack
**Vulnerability:** The login endpoint was vulnerable to user enumeration via response timing differences because it returned early when a user was not found or lacked a password hash.
**Learning:** When mitigating timing attacks using a dummy hash with `argon2-cffi`, the dummy hash must be a fully valid, structurally correct Argon2id string. If an invalid format is used, `argon2.PasswordHasher.verify` fails fast with a decoding error, completely bypassing the intended processing delay.
**Prevention:** Always use a structurally valid dummy hash and ensure verification is run regardless of whether the user exists.
