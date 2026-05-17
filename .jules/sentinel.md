## 2024-05-18 - User Enumeration via Timing Attack in Auth Service
**Vulnerability:** User enumeration is possible because authenticating a missing user or a user without a password returns immediately, taking significantly less time than verifying a user with a valid password.
**Learning:** Returning early on authentication failures without performing cryptographic operations allows attackers to enumerate valid user accounts by measuring response times.
**Prevention:** Always perform a dummy cryptographic operation (like a dummy password hash) if the user is missing or lacks a password hash, to ensure constant-time execution and prevent timing side-channel attacks.
