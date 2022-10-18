"""create interruptions table

Revision ID: fd3dc97009bb
Revises: 0809629b126c
Create Date: 2022-10-18 14:39:40.835027

"""
from datetime import datetime 

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fd3dc97009bb'
down_revision = '0809629b126c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'interruptions',
        sa.Column('interruptor_id', sa.Integer, sa.ForeignKey('tasks.id'), primary_key=True),
        sa.Column('interrupted_at', sa.Integer, sa.ForeignKey('tasks.id'), primary_key=True),
        sa.Column('created_at', sa.DateTime, primary_key=True, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    )


def downgrade() -> None:
    op.drop_table('interruptions')
