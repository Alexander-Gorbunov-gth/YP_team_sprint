"""Add user roles relationship

Revision ID: 28e605a3deb0
Revises: 0cd01645a1a8
Create Date: 2025-03-14 17:29:13.928023

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28e605a3deb0'
down_revision: Union[str, None] = '0cd01645a1a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
