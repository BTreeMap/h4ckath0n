## 2024-11-03 - Centralize ID prefix validation
**Learning:** ID prefix validation (e.g., checking if a string starts with "u" and is 32 chars) is duplicated in `is_user_id`, `is_key_id`, `is_device_id` in `src/h4ckath0n/auth/passkeys/ids.py`. We can extract a pure helper `_is_valid_id(value: str, prefix: str) -> bool`.
**Action:** Extract a small pure helper `_is_valid_id` in `src/h4ckath0n/auth/passkeys/ids.py` to remove the duplicated logic.
