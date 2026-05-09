## 2024-05-19 - Centralize domain logic in schemas.py
**Learning:** To avoid circular dependencies between SQLAlchemy models, service layers, and routers in the `h4ckath0n` architecture, domain-specific pure functional helpers (like scope string normalization/parsing) should be defined in the local domain's `schemas.py` file rather than utility files or models directly.
**Action:** Always place shared pure functional domain helpers in `schemas.py` and import them from there across routers, dependencies, and CLI commands.

## 2024-05-19 - Do not eagerly materialize iterables into sets
**Learning:** When performing set operations like `needed.difference(iterable)`, CPython's `set.difference()` natively consumes arbitrary iterables efficiently. Wrapping the argument in `set(...)` beforehand introduces unnecessary memory overhead and function calls.
**Action:** Pass generators or list comprehensions directly to set methods like `difference()` rather than wrapping them in `set()`.
