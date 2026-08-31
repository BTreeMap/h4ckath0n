## 2024-10-24 - Privilege Escalation via JWT Subject Forgery
**Vulnerability:** `verify_device_jwt` failed to validate that the JWT `sub` claim matches the `user_id` of the `Device` that signed it.
**Learning:** Any user with a registered device could forge a validly signed JWT with the `sub` claim set to an admin's user ID, bypassing authorization because the signature was valid for the attacker's key.
**Prevention:** Always verify that claims within a cryptographic token securely map to the trusted metadata of the associated signing key (e.g., enforcing `claims.sub == device.user_id`).
