## 2024-05-15 - Mitigating User Enumeration Timing Attacks with Argon2

**Vulnerability:** The `authenticate_user` function returned immediately if a user was not found or lacked a password, allowing attackers to enumerate valid email addresses via timing differences.
**Learning:** To properly mitigate timing attacks with `argon2-cffi`, the dummy hash used for the delay *must* be a fully valid, structurally correct Argon2id string. If an invalid string (like `"dummy"`) is used, `argon2` fails fast with a decoding error, completely bypassing the intended computational delay.
**Prevention:** Always use a structurally valid dummy hash string (broken across lines to satisfy E501 length limits) to ensure the hashing algorithm performs the work, equalizing response times.
