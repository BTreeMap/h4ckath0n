1. *Create `src/h4ckath0n/auth/scopes.py`*
   Write the `src/h4ckath0n/auth/scopes.py` file with the exact content below using `write_file`.
   ```python
   """Utilities for parsing and formatting comma-separated scopes."""

   from __future__ import annotations

   from collections.abc import Iterable


   def parse_scopes(raw: str | None) -> list[str]:
       """Parse a comma-separated string into a deduplicated list of scopes, preserving order."""
       if not raw:
           return []
       return list(dict.fromkeys(filter(None, map(str.strip, raw.split(",")))))


   def format_scopes(scopes: Iterable[str]) -> str:
       """Format an iterable of scopes into a deduplicated comma-separated string."""
       return ",".join(dict.fromkeys(filter(None, map(str.strip, scopes))))
   ```

2. *Verify `src/h4ckath0n/auth/scopes.py`*
   Verify the creation of `src/h4ckath0n/auth/scopes.py` by reading it.

3. *Refactor `src/h4ckath0n/auth/dependencies.py`*
   Use `replace_with_git_merge_diff` with the following block:
   ```
   <<<<<<< SEARCH
   from h4ckath0n.auth.models import User
   from h4ckath0n.realtime.auth import AUD_HTTP, AuthContext, AuthError, verify_device_jwt
   =======
   from h4ckath0n.auth.models import User
   from h4ckath0n.auth.scopes import parse_scopes
   from h4ckath0n.realtime.auth import AUD_HTTP, AuthContext, AuthError, verify_device_jwt
   >>>>>>> REPLACE
   <<<<<<< SEARCH
       async def _scoped(user: User = Depends(_get_current_user)) -> User:
           user_scopes = filter(None, map(str.strip, user.scopes.split(",")))
           if missing := needed.difference(user_scopes):
   =======
       async def _scoped(user: User = Depends(_get_current_user)) -> User:
           user_scopes = parse_scopes(user.scopes)
           if missing := needed.difference(user_scopes):
   >>>>>>> REPLACE
   ```

4. *Verify `src/h4ckath0n/auth/dependencies.py`*
   Verify the changes in `src/h4ckath0n/auth/dependencies.py` by reading it.

5. *Refactor `src/h4ckath0n/auth/session_router.py`*
   Use `replace_with_git_merge_diff` with the following block:
   ```
   <<<<<<< SEARCH
   from h4ckath0n.auth.dependencies import get_auth_context, require_user
   from h4ckath0n.auth.models import User
   from h4ckath0n.auth.schemas import SessionResponse
   =======
   from h4ckath0n.auth.dependencies import get_auth_context, require_user
   from h4ckath0n.auth.models import User
   from h4ckath0n.auth.schemas import SessionResponse
   from h4ckath0n.auth.scopes import parse_scopes
   >>>>>>> REPLACE
   <<<<<<< SEARCH
   async def get_session(
       user: User = require_user(),
       ctx: AuthContext = Depends(get_auth_context),
   ) -> SessionResponse:
       scopes = [s for s in user.scopes.split(",") if s]
       return SessionResponse(
   =======
   async def get_session(
       user: User = require_user(),
       ctx: AuthContext = Depends(get_auth_context),
   ) -> SessionResponse:
       scopes = parse_scopes(user.scopes)
       return SessionResponse(
   >>>>>>> REPLACE
   ```

6. *Verify `src/h4ckath0n/auth/session_router.py`*
   Verify the changes in `src/h4ckath0n/auth/session_router.py` by reading it.

