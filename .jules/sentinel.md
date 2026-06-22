## 2024-05-24 - User Enumeration Timing Attack
**Vulnerability:** User enumeration timing attack. Returning early from authentication when a user is not found makes it faster than verifying a real user, allowing an attacker to determine if an email address is registered.
**Learning:** Returning early on authentication flows leaks information through response times.
**Prevention:** To prevent user enumeration timing attacks in authentication flows, always ensure constant-time processing. When an early return is necessary (e.g., user not found), execute a dummy password verification against a pre-computed constant hash to normalize response times.
