## 2024-05-24 - Mitigate User Enumeration Timing Attack
**Vulnerability:** The password authentication routine (`authenticate_user` in `src/h4ckath0n/auth/service.py`) returns early if a user is not found or has no password hash. This bypassed the expensive Argon2 password hashing step, creating a timing discrepancy that allowed attackers to enumerate existing email addresses or determine if a user uses passkeys.
**Learning:** Even early returns or validations must be careful not to create significant timing discrepancies when dealing with expensive cryptographic operations on a hot path like authentication.
**Prevention:** Perform a dummy password hash (`hash_password(password)`) to consume an equivalent amount of time before returning when a user is missing or has no password hash.
