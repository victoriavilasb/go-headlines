"""create task table

Revision ID: 0809629b126c
Revises: 405f630e8f79
Create Date: 2022-10-16 00:17:50.899568

"""
from datetime import datetime 

from alembic import op
import sqlalchemy as sa
from enum import Enum

# revision identifiers, used by Alembic.
revision = '0809629b126c'
down_revision = '405f630e8f79'
branch_labels = None
depends_on = None

class TaskStatus(Enum):
    running = 'RUNNING'
    interrupted = 'INTERRUPTED'
    paused = 'PAUSED'
    finished = 'FINISHED'

def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('project_id', sa.Integer, sa.ForeignKey('projects.id')),
        sa.Column('name', sa.String(), unique=True),
        sa.Column('status', sa.Enum(TaskStatus), default=TaskStatus.running),
        sa.Column('created_at', sa.DateTime, default=datetime.utcnow),
        sa.Column('updated_at', sa.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
    )

def downgrade() -> None:    
    op.drop_table('tasks')
    sa.Enum(name='taskstatus').drop(op.get_bind())
