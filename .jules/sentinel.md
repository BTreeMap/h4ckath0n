## 2024-11-20 - Fix JWT Privilege Escalation in Device Auth
**Vulnerability:** Device-bound JWTs did not verify if the JWT `sub` (subject/user ID) matched the `user_id` of the `device` record used to sign it.
**Learning:** Cryptographic signature verification only proves the key was used, but does not bind the operation to the key owner's identity unless explicitly enforced. An attacker could sign a JWT using their own device key but set `sub` to an admin's ID, successfully authenticating as the admin.
**Prevention:** Always ensure the subject of a token securely aligns with the identity associated with the signing credentials. For device authentication, explicitly check `claims.sub == device.user_id`.
