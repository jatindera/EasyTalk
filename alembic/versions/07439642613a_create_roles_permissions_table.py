"""Create roles_permissions table

Revision ID: 07439642613a
Revises: 92cd699c54c0
Create Date: 2024-09-11 10:35:31.979965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '07439642613a'
down_revision: Union[str, None] = '92cd699c54c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'roles_permissions' table
    op.create_table(
        'roles_permissions',
        sa.Column('role_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('role_name', sa.String(50), nullable=False),  # e.g., 'admin', 'user', etc.
        sa.Column('permission', sa.String(255), nullable=True),  # e.g., 'read', 'write', 'admin access'
        sa.Column('created_at', sa.DateTime, server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now(), onupdate=sa.func.now())
    )

    # Create an index on the role_name column
    op.create_index('idx_roles_permissions_role_name', 'roles_permissions', ['role_name'], unique=False)


def downgrade():
    # Drop the index first
    op.drop_index('idx_roles_permissions_role_name', table_name='roles_permissions')

    # Drop the 'roles_permissions' table
    op.drop_table('roles_permissions')
