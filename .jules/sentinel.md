## 2024-05-24 - Timing Attack Mitigation with Argon2id
**Vulnerability:** User enumeration timing attack during password authentication.
**Learning:** Returning early without verifying a dummy hash, or verifying an invalid hash format, triggers early returns or parsing exceptions that bypass the timing mitigation.
**Prevention:** Always verify a structurally valid dummy Argon2id hash when a user or password hash is not found.
