## 2024-06-17 - User Enumeration Timing Attack

**Vulnerability:** User enumeration timing attack. `authenticate_user` returned immediately if a user didn't exist, taking significantly less time than verifying a hash for an existing user.
**Learning:** Returning early on authentication failure without performing the expensive hash verification allows attackers to enumerate valid email addresses based on server response times. Dummy hashes must be properly formatted for argon2id.
**Prevention:** Always perform the time-consuming operation (hash verification) against a dummy hash when the user doesn't exist to ensure constant-time responses for both valid and invalid usernames.
