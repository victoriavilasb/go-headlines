import sqlalchemy as db

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from enum import Enum

Base = declarative_base()

class ProjectStatus(Enum):
    archived = 'ARCHIVED'
    active = 'ACTIVE'

class TaskStatus(Enum):
    running = 'RUNNING'
    paused = 'PAUSED'
    interrupted = 'INTERRUPTED'
    finished = 'FINISHED'

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(db.Enum(ProjectStatus), nullable=False, default=ProjectStatus.active)

    def __repr__(self) -> str:
        return "<Project(name='%s', status='%s')>" % (
            self.name,
            self.status,
        )

    def get_id(self):
        return self.id

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    name = Column(String, nullable=False)
    status = Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.running)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Task(name='%s', project_id='%s', status='%s', created_at='%s', updated_at= '%s')>" % (
            self.name,
            self.project_id,
            self.status,
            self.created_at,
            self.updated_at
        )

class Interruption(Base):
    __tablename__ = "interruptions"

    interruptor_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, nullable=True)
    interrupted_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, nullable=True)
    created_at = Column(DateTime, primary_key=True, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Interruption(interruptior_id='%s', interrupted_id='%s', created_at='%s', updated_at= '%s')>" % (
            self.interruptor_id,
            self.interrupted_id,
            self.created_at,
            self.updated_at
        )

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    def __repr__(self) -> str:
        return "<Tag(name='%s')>" % (
            self.name
        )

class TaskTag(Base):
    __tablename__ = "task_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), nullable=True)

    def __repr__(self) -> str:
        return "<TaskTag(task_id='%s', tag_id='%s')>" % (
            self.task_id,
            self.tag_id
        )


