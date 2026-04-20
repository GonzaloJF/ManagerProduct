"""add email to user

Revision ID: 3c87c93c5851
Revises: 1bccacc37dd0
Create Date: 2026-04-19 16:40:50.957536

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c87c93c5851'
down_revision: Union[str, Sequence[str], None] = '1bccacc37dd0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('email', sa.String(), nullable=False))
    op.create_unique_constraint('uq_users_email', 'users', ['email'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('uq_users_email', 'users', type_='unique')
    op.drop_column('users', 'email')
