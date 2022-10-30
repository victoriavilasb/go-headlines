from enum import Enum

from datetime import datetime
from ttrack.repository.storage import Storage

class TaskApplication:
    class Status(Enum):
        running = 'RUNNING'
        paused = 'PAUSED'
        finished = 'FINISHED'

    def __init__(self, storage: Storage):
        self.storage = storage

    def start(self, name: str, project_name: str = None):
        if not project_name:
            return self.storage.create_task(name)

        project = self.storage.find_project(project_name)
        if project == None:
            raise Exception("failed: project does not exist")
        else:
            return self.storage.create_task(name, project_name)

    def finish(self, name):
        self.storage.update_task_status(name, TaskApplication.TaskStatus.finished)

    def pause(self, name):
        if self.get_task_status(name) != self.TaskStatus.finished.value:
            raise Exception("failed: task is not running")
            
        self.storage.update_task_status(name, TaskApplication.TaskStatus.paused)

    def get_task_status(self, name):
         task = self.storage.find_task(name)
         return task.status
        
    def get_task_duration_in_hours(self, name):
        task = self.storage.find_task(name)
        duration = 0

        if task.status == self.Status.finished.value:
            duration = datetime(task.update_at) - datetime(task.created_at)
        else:
            duration = datetime.now - task.created_at

        duration_in_seconds = duration.total_seconds()

        return divmod(duration_in_seconds, 3600)[0]

    def resume(self):
        pass

    def tag(self, tag_name: str):
        ## if tag does not exist, create
        pass


