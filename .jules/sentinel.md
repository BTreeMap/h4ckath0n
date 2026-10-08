## 2024-10-08 - Auth Bypass via Missing Device-to-User Binding Check
**Vulnerability:** The device JWT verification `verify_device_jwt` does not verify if the JWT's `sub` claim (user ID) matches the user ID the device key (`kid`) is bound to in the database (`device.user_id`). It only checks if a user with that ID exists.
**Learning:** Any authenticated user can mint a valid device JWT for any other user's ID simply by signing it with their own registered device key and changing the `sub` claim, resulting in complete account takeover.
**Prevention:** When verifying device signatures, always verify that the device making the claim is cryptographically bound to the identity being claimed.
