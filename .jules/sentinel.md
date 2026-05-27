## 2024-05-27 - Prevent User Enumeration Timing Attacks in Authentication
**Vulnerability:** Timing attack allowing user enumeration in `authenticate_user` because password hashing was skipped when a user or password hash was missing.
**Learning:** Early returns in authentication flows leak information via response timing.
**Prevention:** Always execute a constant-time dummy password verification using a pre-computed hash if the user doesn't exist, to normalize response times.
