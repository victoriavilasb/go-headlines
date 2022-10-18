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
    interrupted = 'INTERRUPTED'
    finished = 'FINISHED'

class Project(Base):
    __table_name__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default=ProjectStatus.active)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    update_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Project(name='%s', status='%s', created_at='%s', updated_at= '%s')>" % (
            self.name,
            self.status,
            self.created_at,
            self.update_at
        )

class Task(Base):
    __table_name__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    name = Column(String, nullable=False)
    status = Column(String, nullable=False, default=TaskStatus.running)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    update_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Task(name='%s', project_id='%s', status='%s', created_at='%s', updated_at= '%s')>" % (
            self.name,
            self.project_id,
            self.status,
            self.created_at,
            self.update_at
        )

class Interruption(Base):
    __table_name__ = "interruptions"

    interruptor_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, nullable=True)
    interrupted_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True, nullable=True)
    created_at = Column(DateTime, primary_key=True, nullable=False, default=datetime.utcnow())
    update_at = Column(DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow())

    def __repr__(self) -> str:
        return "<Interruption(interruptior_id='%s', interrupted_id='%s', created_at='%s', updated_at= '%s')>" % (
            self.interruptor_id,
            self.interrupted_id,
            self.created_at,
            self.update_at
        )
