## 2024-05-01 - Fix timing attack in authenticate_user
**Vulnerability:** Timing attack allowing email enumeration during login because password verification was skipped if user didn't exist.
**Learning:** Returning early without doing the same amount of work lets attackers map existing emails based on response times. When using `argon2-cffi`, the dummy hash must be a structurally valid Argon2id hash.
**Prevention:** Always verify a dummy hash of equivalent cost when early-exiting from an authentication flow to normalize the response times.
