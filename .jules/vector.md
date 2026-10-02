## 2025-02-17 - Centralize scope mutations with pure functional helpers
**Learning:** In `h4ckath0n.auth.authz`, when adding or removing scopes, multiple places were re-implementing parsing, concatenating, set filtering, and serializing. Additionally, manual concatenations bypassing `parse_scopes` on collections may cause bugs.
**Action:** Use functional pure helpers like `add_scopes` and `remove_scopes` directly, rather than inline mutations across call sites.
