## 2024-05-18 - User Enumeration Timing Attack
**Vulnerability:** The `authenticate_user` function returns early if the user is not found or has no password hash. This allows attackers to enumerate registered emails by measuring the response time, as Argon2id hashing is intentionally slow.
**Learning:** Returning early on an invalid username bypasses the slow hash verification, creating a noticeable timing difference.
**Prevention:** Always execute a dummy password verification against a pre-computed constant hash to normalize response times when a user is not found.
