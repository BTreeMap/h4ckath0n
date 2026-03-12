"""Add jobs and uploads tables.

Revision ID: 0004
Revises: 0003
Create Date: 2026-03-10 00:00:00.000000

Adds ``h4ckath0n_jobs`` and ``h4ckath0n_uploads`` tables for the
background-job queue and file-upload tracking features.
"""

import sqlalchemy as sa
from alembic import op

revision = "0004"
down_revision = "0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "h4ckath0n_jobs",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("kind", sa.String(100), nullable=False),
        sa.Column("queue", sa.String(50), nullable=False, server_default="default"),
        sa.Column("status", sa.String(20), nullable=False, server_default="queued"),
        sa.Column("payload_json", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("result_json", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("progress", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("attempts", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_attempts", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("created_by_user_id", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "h4ckath0n_uploads",
        sa.Column("id", sa.String(32), primary_key=True),
        sa.Column("owner_user_id", sa.String(32), nullable=False),
        sa.Column("original_filename", sa.String(512), nullable=False),
        sa.Column(
            "content_type",
            sa.String(255),
            nullable=False,
            server_default="application/octet-stream",
        ),
        sa.Column("byte_size", sa.BigInteger(), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("storage_key", sa.String(512), nullable=False),
        sa.Column("extraction_job_id", sa.String(32), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    with op.batch_alter_table("h4ckath0n_uploads") as batch_op:
        batch_op.create_index("ix_h4ckath0n_uploads_owner_user_id", ["owner_user_id"])


def downgrade() -> None:
    op.drop_table("h4ckath0n_uploads")
    op.drop_table("h4ckath0n_jobs")
