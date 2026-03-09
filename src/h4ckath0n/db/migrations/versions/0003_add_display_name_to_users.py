"""Add display_name column to users table.

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-09 00:00:00.000000

Adds a nullable VARCHAR(200) ``display_name`` column to ``h4ckath0n_users``
so that the human-facing name provided during registration is persisted.
"""

import sqlalchemy as sa
from alembic import op

revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("h4ckath0n_users") as batch_op:
        batch_op.add_column(sa.Column("display_name", sa.String(200), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("h4ckath0n_users") as batch_op:
        batch_op.drop_column("display_name")
