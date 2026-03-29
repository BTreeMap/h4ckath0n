## 2026-03-29 - Prevent Timing Attacks in Auth
**Vulnerability:** User enumeration is possible via timing attacks because the `authenticate_user` function returns early without performing expensive cryptographic operations when a user is not found or lacks a password hash.
**Learning:** In asynchronous functions, early exits that bypass heavy operations (like password hashing) reveal state through execution time. Additionally, CPU-bound operations like Argon2 hashing can block the event loop.
**Prevention:** Always perform a dummy cryptographic operation (e.g., `hash_password(password)`) to ensure consistent execution time regardless of user existence. Offload these operations to worker threads using `asyncio.to_thread`.
