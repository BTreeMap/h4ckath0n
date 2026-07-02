## 2024-06-24 - Fix Timing Attack in authenticate_user
**Vulnerability:** Timing attack possible during login because `authenticate_user` returns instantly if the user doesn't exist, but takes time to hash the password if they do exist.
**Learning:** `argon2-cffi` needs a structurally valid dummy hash (`$argon2id$v=19$...`) to actually perform the dummy verification. Using an invalid string fails instantly.
**Prevention:** Always use a structurally valid Argon2id dummy hash for timing attack mitigation.
