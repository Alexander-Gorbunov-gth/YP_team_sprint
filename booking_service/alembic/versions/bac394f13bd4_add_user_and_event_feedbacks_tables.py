"""add user and event feedbacks tables

Revision ID: bac394f13bd4
Revises: fdb3b77b468d
Create Date: 2025-08-07 01:43:11.605974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bac394f13bd4'
down_revision: Union[str, Sequence[str], None] = 'fdb3b77b468d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Check if enum type already exists
    conn = op.get_bind()
    exists = conn.execute(
        sa.text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'review_type')")
    ).scalar()

    if not exists:
        op.execute("CREATE TYPE review_type AS ENUM ('POSITIVE', 'NEGATIVE')")

    review_type_enum = postgresql.ENUM('POSITIVE', 'NEGATIVE', name='review_type', create_type=False)

    op.create_table('user_feedbacks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('owner_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('review', review_type_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('event_feedbacks',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('event_id', sa.UUID(), nullable=False),
        sa.Column('review', review_type_enum, nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('feedbacks')

def downgrade() -> None:
    """Downgrade schema."""
    review_type_enum = postgresql.ENUM('POSITIVE', 'NEGATIVE', name='review_type', create_type=False)

    op.create_table('feedbacks',
        sa.Column('id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('user_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('event_id', sa.UUID(), autoincrement=False, nullable=False),
        sa.Column('review', review_type_enum, autoincrement=False, nullable=False),
        sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], name=op.f('feedbacks_event_id_fkey'), ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id', name=op.f('feedbacks_pkey'))
    )
    op.drop_table('event_feedbacks')
    op.drop_table('user_feedbacks')
