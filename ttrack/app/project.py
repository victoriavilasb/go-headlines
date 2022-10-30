from enum import Enum
from ttrack.repository.storage import Storage
from ttrack.repository.models import ProjectStatus

class ProjectApplication:
    class ProjectStatus(Enum):
        active = 'ACTIVE'
        archived = 'PAUSED'
        failed = 'FAILED'
        success = 'SUCCESS'

    def __init__(self, storage: Storage):
        self.storage = storage

    def start(self, name: str):
        return self.storage.create_project(name)

    def archive(self, name):
        # check if there are tasks running or paused in this project

        # return with option to kill, finish or detatch tasks
        return self.storage.update_project_status(name, ProjectStatus.archived)

    def active(self, name):
        return self.storage.update_project_status(name, ProjectStatus.active)
