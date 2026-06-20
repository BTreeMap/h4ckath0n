# 0001 — Disabled users are not enforced at authentication

- Status: Known issue (documented; behavior intentionally unchanged)
- Scope: Security / authentication

## Context

The `users` table carries a nullable `disabled_at` timestamp
([src/h4ckath0n/auth/models.py](../../src/h4ckath0n/auth/models.py)). Operators
can set or clear it through the CLI:

- `h4ckath0n users disable --user-id … --yes` sets `disabled_at` to now.
- `h4ckath0n users enable --user-id … --yes` clears it.
- `h4ckath0n users list` hides disabled users unless `--include-disabled` is
  passed.

## Problem

`disabled_at` is **only** consulted by the CLI `users list` filter. It is **not**
checked anywhere in the request authentication path:

- `src/h4ckath0n/auth/dependencies.py` (`require_user` / `require_scopes`)
- `src/h4ckath0n/auth/service.py`
- `src/h4ckath0n/auth/jwt.py` (token verification)
- `src/h4ckath0n/realtime/auth.py`

As a result, a user who has been "disabled" can still authenticate and call the
API for as long as their existing credentials/JWT remain valid. Disabling a user
today is an administrative bookkeeping flag, not an access revocation.

## Decision

Document the gap without changing behavior in this change set. Enforcing
disablement is a behavioral/security change that affects the public auth
contract (previously-valid sessions would begin to fail) and therefore belongs
in a dedicated, separately reviewed change rather than the internal
type-safety/maintainability refactor that surfaced it.

## Consequences / future work

When enforcement is implemented, the check should live at a single choke point
so it applies uniformly to passkeys, device JWTs, password sessions, and
realtime connections. Candidate approach:

- Add a `disabled_at is None` assertion in `require_user` (and the realtime
  equivalent) so every authenticated entry point rejects disabled accounts.
- Decide and document the JWT story: short-lived tokens will age out naturally,
  but immediate revocation requires either a deny-list or a per-request user
  lookup.
- Add tests covering: disabled user with a valid JWT is rejected; re-enabled
  user regains access.
