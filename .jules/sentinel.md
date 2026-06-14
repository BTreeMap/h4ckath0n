## 2024-06-14 - Timing Attack on User Login
**Vulnerability:** User enumeration timing attack possible on the password login endpoint. Returning early if a user isn't found or lacks a password means an attacker can time responses and discover if an email exists in the system.
**Learning:** Argon2id hash verification is relatively slow. We must ensure the work done is constant, even for absent users.
**Prevention:** If the user is missing, compute a dummy verify on a pre-computed valid hash structure, so the response time matches the "user found, wrong password" case.
