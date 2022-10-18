"""create tags table

Revision ID: 1bd006d42d5d
Revises: fd3dc97009bb
Create Date: 2022-10-18 14:59:09.926966

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1bd006d42d5d'
down_revision = 'fd3dc97009bb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('name', sa.String, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('tags')