"""Demo data seeding subcommand."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from datetime import UTC, datetime

from h4ckath0n.cli._common import EXIT_BAD_ARGS, EXIT_OK


def _cmd_seed_demo(args: argparse.Namespace) -> int:
    """Seed demo data (admin user, regular user, and sample jobs).

    Creates two users (``admin@demo.local`` with role admin and
    ``user@demo.local`` with role user), optionally sets passwords when
    password auth is enabled, and inserts sample ``demo.echo`` jobs.
    Requires ``--yes`` to confirm the mutation.
    """
    if not getattr(args, "yes", False):
        print("Use --yes to confirm seeding demo data.", file=sys.stderr)
        return EXIT_BAD_ARGS

    from h4ckath0n.config import Settings

    settings = Settings()

    if not settings.demo_mode:
        print(
            "Warning: demo_mode is not enabled. Set H4CKATH0N_DEMO_MODE=true.",
            file=sys.stderr,
        )

    from sqlalchemy.ext.asyncio import async_sessionmaker

    import h4ckath0n.auth.models  # noqa: F401
    import h4ckath0n.jobs.models  # noqa: F401
    import h4ckath0n.uploads.models  # noqa: F401
    from h4ckath0n.auth.models import User
    from h4ckath0n.db.base import Base
    from h4ckath0n.db.engine import create_async_engine_from_settings
    from h4ckath0n.jobs.models import Job

    async def _seed() -> None:
        engine = create_async_engine_from_settings(settings)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        session_factory = async_sessionmaker(engine, expire_on_commit=False)

        async with session_factory() as db:
            admin = User(
                role="admin",
                scopes="admin,demo",
                display_name="Demo Admin",
                email="admin@demo.local",
            )
            regular = User(
                role="user",
                scopes="demo",
                display_name="Demo User",
                email="user@demo.local",
            )

            # Set passwords if password auth enabled
            if settings.password_auth_enabled:
                try:
                    from h4ckath0n.auth.passwords import hash_password

                    admin.password_hash = hash_password("admin123")
                    regular.password_hash = hash_password("user123")
                except ImportError:
                    print("Password extra not installed, skipping password setup.")

            db.add_all([admin, regular])
            await db.flush()

            now = datetime.now(UTC)
            jobs = [
                Job(
                    kind="demo.echo",
                    status="succeeded",
                    progress=100,
                    payload_json=json.dumps({"msg": "Hello from demo"}),
                    result_json=json.dumps({"echo": {"msg": "Hello from demo"}}),
                    created_by_user_id=admin.id,
                    started_at=now,
                    finished_at=now,
                ),
                Job(
                    kind="demo.echo",
                    status="queued",
                    payload_json=json.dumps({"msg": "Pending demo job"}),
                    created_by_user_id=regular.id,
                ),
            ]
            db.add_all(jobs)
            await db.commit()

            print(f"Created demo admin: {admin.id} (admin@demo.local)")
            print(f"Created demo user: {regular.id} (user@demo.local)")
            if settings.password_auth_enabled:
                print("Demo admin password: admin123")
                print("Demo user password: user123")
            print(f"Created {len(jobs)} demo jobs")

        await engine.dispose()

    asyncio.run(_seed())
    return EXIT_OK
