"""create tasktags table

Revision ID: 469e554e613d
Revises: 1bd006d42d5d
Create Date: 2022-10-18 15:06:08.669329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '469e554e613d'
down_revision = '1bd006d42d5d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'task_tags',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('task_id', sa.Integer, sa.ForeignKey('tasks.id')),
        sa.Column('tag_id', sa.Integer, sa.ForeignKey('tags.id')),
    )


def downgrade() -> None:
    op.drop_table('task_tags')
