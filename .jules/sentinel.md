## 2024-05-24 - Fix user enumeration via timing attack in login
**Vulnerability:** The `authenticate_user` function returned immediately if an email wasn't found or a user had no password, taking significantly less time (~2ms) compared to a failed password attempt (~100ms+). This allowed attackers to enumerate valid email addresses based on response time.
**Learning:** Returning early during authentication functions before the slow cryptographic operations run allows timing attacks.
**Prevention:** Always perform a dummy slow operation (like `hash_password(password)`) when the primary check (like user existence) fails, so the function executes in constant-ish time.
