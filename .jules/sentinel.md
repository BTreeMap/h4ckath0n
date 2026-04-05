## 2024-04-05 - Mitigate user enumeration via timing attacks in auth service
**Vulnerability:** The password authentication endpoint executed faster when a user did not exist or had no password, allowing an attacker to enumerate valid email addresses via timing differences.
**Learning:** Argon2 hashing is computationally expensive. Early returns before verifying a password expose observable timing disparities.
**Prevention:** Always perform a dummy password verification using a valid dummy hash when failing early in authentication flows to equalize response times.
