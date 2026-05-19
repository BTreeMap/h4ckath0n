## 2024-05-24 - Timing Attacks in Password Authentication
**Vulnerability:** User enumeration timing attack in `authenticate_user`. The function was returning early without hashing the password if the user was not found or if the user did not have a password hash.
**Learning:** Returning early without hashing the password creates a noticeable timing difference between valid and invalid emails, allowing attackers to enumerate registered users.
**Prevention:** Always verify the password against a hash. If the user is not found or lacks a password hash, verify the password against a pre-computed dummy hash to ensure the operation takes a constant amount of time.
