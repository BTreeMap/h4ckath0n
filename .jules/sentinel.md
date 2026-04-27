
## 2024-04-27 - Fix timing attack in user authentication
**Vulnerability:** The `authenticate_user` function returned early if a user was not found or had no password hash, allowing an attacker to enumerate valid email addresses based on response time differences (Argon2 verification takes ~80ms, early return takes ~2ms).
**Learning:** The dummy password verification must use a structurally valid Argon2id hash string. An invalid hash format triggers an early parsing exception (`InvalidHashError`), which bypasses the timing mitigation and allows user enumeration.
**Prevention:** Always perform a dummy hash verification with a valid hash string when the user is not found or has no password hash to ensure constant-time response characteristics.
