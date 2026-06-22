## 2024-05-24 - [Auth Timing Attack]
**Vulnerability:** Timing attack possible on `authenticate_user` when user doesn't exist.
**Learning:** `authenticate_user` returns early if user not found, skipping the expensive argon2 hash verification. This leaks whether an email is registered or not via response timing.
**Prevention:** Always perform a dummy hash verification when a user is not found to ensure constant-time response and prevent user enumeration.
