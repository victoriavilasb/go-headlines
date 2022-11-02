from enum import Enum
from ttrack.repository.database.command import Command
from ttrack.repository.database.models import ProjectStatus
from ttrack.repository.database.query import Query

class ProjectApplication:
    class Status(Enum):
        active = 'ACTIVE'
        archived = 'ARCHIVED'

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
        return self.storage.update_project_status(name, ProjectStatus.active)

    def list(self, status):
        appStatus = None

        try:
            appStatus = self.Status(status.upper()).value  if len(status) > 0 else None
        except:
            print("Status <{}> is not a option".format(status))
            return
            
        return self.storage.list_projects(appStatus)
