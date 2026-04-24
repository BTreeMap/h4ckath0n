## 2024-04-24 - Fix User Enumeration via Timing Attack
**Vulnerability:** User enumeration timing attack
**Learning:** When mitigating timing attacks with argon2-cffi, dummy hash verification must use a structurally valid hash string to avoid early parsing exception
**Prevention:** Use a structurally valid Argon2id hash string for dummy verifications.
