
## 2024-06-23 - Timing Attack in User Authentication
**Vulnerability:** The `authenticate_user` function returned early if a user was not found or lacked a password hash, skipping the slow argon2 password verification. This exposed a timing difference that attackers could use to enumerate valid email addresses.
**Learning:** Returning early before expensive operations like hashing in authentication flows inadvertently leaks state.
**Prevention:** Always perform the expensive hashing operation, using a structurally valid dummy argon2id hash when the user or user's hash is not found, to ensure the verification time remains relatively constant.
