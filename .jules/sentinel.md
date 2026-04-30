## 2024-05-24 - Prevent User Enumeration Timing Attacks in Argon2 Verification
**Vulnerability:** The `authenticate_user` function returned early for non-existent users, skipping the slow Argon2 verification step. This allowed user enumeration via timing attacks.
**Learning:** When using intentionally slow password hashing algorithms like Argon2, the verification step must always occur regardless of whether the user exists, using a structurally valid dummy hash, to normalize response times. Otherwise, invalid formats trigger an early exception, bypassing the mitigation.
**Prevention:** Ensure a dummy hash validation step is implemented for all branches where an invalid user or missing password hash is detected.
