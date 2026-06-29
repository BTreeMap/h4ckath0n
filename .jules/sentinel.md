## 2024-06-29 - Argon2id Dummy Hash Structure
**Vulnerability:** User enumeration via timing attack in login and registration endpoints.
**Learning:** When mitigating timing attacks using a dummy hash with `argon2-cffi`, the dummy hash must be a fully valid, structurally correct Argon2id string. If an invalid format is used, `argon2.PasswordHasher.verify` fails fast with a decoding error, completely bypassing the intended processing delay.
**Prevention:** Always generate an actual valid hash for the dummy value using the exact Argon2 parameters expected by the application instead of using placeholder strings.
