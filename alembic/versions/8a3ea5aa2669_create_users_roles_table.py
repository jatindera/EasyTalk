"""Create users_roles table

Revision ID: 8a3ea5aa2669
Revises: 07439642613a
Create Date: 2024-09-11 10:48:15.336576

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8a3ea5aa2669'
down_revision: Union[str, None] = '07439642613a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create the 'users_roles' table
    op.create_table(
        'users_roles',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.user_id', ondelete='CASCADE'), primary_key=True),
        sa.Column('role_id', sa.Integer, sa.ForeignKey('roles_permissions.role_id', ondelete='CASCADE'), primary_key=True)
    )

    # Optionally, create an index for faster lookups
    op.create_index('idx_users_roles_user_id', 'users_roles', ['user_id'], unique=False)
    op.create_index('idx_users_roles_role_id', 'users_roles', ['role_id'], unique=False)

#Two indexes are created on the user_id and role_id columns to optimize performance when searching 
# for all roles assigned to a specific user or all users assigned to a specific role. 
# This ensures faster lookup times, particularly in many-to-many relationships, 
# where queries can involve multiple users and roles.
def downgrade():
    # Drop the indexes first
    op.drop_index('idx_users_roles_user_id', table_name='users_roles')
    op.drop_index('idx_users_roles_role_id', table_name='users_roles')

    # Drop the 'users_roles' table
    op.drop_table('users_roles')