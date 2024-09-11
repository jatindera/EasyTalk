"""Create user_sessions table

Revision ID: 92cd699c54c0
Revises: 24ae44c43ccf
Create Date: 2024-09-11 09:46:20.996866

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '92cd699c54c0'
down_revision: Union[str, None] = '24ae44c43ccf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'auth.user_sessions' table
    op.create_table(
        'user_sessions',
        sa.Column('session_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('token', sa.String(500), nullable=False, unique=True),  # JWT or session token
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('user_agent', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('expires_at', sa.DateTime, nullable=True)
    )

    # Create an index on the token column for faster lookups
    op.create_index('idx_user_sessions_token', 'user_sessions', ['token'], unique=True)


def downgrade():
    # Drop the index first
    op.drop_index('idx_user_sessions_token', table_name='user_sessions')

    # Drop the 'auth.user_sessions' table
    op.drop_table('user_sessions')