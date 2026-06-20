"""Argument parser construction for the operator CLI."""

from __future__ import annotations

import argparse

from h4ckath0n.cli._common import _add_user_selector


def build_parser() -> argparse.ArgumentParser:
    # Common flags shared by all leaf subcommands
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--db", default=None, help="Database URL override")
    common.add_argument(
        "--format", choices=["json", "jsonl"], default="json", help="Output format"
    )
    common.add_argument("--pretty", action="store_true", default=False, help="Pretty-print output")

    parser = argparse.ArgumentParser(
        prog="h4ckath0n",
        description="h4ckath0n operator CLI",
    )
    subparsers = parser.add_subparsers(dest="command")

    # ---- db ----
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_sub = db_parser.add_subparsers(dest="db_command")

    # db ping
    db_sub.add_parser("ping", parents=[common], help="Check database connectivity")

    # db migrate
    db_migrate = db_sub.add_parser("migrate", help="Run Alembic migrations")
    migrate_sub = db_migrate.add_subparsers(dest="migrate_command")

    # db migrate upgrade
    mig_upgrade = migrate_sub.add_parser("upgrade", parents=[common], help="Upgrade database")
    mig_upgrade.add_argument("--to", default="head", help="Target revision (default: head)")
    mig_upgrade.add_argument("--yes", action="store_true", help="Confirm mutation")

    # db migrate downgrade
    mig_downgrade = migrate_sub.add_parser(
        "downgrade", parents=[common], help="Downgrade database"
    )
    mig_downgrade.add_argument("--to", required=True, help="Target revision")
    mig_downgrade.add_argument("--yes", action="store_true", help="Confirm mutation")

    # db migrate current
    migrate_sub.add_parser("current", parents=[common], help="Show current revision")

    # db migrate heads
    migrate_sub.add_parser("heads", parents=[common], help="Show head revisions")

    # ---- users ----
    users_parser = subparsers.add_parser("users", help="User management")
    users_sub = users_parser.add_subparsers(dest="users_command")

    # users list
    users_list = users_sub.add_parser("list", parents=[common], help="List users")
    users_list.add_argument("--limit", type=int, default=50, help="Limit results")
    users_list.add_argument("--offset", type=int, default=0, help="Offset results")
    users_list.add_argument(
        "--include-disabled", action="store_true", help="Include disabled users"
    )

    # users show
    users_show = users_sub.add_parser("show", parents=[common], help="Show user details")
    _add_user_selector(users_show)

    # users set-role
    users_set_role = users_sub.add_parser("set-role", parents=[common], help="Set user role")
    _add_user_selector(users_set_role)
    users_set_role.add_argument(
        "--role", required=True, choices=["user", "admin"], help="Role to set"
    )
    users_set_role.add_argument("--yes", action="store_true", help="Confirm mutation")

    # users disable
    users_disable = users_sub.add_parser("disable", parents=[common], help="Disable user")
    _add_user_selector(users_disable)
    users_disable.add_argument("--yes", action="store_true", help="Confirm mutation")

    # users enable
    users_enable = users_sub.add_parser("enable", parents=[common], help="Enable user")
    _add_user_selector(users_enable)
    users_enable.add_argument("--yes", action="store_true", help="Confirm mutation")

    # users scopes
    users_scopes = users_sub.add_parser("scopes", help="Manage user scopes")
    scopes_sub = users_scopes.add_subparsers(dest="scopes_command")

    # users scopes add
    scopes_add = scopes_sub.add_parser("add", parents=[common], help="Add scopes")
    _add_user_selector(scopes_add)
    scopes_add.add_argument("--scope", action="append", required=True, help="Scope to add")
    scopes_add.add_argument("--yes", action="store_true", help="Confirm mutation")

    # users scopes remove
    scopes_remove = scopes_sub.add_parser("remove", parents=[common], help="Remove scopes")
    _add_user_selector(scopes_remove)
    scopes_remove.add_argument("--scope", action="append", required=True, help="Scope to remove")
    scopes_remove.add_argument("--yes", action="store_true", help="Confirm mutation")

    # users scopes set
    scopes_set = scopes_sub.add_parser("set", parents=[common], help="Set scopes (replace all)")
    _add_user_selector(scopes_set)
    scopes_set.add_argument("--scopes", required=True, help="Comma-separated scopes")
    scopes_set.add_argument("--yes", action="store_true", help="Confirm mutation")

    # ---- devices ----
    devices_parser = subparsers.add_parser("devices", help="Device management")
    devices_sub = devices_parser.add_subparsers(dest="devices_command")

    # devices list
    devices_list = devices_sub.add_parser("list", parents=[common], help="List devices for a user")
    _add_user_selector(devices_list)
    devices_list.add_argument(
        "--include-revoked", action="store_true", help="Include revoked devices"
    )

    # devices revoke
    devices_revoke = devices_sub.add_parser("revoke", parents=[common], help="Revoke a device")
    devices_revoke.add_argument("--device-id", required=True, help="Device ID (d...)")
    devices_revoke.add_argument("--yes", action="store_true", help="Confirm mutation")

    # ---- passkeys ----
    passkeys_parser = subparsers.add_parser("passkeys", help="Passkey management")
    passkeys_sub = passkeys_parser.add_subparsers(dest="passkeys_command")

    # passkeys list
    passkeys_list = passkeys_sub.add_parser(
        "list", parents=[common], help="List passkeys for a user"
    )
    _add_user_selector(passkeys_list)
    passkeys_list.add_argument(
        "--include-revoked", action="store_true", help="Include revoked passkeys"
    )

    # passkeys revoke
    passkeys_revoke = passkeys_sub.add_parser("revoke", parents=[common], help="Revoke a passkey")
    passkeys_revoke.add_argument("--key-id", required=True, help="Passkey ID (k...)")
    passkeys_revoke.add_argument("--yes", action="store_true", help="Confirm mutation")

    # ---- jobs ----
    jobs_parser = subparsers.add_parser("jobs", help="Background job operations")
    jobs_sub = jobs_parser.add_subparsers(dest="jobs_command")

    # jobs worker
    jobs_worker = jobs_sub.add_parser(
        "worker", parents=[common], help="Run a background job worker"
    )
    jobs_worker.add_argument("--queue", default="default", help="Queue name (default: default)")
    jobs_worker.add_argument(
        "--poll-interval",
        type=float,
        default=2,
        help="Poll interval in seconds (default: 2)",
    )

    # ---- seed ----
    seed_parser = subparsers.add_parser("seed", help="Seed data operations")
    seed_sub = seed_parser.add_subparsers(dest="seed_command")

    # seed demo
    seed_demo = seed_sub.add_parser("demo", parents=[common], help="Seed demo data")
    seed_demo.add_argument("--yes", action="store_true", help="Confirm mutation")

    return parser
