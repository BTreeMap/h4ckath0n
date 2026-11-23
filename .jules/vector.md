## 2024-11-08 - TypeGuard delegation to bool helper
**Learning:** mypy handles delegating a `TypeGuard` function directly to a helper that returns a standard `bool` natively, without requiring `# type: ignore[return-value]`. Adding unnecessary ignores causes a `[unused-ignore]` error.
**Action:** Extract duplicated type guard logic into simple `bool`-returning helpers directly, without fighting mypy or adding redundant ignores.
