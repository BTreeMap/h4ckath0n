## 2025-02-23 - JWT Privilege Escalation
**Vulnerability:** JWT `sub` claim was not verified against the signing device's `user_id`.
**Learning:** In a device-bound JWT architecture, the cryptographic signature proves possession of the device key, but it does not inherently guarantee the device belongs to the user asserted in the JWT payload. Relying solely on the signature without checking the binding allows a compromised or malicious device to sign tokens asserting identity of other users.
**Prevention:** Always explicitly validate that the identity asserted in a token (`sub`) matches the identity associated with the cryptographic material used to sign it (`device.user_id`).
