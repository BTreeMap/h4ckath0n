## 2024-05-18 - SQLAlchemy ORM Execution Overhead
**Learning:** For non-PK lookups, aggregations (like `func.count()`), or existence checks in SQLAlchemy, using `await db.execute(select(...)).scalars().first()` or `await db.execute(select(...)).scalar()` incurs the overhead of creating a `Result` object and its iterator.
**Action:** Use `await db.scalar(select(...))` (or `select(Model.id)` for existence checks) directly to avoid the unnecessary `Result` object overhead and improve backend performance.
