## 2024-05-24 - User Enumeration via Timing Attacks in Auth
**Vulnerability:** `authenticate_user` returned early when a user was not found or lacked a password hash, bypassing the expensive cryptographic operation. This exposed the application to user enumeration via timing attacks.
**Learning:** Early returns in authentication flows that skip expensive operations (like password hashing) create timing discrepancies that attackers can exploit to verify the existence of users.
**Prevention:** Always ensure consistent execution time in authentication flows by performing dummy cryptographic operations (e.g., `hash_password(password)`) when a user is not found or lacks a password hash.
