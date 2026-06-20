"""Database subcommands for the operator CLI."""

from __future__ import annotations

import argparse

from alembic import command as alembic_command
from alembic.config import Config
from sqlalchemy import text

from h4ckath0n.cli._common import (
    EXIT_BAD_ARGS,
    EXIT_MIGRATIONS_MISSING,
    EXIT_OK,
    _err,
    _get_db_url,
    _make_sync_engine,
    _normalize_db_url_for_sync,
    _output,
    _require_yes,
)
from h4ckath0n.db.migrations.runtime import (
    PackagedMigrationsError,
    get_schema_status,
    packaged_migrations_dir,
    run_upgrade_to_head,
)

__all__ = [
    "alembic_command",
    "_cmd_db_ping",
    "_cmd_db_migrate_upgrade",
    "_cmd_db_migrate_downgrade",
    "_cmd_db_migrate_current",
    "_cmd_db_migrate_heads",
]


def _alembic_config(url: str, migrations_path: object) -> Config:
    cfg = Config()
    cfg.set_main_option("script_location", str(migrations_path))
    cfg.set_main_option("sqlalchemy.url", url)
    return cfg


def _cmd_db_ping(args: argparse.Namespace) -> int:
    url = _normalize_db_url_for_sync(_get_db_url(args))
    engine = _make_sync_engine(url)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        try:
            status = get_schema_status(url)
            _output(
                {
                    "ok": True,
                    "schema_state": status.state,
                    "current_revisions": list(status.current_revisions),
                    "head_revisions": list(status.head_revisions),
                    "warning": status.warning,
                },
                fmt=args.format,
                pretty=args.pretty,
            )
        except PackagedMigrationsError:
            _err("packaged migrations not found; installation may be broken")
            return EXIT_MIGRATIONS_MISSING
        return EXIT_OK
    finally:
        engine.dispose()


def _cmd_db_migrate_upgrade(args: argparse.Namespace) -> int:
    if not _require_yes(args):
        return EXIT_BAD_ARGS

    url = _normalize_db_url_for_sync(_get_db_url(args))
    revision = getattr(args, "to", "head")
    try:
        if revision == "head":
            # Using our high-level helper which handles fresh install nicely
            run_upgrade_to_head(url)
        else:
            with packaged_migrations_dir() as migrations_path:
                alembic_command.upgrade(_alembic_config(url, migrations_path), revision)
        _output({"ok": True, "revision": revision}, fmt=args.format, pretty=args.pretty)
        return EXIT_OK
    except PackagedMigrationsError:
        _err("packaged migrations not found; installation may be broken")
        return EXIT_MIGRATIONS_MISSING


def _cmd_db_migrate_downgrade(args: argparse.Namespace) -> int:
    if not _require_yes(args):
        return EXIT_BAD_ARGS

    url = _normalize_db_url_for_sync(_get_db_url(args))

    revision = getattr(args, "to", None)
    if not revision:
        _err("--to is required for downgrade")
        return EXIT_BAD_ARGS

    try:
        with packaged_migrations_dir() as migrations_path:
            alembic_command.downgrade(_alembic_config(url, migrations_path), revision)
        _output({"ok": True, "revision": revision}, fmt=args.format, pretty=args.pretty)
        return EXIT_OK
    except PackagedMigrationsError:
        _err("packaged migrations not found; installation may be broken")
        return EXIT_MIGRATIONS_MISSING


def _cmd_db_migrate_current(args: argparse.Namespace) -> int:
    url = _normalize_db_url_for_sync(_get_db_url(args))
    try:
        with packaged_migrations_dir() as migrations_path:
            alembic_command.current(_alembic_config(url, migrations_path))
        return EXIT_OK
    except PackagedMigrationsError:
        _err("packaged migrations not found; installation may be broken")
        return EXIT_MIGRATIONS_MISSING


def _cmd_db_migrate_heads(args: argparse.Namespace) -> int:
    url = _normalize_db_url_for_sync(_get_db_url(args))
    try:
        with packaged_migrations_dir() as migrations_path:
            alembic_command.heads(_alembic_config(url, migrations_path))
        return EXIT_OK
    except PackagedMigrationsError:
        _err("packaged migrations not found; installation may be broken")
        return EXIT_MIGRATIONS_MISSING
