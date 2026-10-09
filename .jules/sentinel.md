## 2025-02-14 - Prevent CPU Exhaustion DoS in Password Auth
**Vulnerability:** The password authentication schema in `h4ckath0n` lacked a maximum length constraint. Although `argon2-cffi` is robust, hashing extremely long strings (e.g. 1MB or 100MB) blocks threads and consumes excessive CPU time, making it a viable Denial of Service (DoS) vector on login/registration endpoints.
**Learning:** Pydantic models handling unhashed sensitive data must always implement reasonable `max_length` constraints before computationally expensive cryptographic functions are called.
**Prevention:** When validating inputs destined for KDFs or hashing functions, verify that Pydantic `Field` validation explicitly caps the string length (e.g., `max_length=1024`).
