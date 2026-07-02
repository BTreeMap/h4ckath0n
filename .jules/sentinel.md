## 2024-05-14 - Timing Attack Mitigation in User Auth
**Vulnerability:** User enumeration is possible because authenticating non-existent users returns instantly, while valid users incur the delay of password hashing.
**Learning:** When mitigating timing attacks using dummy hashes with `argon2-cffi`, the dummy hash must be structurally valid (e.g., `$argon2id$v=19$...`). Passing an invalid string causes an early parsing exception, defeating the timing mitigation.
**Prevention:** Always use a structurally valid dummy hash generated from a real hasher instance when ensuring consistent execution time.
