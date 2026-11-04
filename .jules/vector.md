## 2025-02-12 - Extracted scope addition and removal to pure helpers
**Learning:** Adding and removing scopes from strings was manually parsing, mutating with sets, and serializing in `src/h4ckath0n/cli/users.py`.
**Action:** Extract `add_scopes` and `remove_scopes` into `src/h4ckath0n/auth/authz.py` to keep the domain logic centralized, pure, and composable. Use these helpers across the codebase.
