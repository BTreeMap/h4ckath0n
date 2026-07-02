## $(date +%Y-%m-%d) - Prevent user enumeration via timing attacks
**Vulnerability:** The password authentication endpoint was susceptible to user enumeration timing attacks. Because password verification via Argon2 is intentionally slow, an attacker could measure response times to discover whether an email address exists in the database.
**Learning:** If a user is not found, returning immediately creates a timing disparity.
**Prevention:** Always execute the computationally expensive hash verification step (e.g. by hashing against a dummy hash) even when the user is not found, to ensure the authentication response time remains relatively constant.
