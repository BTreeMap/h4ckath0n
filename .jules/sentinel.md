## 2024-05-24 - User Enumeration Timing Attack in Login
**Vulnerability:** The password authentication endpoint returned immediately if an email was not found in the database.
**Learning:** Because Argon2 hashing is intentionally slow, an attacker could observe the response times to determine if an email exists in the system (user enumeration).
**Prevention:** Ensure consistent execution time by performing a dummy password hash verification even when the user is not found or doesn't have a password set.
