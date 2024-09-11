"""Create chat_sessions table

Revision ID: 68848be4cb07
Revises: 8a3ea5aa2669
Create Date: 2024-09-11 10:54:23.074032

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68848be4cb07'
down_revision: Union[str, None] = '8a3ea5aa2669'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'chat_sessions' table
    op.create_table(
        'chat_sessions',
        sa.Column('session_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_name', sa.String(255), nullable=True),  # Optional name for the session
        sa.Column('session_status', sa.String(50), default='active'),  # Active or completed
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

    # Optionally, create an index on user_id for faster lookups by user
    op.create_index('idx_chat_sessions_user_id', 'chat_sessions', ['user_id'], unique=False)


def downgrade():
    # Drop the index first
    op.drop_index('idx_chat_sessions_user_id', table_name='chat_sessions')

    # Drop the 'chat_sessions' table
    op.drop_table('chat_sessions')
