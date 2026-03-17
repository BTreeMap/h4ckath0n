## 2024-05-18 - Prevent User Enumeration via Timing Attack
**Vulnerability:** The `authenticate_user` function returned immediately if a user was not found or lacked a password hash, avoiding the expensive argon2 hash check. This timing difference allowed attackers to enumerate existing email addresses based on response time.
**Learning:** Returning early before an expensive cryptographic operation introduces a timing side-channel. Even if an early exit is computationally efficient, it leaks the state of the system (user existence).
**Prevention:** Perform a dummy execution of the expensive operation (e.g., hash the given password anyway) before returning when a condition fails, ensuring execution time is roughly constant regardless of the check's outcome.
