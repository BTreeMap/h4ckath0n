## 2024-07-06 - Centralize CLI scope parsing
**Learning:** The CLI tools for user scopes (`users scopes add` and `users scopes remove`) used ad-hoc string splitting that bypassed the centralized `parse_scopes` logic, leading to duplicate and unparsed scopes when users provided comma-separated lists inline (e.g. `--scope="admin, demo"`).
**Action:** Always route external input strings through the primary domain normalization functions (`parse_scopes`) before manipulating collections, ensuring a single source of truth for semantic boundaries and eliminating manual looping over unparsed inputs.
