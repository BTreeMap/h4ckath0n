## 2024-05-23 - Timing Attack in Auth
**Vulnerability:** Username enumeration via timing attacks in `authenticate_user`.
**Learning:** Argon2 mitigations must use a structurally valid dummy hash string to prevent fail-fast decoding errors in `argon2-cffi`.
**Prevention:** Always verify passwords against a valid dummy hash even when the user is not found to ensure constant time execution.
