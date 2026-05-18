## 2024-05-18 - Prevent User Enumeration Timing Attacks
**Vulnerability:** The `authenticate_user` function returned immediately if a user was not found or lacked a password, leaking timing information that allowed user enumeration.
**Learning:** Returning early without verifying a dummy password allows an attacker to distinguish between invalid users and valid users with incorrect passwords because Argon2id verification takes noticeable time.
**Prevention:** Always perform a dummy password verification against a pre-computed constant hash when an early return is necessary (e.g., user not found) to normalize response times and prevent timing side-channel attacks.
