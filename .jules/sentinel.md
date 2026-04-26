
## 2024-04-26 - Timing Attack Mitigation in Authentication
**Vulnerability:** User enumeration via timing attack in `authenticate_user`. When a user was not found or had no password hash, the function returned immediately without executing the expensive Argon2id hashing operation, allowing an attacker to determine if an email address exists by measuring response times.
**Learning:** Python's `argon2-cffi` library raises an early `InvalidHashError` exception if the provided hash string is not structurally valid (e.g., if you just pass "dummy"). This exception bypasses the hashing algorithm completely, meaning the timing attack mitigation fails.
**Prevention:** Always use a structurally valid Argon2id hash string (e.g., `$argon2id$v=19$m=65536,t=3,p=4$dHVtYmFzYWx0$dHVtYmFoYXNo`) for dummy verifications when mitigating timing attacks to ensure the algorithm performs the full computational work and normalizes response times.
