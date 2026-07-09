## 2024-07-09 - User Enumeration via Authentication Timing Attack
**Vulnerability:** Attackers could enumerate valid email addresses because invalid user logins returned significantly faster (no Argon2id hashing) than valid user logins.
**Learning:** Argon2id processing takes a perceptible amount of time (~150ms). When mitigating timing attacks by verifying a dummy hash, the dummy hash must be a structurally valid Argon2id string. Otherwise, `argon2-cffi` fails fast with a decoding error, bypassing the intended processing delay.
**Prevention:** Ensure authentication pathways take a constant amount of time regardless of whether a user exists or not, and always use structurally valid dummy hashes for timing attack mitigations.
