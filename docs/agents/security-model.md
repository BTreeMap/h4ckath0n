# Security model

These are the opinionated security invariants that must be preserved on every change. The
authoritative design reference is [docs/security/frontend.md](../security/frontend.md);
the auth references live under [docs/auth/](../auth/passkeys.md) and
[docs/authz/rbac.md](../authz/rbac.md). Keep all of those aligned with the implementation
and with this file.

## Authentication

### User authentication (passkeys)

- Default user auth is passkeys (WebAuthn) via `webauthn`.
- Password auth is an optional extra (`h4ckath0n[password]`, Argon2) and stays **off by
  default**.

### Device authentication (client-signed ES256 JWT)

Each browser device holds a long-lived device identity key:

- The private key is generated via WebCrypto as non-extractable and stored in IndexedDB.
- The public key is exported as JWK and registered with the backend.
- Device IDs use the `d...` prefix, stored server side bound to a user (`u...`).

For API calls the web client mints short-lived ES256 JWTs signed by the device private key:

- The JWT header `kid` is the device id (`d...`).
- The payload carries only identity and time claims (`sub`, `iat`, `exp`, optional `aud`).
- The JWT contains **no privilege claims**. Authorization is computed server side from the
  database.

Server verification flow:

1. Extract `Authorization: Bearer <jwt>`.
2. Read `kid` from the JWT header; load the device public key from the DB.
3. Verify the ES256 signature and the time claims.
4. Confirm the device is not revoked.
5. Load the user bound to the device.
6. Enforce authorization from DB state, never from JWT claims.

## Authorization

- Built-in roles are `user` and `admin`, stored server side.
- Scopes are stored as a comma-separated string on the user record.
- Enforce access with `require_user()`, `require_admin()`, and `require_scopes([...])` in
  `src/h4ckath0n/auth/authz.py`. These helpers must never trust JWT privilege claims.

## Identity scheme

- User IDs: 32-char base32 from 20 random bytes, prefixed `u`. Never use email as a user ID.
- Internal credential key IDs: same scheme, prefix `k`.
- Device IDs: same scheme, prefix `d`.
- Password reset tokens: UUID hex (not base32).
- Generators and predicates live in `src/h4ckath0n/auth/passkeys/ids.py`:
  `new_user_id()`, `new_key_id()`, `new_device_id()`, `new_token_id()`, `is_user_id()`,
  `is_key_id()`, `is_device_id()`.
- The browser WebAuthn credential id is stored separately, never as the internal key ID.

## Last-passkey invariant

- Users may register multiple passkeys.
- A user's **last active passkey cannot be revoked** (`LAST_PASSKEY` error).
- The check is transactional via `SELECT ... FOR UPDATE` on Postgres.
- Revoked passkeys have `revoked_at` set and cannot be un-revoked.

## WebAuthn challenges

- Challenge state is stored server side (`webauthn_challenges` table).
- Default TTL is 300 seconds (`H4CKATH0N_WEBAUTHN_TTL_SECONDS`).
- Challenges are single-use, consumed on a successful finish.
- Expired challenges are cleaned up via `cleanup_expired_challenges()`.

## Secrecy and hardening defaults

- Never log secrets, tokens, Authorization headers, or WebAuthn payloads.
- Tokens are short-lived and minted client side; never persist them in localStorage or
  cookies.
- Do not document or reintroduce server-minted access plus refresh token flows unless that
  design is deliberately reinstated in [docs/security/frontend.md](../security/frontend.md).
- WebAuthn origin and RP ID are strict in production; development defaults to localhost
  with warnings.
