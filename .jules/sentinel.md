## 2024-05-02 - Mitigating Timing Attacks in User Authentication
**Vulnerability:** User enumeration via timing attack in `authenticate_user`. The system exited early if an email was not found, making valid but incorrect logins computationally more expensive (and thus slower) than invalid ones.
**Learning:** By utilizing an invalid but structurally correct Argon2id dummy hash, we ensure the timing of `verify_password` calls remain consistent across both valid and invalid login attempts.
**Prevention:** Always ensure that authentication endpoints process failed user lookups in roughly the same amount of time as incorrect password attempts against existing users. This involves explicitly calling dummy verification routines rather than failing fast.
