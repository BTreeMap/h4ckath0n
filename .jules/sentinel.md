## 2026-04-11 - Mitigating Timing Attacks in Password Authentication
**Vulnerability:** User enumeration timing vulnerability in `authenticate_user`.
**Learning:** Returning early when a user is not found or has no password hash allows attackers to enumerate valid email addresses based on response time, since password hashing (Argon2id) takes significantly longer than a simple database lookup.
**Prevention:** Always verify a password against a hash, even if the user doesn't exist or has no password. Use a structurally valid dummy Argon2id hash (e.g. `$argon2id$v=19$...`) to avoid early parsing exceptions in `argon2-cffi` that would defeat the timing mitigation.
