from enum import Enum
from ttrack.repository.storage import Storage
from ttrack.repository.models import ProjectStatus

class ProjectApplication:
    class Status(Enum):
        active = 'ACTIVE'
        archived = 'ARCHIVED'

    def __init__(self, storage: Storage, name = None):
        self.storage = storage
        self.name = name

    def start(self):
        return self.storage.create_project(self.name)

    def archive(self):
        return self.storage.update_project_status(self.name, ProjectStatus.archived.value)

    def activate(self):
        return self.storage.update_project_status(self.name, ProjectStatus.active.value)

    def list(self, status):
        app_status = None

        try:
            app_status = self.Status(status.upper()).value  if len(status) > 0 else None
        except:
            print("Status <{}> is not a option".format(status))
            return
            
        return self.storage.list_projects(app_status)

    def add_project_to_task(self, task_name: str):
        project = self.storage.find_project(self.project_name)
        task = self.storage.find_task(task_name)


        if len(project) == 0:
            print("ERROR: project does not exist")
            return
        if len(task) == 0:
            print("ERROR: task does not exist")
            return

        task = self.storage.add_project_to_task(project, task)

    def remove_project_from_task(self, task_name: str):
        task = self.storage.find_task(task_name)

        if len(task) == 0:
            print("ERROR: task does not exist")
            return

        task = self.storage.remove_project_from_task(task)
