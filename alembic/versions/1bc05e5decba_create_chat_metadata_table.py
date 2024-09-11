"""Create chat_metadata table

Revision ID: 1bc05e5decba
Revises: 7761ac277c09
Create Date: 2024-09-11 11:21:29.914172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc05e5decba'
down_revision: Union[str, None] = '7761ac277c09'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'chat_metadata' table
    op.create_table(
        'chat_metadata',
        sa.Column('metadata_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('session_id', sa.Integer, sa.ForeignKey('chat_sessions.session_id', ondelete='CASCADE'), nullable=False),
        sa.Column('ai_model', sa.String(255), nullable=True),  # AI model used during the session
        sa.Column('total_duration', sa.Integer, nullable=True),  # Total duration of the session in minutes
        sa.Column('message_count', sa.Integer, nullable=True),  # Total number of messages exchanged in the session
        sa.Column('feedback', sa.String(255), nullable=True),  # Optional feedback from the user
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)
    )

    # Optionally, create an index on session_id for faster lookups by session
    op.create_index('idx_chat_metadata_session_id', 'chat_metadata', ['session_id'], unique=False)


def downgrade():
    # Drop the index first
    op.drop_index('idx_chat_metadata_session_id', table_name='chat_metadata')

    # Drop the 'chat_metadata' table
    op.drop_table('chat_metadata')
