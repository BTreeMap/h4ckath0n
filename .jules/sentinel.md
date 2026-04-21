## 2024-05-24 - Fix User Enumeration Timing Attack
**Vulnerability:** User enumeration timing attack in `authenticate_user` due to early return when user not found, bypassing Argon2id verification.
**Learning:** When using computationally expensive password hashing, early returns for non-existent users allow attackers to harvest valid email addresses by measuring response times. The verification step must be structurally identical whether the user exists or not.
**Prevention:** Always verify a structurally valid dummy Argon2id hash when the user is not found or has no password set. Ensure the dummy hash has the correct format so it triggers the full computation instead of failing early with an `InvalidHashError`.
