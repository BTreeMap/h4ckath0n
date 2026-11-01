## 2025-02-28 - Centralizing ID Generation and Validation
**Learning:** The `h4ckath0n` codebase favors functional programming style thinking, including centralized normalization and pure helpers over duplicated local transformations. We must prefer explicit transformation pipelines and pure helpers even for seemingly small string operations (e.g. generating and validating IDs).
**Action:** Extract repeated string normalizations, prefix assignments, and length validations into shared pure helpers (e.g., `_new_id`, `_is_valid_id`) rather than repeating the slicing/logic inline.
