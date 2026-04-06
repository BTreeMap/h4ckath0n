## 2024-05-24 - Mitigated User Enumeration via Timing Attack
**Vulnerability:** Returning early without hashing allows attackers to enumerate users by measuring response times.
**Learning:** When using `argon2-cffi` to mitigate timing attacks via dummy password verification, ensure the dummy hash is a structurally valid Argon2id hash string. Passing an invalidly formatted string causes `verify_password` to raise an early parsing exception, which defeats the timing mitigation.
**Prevention:** Always use a structurally valid dummy hash when simulating authentication steps for non-existent users.
