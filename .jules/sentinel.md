## 2025-06-30 - Fix Argon2 Timing Attack in user authentication
**Vulnerability:** User enumeration vulnerability existed because `authenticate_user` returned early without verifying a password if the user didn't exist or had no password. This bypasses the processing delay of Argon2, exposing whether an email is registered.
**Learning:** Argon2 verification mitigates timing attacks by introducing a substantial delay. A dummy hash used to simulate this delay MUST be a structurally valid Argon2id string. Otherwise, `verify` fails fast with a decoding error, completely bypassing the intended delay.
**Prevention:** Always verify a validly formatted dummy hash when failing early in authentication flows.
