## 2024-04-19 - Timing Attack Mitigation in Argon2id
**Vulnerability:** User enumeration via timing attack in `authenticate_user` because it returns early when a user is not found.
**Learning:** When mitigating timing attacks with `argon2-cffi`, the dummy hash must be a structurally valid Argon2id string. An invalid hash triggers an early `InvalidHashError` exception, bypassing the mitigation.
**Prevention:** Always use a real, pre-computed valid Argon2id hash (e.g. implicitly concatenated literal) for the dummy verification step to ensure identical execution paths.
