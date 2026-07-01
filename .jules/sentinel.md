## 2024-07-01 - User Enumeration via Timing Attack
**Vulnerability:** Login endpoint returned immediately if user didn't exist, enabling timing attacks to enumerate valid emails.
**Learning:** In `authenticate_user`, early exits bypassed Argon2 password hashing. Argon2's `verify` needs a structurally valid dummy hash string to process correctly without throwing a fast decode error.
**Prevention:** Always execute the password hashing function with a valid dummy hash when the user is not found to equalize response times.
