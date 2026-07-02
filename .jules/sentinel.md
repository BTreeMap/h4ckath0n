## 2024-05-28 - Mitigate User Enumeration Timing Attack
**Vulnerability:** User enumeration via timing attack in `authenticate_user` endpoint. The application returned early if the user was not found or lacked a password hash, resulting in a noticeably faster response compared to verifying an Argon2 hash.
**Learning:** Argon2 is intentionally slow. Early returns before verifying a password hash allow attackers to accurately determine if an email is registered based on response time.
**Prevention:** Always ensure constant-time processing in authentication flows. Execute a dummy password verification against a pre-computed constant hash to normalize response times when a user is not found or has no password set.
