## 2025-03-05 - User Enumeration Timing Attack in Authentication
**Vulnerability:** The password authentication endpoint was susceptible to user enumeration via timing attack. It returned immediately when an email was not found, but performed an expensive Argon2 hash verification when the user was found.
**Learning:** This is a classic timing attack vulnerability, where the response time reveals whether an email is registered or not. It existed because the early return optimization bypassed the hash verification.
**Prevention:** Always ensure constant-time processing for authentication requests, even for invalid users. When an early return is necessary, execute a dummy verification (e.g., using a pre-computed dummy hash) to normalize response times.
