## 2024-05-24 - Mitigate User Enumeration Timing Attack with Dummy Hash
**Vulnerability:** The `authenticate_user` function returned immediately if a user didn't exist, enabling timing-based user enumeration attacks.
**Learning:** To avoid timing attacks, computationally expensive password verification must run regardless of user existence. The dummy hash used must be a fully valid, structurally correct Argon2id string. Otherwise, `argon2.PasswordHasher.verify` fails fast with a decoding error, bypassing the delay.
**Prevention:** Always perform constant-time verification when dealing with passwords, using a structurally correct dummy hash as a fallback if the user or hash is not found.
