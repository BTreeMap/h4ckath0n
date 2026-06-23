## 2024-03-19 - User Enumeration Timing Attack
**Vulnerability:** The authentication service `authenticate_user` returned early when a user was not found or lacked a password hash. Attackers could measure the response time to determine if an email address was registered in the system (timing attack), since checking an invalid user took significantly less time than verifying a password hash with Argon2.
**Learning:** Returning early to avoid expensive cryptographic operations (like Argon2 hashing) creates a timing discrepancy that leaks user existence.
**Prevention:** Ensure consistent execution time regardless of user existence by performing a dummy password hash (`hash_password(password)`) when the user is not found or lacks a password.
