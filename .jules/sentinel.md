## 2025-02-14 - Fix user enumeration timing attack in authentication
**Vulnerability:** User enumeration timing attack. `authenticate_user` returned early when a user was not found or had no password hash, causing authentication failures for invalid emails to process significantly faster than valid emails.
**Learning:** Early returns in authentication flows without constant-time operations leak whether an account exists, violating the principle of failing securely.
**Prevention:** Execute a dummy password verification using a pre-computed constant hash against the provided password whenever an early return is necessary due to user absence or missing password hash.
