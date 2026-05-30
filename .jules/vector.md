## 2024-05-30 - Refactored passkey ID generators
**Learning:** The ID generators in `src/h4ckath0n/auth/passkeys/ids.py` contained duplicated prefix generation and validation logic.
**Action:** Extracted pure helper functions `_generate_prefixed_id` and `_is_valid_id` to centralize this logic, adhering to the codebase's preference for functional-programming style and pure helpers. This makes adding new prefixed ID types much simpler.
