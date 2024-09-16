"""Create users table

Revision ID: 24ae44c43ccf
Revises: 
Create Date: 2024-09-11 09:44:23.704739

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24ae44c43ccf'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'auth.users' table
    # Reasons to Use Both user_id and email:
    # user_id (integer) is more efficient for database indexing and querying compared to an email address (which is a string). 
    # Users may change their email addresses over time.
    # Other thoughts: No user id / password: Only single sign on using Google, Microsoft etc.
    op.create_table(
        'users',
        sa.Column('user_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('first_name', sa.String(100), nullable=True),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('provider_name', sa.String(50), nullable=False),  # e.g., 'google', 'azure'
        sa.Column('provider_id', sa.String(255), nullable=False, unique=True),  # Unique ID from SSO provider
        sa.Column('role', sa.String(50), nullable=False, default='user'),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )


def downgrade():
    # Drop the 'auth.users' table
    op.drop_table('users')
