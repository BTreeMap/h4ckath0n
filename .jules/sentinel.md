## 2024-05-24 - User Enumeration via Timing Attacks
**Vulnerability:** The `authenticate_user` function returns early when a user is not found or lacks a password hash, skipping the expensive Argon2id verification step.
**Learning:** This discrepancy allows attackers to enumerate registered users (or those with password auth) by measuring the response time.
**Prevention:** Mitigate timing attacks by always performing dummy password verification against a valid Argon2id hash when the actual user or their hash is missing.
