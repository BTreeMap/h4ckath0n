## 2024-03-21 - [Prevent User Enumeration via Timing Attacks in Auth]
**Vulnerability:** [User enumeration possible because authentication returns immediately when a user is not found or lacks a password hash, skipping the expensive hashing operation.]
**Learning:** [Early returns that bypass expensive cryptographic operations create a detectable timing difference, allowing attackers to check if an email or username exists in the system.]
**Prevention:** [Ensure consistent execution time by performing a dummy password hash (`hash_password(password)`) when a user is not found or lacks a password hash. Also, offload this CPU-bound hashing operation to a worker thread using `asyncio.to_thread` to prevent blocking the asynchronous event loop.]
