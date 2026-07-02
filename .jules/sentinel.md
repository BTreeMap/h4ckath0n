
## 2024-06-19 - Timing Attack in User Authentication
**Vulnerability:** User enumeration via timing attack in `authenticate_user`. The function returned immediately for non-existent users (or users missing a password hash), while spending significant CPU time calculating the Argon2id hash for existing users.
**Learning:** Argon2id is intentionally slow to prevent brute force, making it highly susceptible to timing attacks. An attacker could measure response times to accurately build a list of valid email addresses. Using a dummy hash allows the function to consume a similar amount of CPU cycles for missing users.
**Prevention:** Whenever verifying passwords or other secrets computationally, always ensure the failure path executes a dummy operation taking identical time as the success path. The dummy hash itself must be fully valid (structurally correct Argon2id) to ensure the verification function performs the expensive calculation instead of failing fast on a format error.
