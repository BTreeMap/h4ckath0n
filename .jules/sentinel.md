## 2024-05-15 - User Enumeration via Timing Attack in Authentication
**Vulnerability:** The authentication endpoint returns early if a user is not found, allowing an attacker to determine if a given user exists by measuring request duration.
**Learning:** When mitigating this with dummy password hashing, the dummy hash string must be structurally valid for Argon2id (e.g. `$argon2id$v=19$...`). Invalid dummy strings cause the verify function to raise an early parsing exception, defeating the timing mitigation.
**Prevention:** Always use structurally valid hashes for constant-time failure mechanisms.
