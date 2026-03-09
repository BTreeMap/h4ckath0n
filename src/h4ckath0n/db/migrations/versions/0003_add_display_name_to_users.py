"""add display_name to users

Revision ID: 0003
Revises: 0002
Create Date: 2026-03-09 00:00:00.000000
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Batch mode for SQLite compatibility (ALTER TABLE limitations).
    with op.batch_alter_table("h4ckath0n_users") as batch_op:
        batch_op.add_column(sa.Column("display_name", sa.String(64), nullable=True))


def downgrade() -> None:
    with op.batch_alter_table("h4ckath0n_users") as batch_op:
        batch_op.drop_column("display_name")
