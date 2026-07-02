
## 2024-05-20 - Fix User Enumeration Timing Attack
**Vulnerability:** A timing attack was possible on the `authenticate_user` function. When a user did not exist or had no password hash, the function returned early without attempting to verify the password, taking significantly less time than a failed login for an existing user.
**Learning:** Early returns in authentication flows create a timing discrepancy that attackers can exploit to enumerate registered users.
**Prevention:** Always ensure constant-time processing for authentication. When a user is not found, execute a dummy password verification against a pre-computed constant hash to normalize response times.
