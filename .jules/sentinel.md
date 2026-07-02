## 2023-10-24 - [Timing Attack in authenticate_user]
**Vulnerability:** The `authenticate_user` function was vulnerable to a timing attack / user enumeration. If the user was not found, the function returned early instead of computing the argon2 password hash. Valid users took ~130ms, while invalid users took ~1ms.
**Learning:** Returning early when checking existence before doing a computationally expensive task creates an easily exploitable timing difference that reveals valid users.
**Prevention:** Always verify a dummy hash if the user or the user's password hash is not found to equalize the response time, and carefully ensure that doing so does not result in a valid authentication if an attacker magically guessed the dummy hash's original password.
