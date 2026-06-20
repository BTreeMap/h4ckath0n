"""Device management subcommands."""

from __future__ import annotations

import argparse
from datetime import UTC, datetime

from sqlalchemy import select

from h4ckath0n.auth.models import Device
from h4ckath0n.cli._common import (
    EXIT_BAD_ARGS,
    EXIT_NOT_FOUND,
    EXIT_OK,
    _device_dict,
    _err,
    _output,
    _require_yes,
    _sync_session,
    _user_or_exit,
)

__all__ = ["_cmd_devices_list", "_cmd_devices_revoke"]


def _cmd_devices_list(args: argparse.Namespace) -> int:
    with _sync_session(args) as session:
        user, err = _user_or_exit(session, args)
        if err is not None:
            return err
        assert user is not None

        stmt = select(Device).where(Device.user_id == user.id)
        if not getattr(args, "include_revoked", False):
            stmt = stmt.where(Device.revoked_at.is_(None))
        devices = session.execute(stmt).scalars().all()
        _output([_device_dict(d) for d in devices], fmt=args.format, pretty=args.pretty)
    return EXIT_OK


def _cmd_devices_revoke(args: argparse.Namespace) -> int:
    if not _require_yes(args):
        return EXIT_BAD_ARGS

    with _sync_session(args) as session:
        if (device := session.get(Device, args.device_id)) is None:
            _err("device not found")
            return EXIT_NOT_FOUND

        if device.revoked_at is None:
            device.revoked_at = datetime.now(UTC)
            session.commit()
            session.refresh(device)
        _output(_device_dict(device), fmt=args.format, pretty=args.pretty)
    return EXIT_OK
