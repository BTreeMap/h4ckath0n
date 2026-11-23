## 2024-05-18 - Centralize FastAPI dependencies for DB sessions
**Learning:** The codebase repeatedly implemented an ad-hoc local `_db_dep` FastAPI dependency inside almost every router, and an imperative session lifecycle manager `_get_async_db_from_request` in `auth/dependencies.py` which led to repeated try-finally blocks for closing sessions.
**Action:** Use a single, central `get_async_session` in `db.session` to yield an AsyncSession context block, eliminating duplicated dependency code and enforcing declarative session lifecycle management across routers and dependencies.
