"""Create chat_history table

Revision ID: 7761ac277c09
Revises: 68848be4cb07
Create Date: 2024-09-11 11:19:07.564007

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7761ac277c09'
down_revision: Union[str, None] = '68848be4cb07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'chat_history' table
    op.create_table(
        'chat_history',
        sa.Column('message_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.Integer, sa.ForeignKey('chat_sessions.session_id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='SET NULL'), nullable=True),
        sa.Column('message_text', sa.Text, nullable=False),
        sa.Column('sender', sa.String(50), nullable=False, default='user'),  # 'user' or 'ai'
        sa.Column('message_type', sa.String(50), nullable=False, default='text'),  # 'text', 'image', etc.
        sa.Column('timestamp', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

    # Optionally, create indexes for faster lookups
    op.create_index('idx_chat_history_session_id', 'chat_history', ['session_id'], unique=False)
    op.create_index('idx_chat_history_user_id', 'chat_history', ['user_id'], unique=False)


def downgrade():
    # Drop the indexes first
    op.drop_index('idx_chat_history_session_id', table_name='chat_history')
    op.drop_index('idx_chat_history_user_id', table_name='chat_history')

    # Drop the 'chat_history' table
    op.drop_table('chat_history')
