## 2025-04-28 - Timing Attack in Password Authentication
**Vulnerability:** The `authenticate_user` function returns early without verifying a hash if the user does not exist or has no password hash set. This leads to observable time differences, permitting user enumeration.
**Learning:** Returning early or skipping hash verification when a user is not found bypasses timing mitigations provided by the hashing algorithm.
**Prevention:** Always perform a dummy hash verification against a structurally valid Argon2id dummy hash when authentication fails early.
