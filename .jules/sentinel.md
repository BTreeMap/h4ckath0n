## 2024-07-10 - Argon2id Timing Attack Mitigation
**Vulnerability:** Username enumeration via timing attacks in `authenticate_user`.
**Learning:** Argon2id is intentionally slow. If the application returns early when a user is not found without performing the hash verification, an attacker can distinguish between valid and invalid usernames by measuring response times. A structurally valid Argon2id dummy hash must be used; otherwise, `argon2.PasswordHasher.verify` fails fast with a decoding error, completely bypassing the intended processing delay.
**Prevention:** Always execute the slow hashing operation regardless of whether the user exists, using a valid dummy hash for non-existent users.
