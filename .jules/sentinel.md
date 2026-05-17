## 2025-02-28 - [Mitigate Authentication Timing Attacks]
**Vulnerability:** [User enumeration via timing attack in `authenticate_user`]
**Learning:** [When mitigating timing attacks with argon2, a structurally valid Argon2id hash must be used for the dummy verification to ensure constant time execution. An invalid hash triggers an early return and bypasses the timing mitigation.]
**Prevention:** [Always define and use a structurally valid dummy hash (`$argon2id$...`) when adding constant-time fallbacks for password verifications.]
