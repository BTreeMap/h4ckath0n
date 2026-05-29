## 2025-04-23 - Timing Attack on Authentication
**Vulnerability:** The `authenticate_user` function returns early if the user is not found or has no password hash. This allows attackers to enumerate registered email addresses by observing the response time difference (Argon2id hashing takes ~300ms, while early return is <1ms).
**Learning:** Even if a standard password hashing algorithm like Argon2 is used, timing side-channels during the user lookup phase can still bypass intended security properties by leaking account existence.
**Prevention:** Always perform a dummy verification with a structurally valid hash string when the actual verification cannot be performed (e.g., user not found or no password set) to ensure a constant-time response curve across all authentication attempts.
