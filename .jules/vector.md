## 2024-05-26 - Import `Iterable` from `collections.abc`
**Learning:** The project uses Ruff which enforces UP035. Importing `Iterable` from `typing` will fail the CI linting gate.
**Action:** Always import abstract base classes like `Iterable`, `Sequence`, or `Mapping` from `collections.abc` instead of `typing`.
