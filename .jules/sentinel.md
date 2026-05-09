## 2024-05-09 - [HIGH] Fix User Enumeration via Timing Attack
**Vulnerability:** User enumeration timing attack found in `authenticate_user`.
**Learning:** Returning `None` early on non-existent users allows attackers to deduce user existence based on the response time variance between checking a valid email (slow due to hashing) and an invalid one (fast). Dummy hashes must be structurally valid Argon2id hashes, not empty strings, to prevent early `InvalidHashError` exceptions.
**Prevention:** Always verify a hash (either the user's actual hash or a dummy hash) to maintain consistent timing regardless of user existence.
