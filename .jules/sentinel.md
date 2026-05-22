
## 2024-05-22 - User Enumeration Timing Attack
**Vulnerability:** The password authentication endpoint was susceptible to user enumeration timing attacks because `verify_password` was skipped if the user did not exist or had no password hash set, resulting in an early return.
**Learning:** Returning early on an invalid username creates a measurable timing difference between valid and invalid users when checking against an expensive Argon2 hash.
**Prevention:** Always ensure constant-time processing. When an early return is necessary due to a user not found, execute a dummy password verification against a pre-computed constant hash to normalize response times.
