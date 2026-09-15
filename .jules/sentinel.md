## 2025-03-09 - Authorization bypass in verify_device_jwt
**Vulnerability:** A user can construct a valid JWT claiming the identity (`sub`) of another user, even if they use their own device key to sign it. This allows an attacker to escalate privileges or act as other users.
**Learning:** Device-bound JWTs must verify that the signing device is actually associated with the user claimed in the `sub` token field.
**Prevention:** In `verify_device_jwt`, always check that `device.user_id == claims.sub`.
