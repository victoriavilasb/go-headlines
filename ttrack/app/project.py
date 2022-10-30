from enum import Enum
from ttrack.repository.database.command import Command
from ttrack.repository.database.models import ProjectStatus
from ttrack.repository.database.query import Query

class ProjectApplication:
    class ProjectStatus(Enum):
        active = 'ACTIVE'
        archived = 'PAUSED'
        failed = 'FAILED'
        success = 'SUCCESS'

    def __init__(self, command: Command, query: Query):
        self.command = command
        self.query = query

    def start(self, name: str):
        return self.command.create_project(name)

    def archive(self, name):
        # check if there are tasks running or paused in this project

        # return with option to kill, finish or detatch tasks
        return self.command.update_project_status(name, ProjectStatus.archived)

    def active(self, name):
        return self.command.update_project_status(name, ProjectStatus.active)
