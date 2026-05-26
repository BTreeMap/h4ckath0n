## 2024-05-26 - Fix user enumeration timing attack in password authentication
**Vulnerability:** User enumeration timing attack was possible because invalid emails failed fast, while valid emails performed slow Argon2 hashing.
**Learning:** Returning early without running the hash function gives attackers a clear signal about whether a user account exists.
**Prevention:** Always perform a dummy hash comparison on a constant hash when an early return is necessary during authentication to equalize response times.
