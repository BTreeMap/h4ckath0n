## 2024-05-29 - Prevent User Enumeration Timing Attacks in Password Authentication

**Vulnerability:** The password authentication endpoint was returning early if a user was not found or if the user had no password hash. This allowed attackers to enumerate existing email addresses based on timing differences (a user with a password took ~230ms longer to return than an unknown user).
**Learning:** Early returns in authentication flows, especially before computationally expensive operations like password hashing (Argon2), leak information about the existence of accounts.
**Prevention:** Always ensure constant-time processing. When an early return is otherwise necessary (e.g., user not found), execute a dummy password verification against a pre-computed constant hash to normalize response times before returning failure.
