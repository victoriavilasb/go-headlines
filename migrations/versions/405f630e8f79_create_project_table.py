"""create project table

Revision ID: 405f630e8f79
Revises: 
Create Date: 2022-10-15 23:50:13.706025

"""
from alembic import op
import sqlalchemy as sa
from enum import Enum


# revision identifiers, used by Alembic.
revision = '405f630e8f79'
down_revision = None
branch_labels = None
depends_on = None

class ProjectStatus(Enum):
    archived = 'ARCHIVED'
    active = 'ACTIVE'


def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String()),
        sa.Column('status', sa.Enum(ProjectStatus), default=ProjectStatus.active)
    )


def downgrade() -> None:
    op.drop_table('projects')
