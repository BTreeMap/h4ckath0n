## 2024-05-23 - Argon2 Timing Attack Mitigation
**Vulnerability:** The authentication logic returned immediately when a user was not found, allowing attackers to enumerate valid email addresses based on response time.
**Learning:** Using `argon2-cffi` to mitigate timing attacks by verifying a dummy hash requires the dummy hash to be a fully valid, structurally correct Argon2id string. Otherwise, it fails fast with a decoding error and bypasses the processing delay.
**Prevention:** Always ensure the dummy hash is generated via Argon2 and structurally valid when implementing timing attack mitigations in Python.
