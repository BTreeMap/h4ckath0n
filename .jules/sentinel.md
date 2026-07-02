## 2024-04-22 - Prevent User Enumeration Timing Attack
**Vulnerability:** The `authenticate_user` function returned early if a user was not found or had no password hash, allowing attackers to measure response times and enumerate valid email addresses.
**Learning:** When using Argon2 or other slow hash functions, returning early leaks whether an account exists. A structurally valid dummy hash must be verified to equalize processing time without triggering `InvalidHashError`.
**Prevention:** Always use a dummy password verification using a properly formatted dummy hash (e.g., `$argon2id$v=19$...`) when looking up invalid or missing users in an authentication flow.