7. *Refactor `src/h4ckath0n/cli.py`*
   Use `replace_with_git_merge_diff` with the following blocks:
   ```
   <<<<<<< SEARCH
   from h4ckath0n.auth.models import Device, User, WebAuthnCredential
   from h4ckath0n.auth.passkeys.ids import is_device_id, is_key_id
   from h4ckath0n.auth.passkeys.service import revoke_passkey
   =======
   from h4ckath0n.auth.models import Device, User, WebAuthnCredential
   from h4ckath0n.auth.passkeys.ids import is_device_id, is_key_id
   from h4ckath0n.auth.passkeys.service import revoke_passkey
   from h4ckath0n.auth.scopes import format_scopes, parse_scopes
   >>>>>>> REPLACE
   <<<<<<< SEARCH
   def _normalize_scopes(raw: str) -> str:
       """Normalize a comma-separated scopes string."""
       parts = filter(None, map(str.strip, raw.split(",")))
       # de-duplicate preserving order
       return ",".join(dict.fromkeys(parts))


   def _cmd_db_ping(args: argparse.Namespace) -> int:
   =======
   def _cmd_db_ping(args: argparse.Namespace) -> int:
   >>>>>>> REPLACE
   <<<<<<< SEARCH
               existing = set(s for s in user.scopes.split(",") if s.strip())
               for scope in args.scope:
                   existing.add(scope.strip())
               user.scopes = _normalize_scopes(",".join(existing))

               await db.commit()
   =======
               existing = parse_scopes(user.scopes)
               user.scopes = format_scopes(existing + args.scope)

               await db.commit()
   >>>>>>> REPLACE
   <<<<<<< SEARCH
               existing = [s for s in user.scopes.split(",") if s.strip()]
               to_remove = {s.strip() for s in args.scope}
               remaining = [s for s in existing if s not in to_remove]
               user.scopes = _normalize_scopes(",".join(remaining))

               await db.commit()
   =======
               existing = parse_scopes(user.scopes)
               to_remove = {s.strip() for s in args.scope}
               remaining = [s for s in existing if s not in to_remove]
               user.scopes = format_scopes(remaining)

               await db.commit()
   >>>>>>> REPLACE
   <<<<<<< SEARCH
           async with _session(args) as db:
               user = await _get_user_or_err(db, args)
               if not user:
                   _err("user not found")
                   return EXIT_NOT_FOUND

               user.scopes = _normalize_scopes(args.scopes)

               await db.commit()
   =======
           async with _session(args) as db:
               user = await _get_user_or_err(db, args)
               if not user:
                   _err("user not found")
                   return EXIT_NOT_FOUND

               user.scopes = format_scopes(args.scopes.split(","))

               await db.commit()
   >>>>>>> REPLACE
   ```

8. *Verify `src/h4ckath0n/cli.py`*
   Verify the changes in `src/h4ckath0n/cli.py` by reading it.

9. *Create `tests/test_auth_scopes.py`*
   Write the test file exactly as follows using `write_file`.
   ```python
   """Tests for h4ckath0n.auth.scopes utilities."""

   from h4ckath0n.auth.scopes import format_scopes, parse_scopes


   def test_parse_scopes() -> None:
       assert parse_scopes(None) == []
       assert parse_scopes("") == []
       assert parse_scopes("foo, bar, baz") == ["foo", "bar", "baz"]
       assert parse_scopes("  foo  ,  bar  ") == ["foo", "bar"]
       assert parse_scopes("foo,foo,bar") == ["foo", "bar"]
       assert parse_scopes("foo,,bar,") == ["foo", "bar"]


   def test_format_scopes() -> None:
       assert format_scopes([]) == ""
       assert format_scopes(["foo", "bar"]) == "foo,bar"
       assert format_scopes(["foo", "bar", "foo"]) == "foo,bar"
       assert format_scopes([" foo ", "bar "]) == "foo,bar"
       assert format_scopes(["foo", "", "bar"]) == "foo,bar"

   ```

10. *Verify `tests/test_auth_scopes.py`*
   Verify the creation of `tests/test_auth_scopes.py` by reading it.

11. *Update Vector journal*
   Run the following exact bash command to update `.jules/vector.md`:
   ```bash
   mkdir -p .jules && cat << 'EOF' >> .jules/vector.md
   ## 2025-04-12 - Centralize parsing and formatting logic for database text columns
   **Learning:** When converting sequences like comma-separated scopes to and from database text columns, repeating ad-hoc string manipulation (like `.split(",")`, `.strip()`, or `filter(None)`) across modules causes minor subtle divergence and bug risks.
   **Action:** Extract this logic into small, pure helper functions (e.g. `parse_scopes`, `format_scopes`) with clear boundaries. Deduplication that preserves order should be favored using `dict.fromkeys()` over `set()`.
   EOF
   ```

12. *Verify `.jules/vector.md`*
    Verify the changes by running `cat .jules/vector.md`

13. *Final Verification*
    Run `uv run --locked ruff check --fix . && uv run --locked ruff format . && uv run --locked pytest -v` using `run_in_bash_session` to verify tests and linting.

14. *Pre-commit steps*
    Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

15. *Submit the change*
    Submit the PR with branch name `vector/auth-scopes` and explicitly list all required Vector persona fields in the description ('💡 What', '🎯 Why', '🧠 Design', 'λ FP Angle', '✅ Verification', '🧪 Edge cases', '⚠️ Risk').
