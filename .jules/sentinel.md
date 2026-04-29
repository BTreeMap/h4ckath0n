## 2025-03-08 - Prevent User Enumeration via Timing Attack in Authentication
**Vulnerability:** User enumeration timing attack. `authenticate_user` returned early if a user wasn't found or lacked a password, allowing attackers to distinguish valid emails based on response times since Argon2 is computationally expensive.
**Learning:** During authentication, always perform the expensive password verification even when the user is not found to normalize response times. The dummy hash verified against must be a structurally valid hash string to avoid early parsing exceptions bypassing the timing mitigation.
**Prevention:** In auth flows, use a valid dummy Argon2id hash and verify the user's password against it when the lookup fails or the hash is missing.
