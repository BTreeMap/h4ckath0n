## 2024-05-10 - Fix Timing Attack in Password Authentication
**Vulnerability:** User Enumeration via Timing Attack in `authenticate_user`
**Learning:** Early returns when a user is not found or has no password hash bypassed the expensive Argon2id hash verification. An attacker could measure response times to enumerate valid users.
**Prevention:** Always perform a dummy password verification using a valid dummy hash string (`_DUMMY_HASH`) when the user is not found or has no password, ensuring the response time remains constant regardless of whether the user exists. Also, `verify_password` must be able to catch `InvalidHashError` alongside `VerifyMismatchError`.
