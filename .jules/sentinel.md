## 2024-05-18 - [Timing Attack Mitigation in Authentication]
**Vulnerability:** User enumeration timing attack in `authenticate_user` when returning early for non-existent users or empty password hashes.
**Learning:** Argon2id hash verification must use a structurally valid dummy hash string. Otherwise, `argon2-cffi` throws an early `InvalidHashError`, bypassing the timing mitigation and allowing timing attacks to persist.
**Prevention:** Always verify passwords against a well-formed dummy hash (`$argon2id$v=...`) to ensure execution time remains constant when the user is not found.
