## 2023-11-20 - Device JWT Subject Spoofing
**Vulnerability:** Device-signed JWTs trusted the `sub` claim without verifying it matched the device owner's `user_id`, allowing a registered user to forge tokens for any other user (Privilege Escalation).
**Learning:** In a device-bound architecture, cryptographic signature validity only proves possession of the device key, not authorization for the claimed subject. The `sub` claim must always be bound to the hardware record.
**Prevention:** When verifying device JWTs, explicitly enforce `claims.sub == device.user_id`.
