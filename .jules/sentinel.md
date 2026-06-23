## 2024-04-08 - Prevent User Enumeration via Timing Attacks
**Vulnerability:** The authentication endpoint leaked whether an email existed by returning early when a user was not found or lacked a password, skipping the computationally expensive Argon2 verification.
**Learning:** When mitigating timing attacks with `argon2-cffi` by verifying a dummy password, the dummy hash must be a structurally valid Argon2id string. An improperly formatted string causes an early parsing exception in `verify_password`, entirely defeating the timing mitigation.
**Prevention:** Always verify a structurally valid dummy hash when the user is not found to ensure consistent execution time.
