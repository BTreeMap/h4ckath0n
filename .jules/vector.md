# Vector Journal: Critical Learnings

## 2026-03-12 - Centralized functional scope parsing

**Learning:** The codebase had duplicated and fragmented scope string normalization pipelines (e.g. `[s for s in scopes.split(',') if s.strip()]`, `filter(None, map(str.strip...))`) scattered across `cli.py`, `dependencies.py`, and `session_router.py`. In addition to being verbose and repetitive, it was prone to edge cases where extra spaces could cause subtle errors or incorrect tokenization.
**Action:** Created `src/h4ckath0n/auth/scopes.py` providing pure FP helpers (`parse_scopes`, `format_scopes`, `normalize_scopes_string`). Replaced the ad-hoc mutation/comprehension logic across the codebase with these deterministic utilities. This effectively centralizes a shared data-shaping pipeline and leverages `dict.fromkeys()` for stable deduplication.
