## 2026-06-15 - User Enumeration Timing Attack via Authentication Early Return
**Vulnerability:** The `authenticate_user` function was returning early without performing password verification when a user didn't exist or lacked a password hash, allowing timing attacks to enumerate users.
**Learning:** When mitigating timing attacks by using a dummy hash with Argon2, the dummy hash must be a structurally valid Argon2id string. Otherwise, the verification function will fail fast with a decoding error, failing to simulate the timing delay.
**Prevention:** Always verify a structurally valid dummy Argon2 hash when the actual user is not found to ensure consistent processing time.
