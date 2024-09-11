"""Create ai_models table

Revision ID: 72ba2e760cbd
Revises: 1bc05e5decba
Create Date: 2024-09-11 11:28:00.221087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '72ba2e760cbd'
down_revision: Union[str, None] = '1bc05e5decba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'ai_models' table
    op.create_table(
        'ai_models',
        sa.Column('model_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('model_name', sa.String(255), nullable=False),  # Name of the AI model (e.g., GPT-4, LLaMA)
        sa.Column('version', sa.String(50), nullable=False),  # Version of the AI model
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False)  # Timestamp for when the model entry was created
    )


def downgrade():
    # Drop the 'ai_models' table
    op.drop_table('ai_models')