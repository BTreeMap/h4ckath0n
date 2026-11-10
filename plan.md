1. **Optimize `_resolve_user` in `src/h4ckath0n/cli/_common.py`**
   - Replace `session.execute(select(User).where(User.email == email)).scalars().first()` with `session.scalar(select(User).where(User.email == email))` to avoid the overhead of the `Result` object.

2. **Optimize `register_user` in `src/h4ckath0n/auth/service.py`**
   - Replace `await db.execute(select(User).filter(User.email == email))` followed by `.scalars().first()` with `await db.scalar(select(User.id).filter(User.email == email))` to avoid ORM hydration for an existence check.

3. **Optimize `authenticate_user` in `src/h4ckath0n/auth/service.py`**
   - Replace `await db.execute(select(User).filter(User.email == email))` followed by `.scalars().first()` with `await db.scalar(select(User).filter(User.email == email))` to avoid the overhead of the `Result` object.

4. **Optimize `confirm_password_reset` in `src/h4ckath0n/auth/service.py`**
   - Replace `await db.execute(select(PasswordResetToken).filter(...))` followed by `.scalars().first()` with `await db.scalar(select(PasswordResetToken).filter(...))` to avoid the overhead of the `Result` object.

5. **Optimize `finish_authentication` in `src/h4ckath0n/auth/passkeys/service.py`**
   - Replace `await db.execute(select(WebAuthnCredential).filter(...))` followed by `.scalars().first()` with `await db.scalar(select(WebAuthnCredential).filter(...))` to avoid the overhead of the `Result` object.

6. **Add Journal Entry**
   - Add a critical learning journal entry to `.jules/bolt.md` detailing the performance optimization of using `db.scalar(...)` instead of `db.execute(...).scalars().first()`.

7. **Run pre-commit steps**
   - Complete pre-commit steps to ensure proper testing, verification, review, and reflection are done.

8. **Submit PR**
   - Submit the PR titled '⚡ Bolt: [performance improvement]' detailing the use of `db.scalar` instead of `db.execute(...).scalars().first()` for single record fetches.
