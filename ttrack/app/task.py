from enum import Enum

from datetime import datetime
from ttrack.repository.storage import Storage

class TaskApplication:
    class Status(Enum):
        running = 'RUNNING'
        paused = 'PAUSED'
        finished = 'FINISHED'

    def __init__(self, storage: Storage, name: str = None, project_name: str = None):
        self.storage = storage
        self.name = name
        self.project_name = project_name

    def start(self, force: bool):
        if self.project_name and self.storage.find_project(self.project_name) == None:
            print("ERROR: this project does not exist. You should choose an existent project.")
            print("run ttrack list --project to see all projects available")
            return
            
        running_task = self._get_running_task()
        if running_task:
            if force:
                self.storage.update_task_status(
                    running_task["name"],
                    self.Status.paused.value
                )
            else:
                print("ERROR: {} is running. You should finish or pause this task before starting another.".format(running_task["name"]))
                return
        
        self.storage.create_task(self.name, self.project_name)

    def finish(self):
        self.storage.update_task_status(self.name, self.Status.finished.value)

    def pause(self):
        status = self.get_task_status(self.name)
        if status and status == self.Status.finished.value:
            print("ERROR: {} already finished".format(self.name))
            
        self.storage.update_task_status(self.name, self.Status.paused.value)

    def get_task_status(self):
         task = self.storage.find_task(self.name)
         return task["status"] if "status" in task else None
        
    def get_task_duration_in_hours(self):
        task = self.storage.find_task(self.name)
        duration = 0

        if task.status == self.Status.finished.value:
            duration = datetime(task.update_at) - datetime(task.created_at)
        else:
            duration = datetime.now - task.created_at

        duration_in_seconds = duration.total_seconds()

        return divmod(duration_in_seconds, 3600)[0]

    def list(self, status):
        my_status = None

        try:
            my_status = self.Status(status.upper()).value if len(status) > 0 else None
        except:
            print("ERROR: status {} is not a option".format(status))
            return

        return self.storage.list_tasks(my_status)

    def add_tag_to_task(self, tag_name: str):
        tag = self.storage.find_tag(tag_name)
        task = self.storage.find_task(self.name)

        if len(tag) == 0:
            tag = self.storage.create_tag(tag_name)
        if len(task) == 0:
            print("ERROR: task does not exist")
            return

        task = self.storage.add_tag_to_task(tag, task)

    def remove_tag_from_task(self, tag_name: str):
        tag = self.storage.find_tag(tag_name)
        task = self.storage.find_task(self.name)

        if len(tag) == 0:
            print("ERROR: tag does not exist")
            return
        if len(task) == 0:
            print("ERROR: task does not exist")
            return

        task = self.storage.remove_tag_from_task(tag, task)

    def resume(self):
        running_task = self._get_running_task()
        if running_task:
            print("ERROR: {} is running. You should finish or pause this task before continuing another.".format(running_task["name"]))
            return

        self.storage.update_task_status(self.name, self.Status.running.value)

    def tag(self, tag_name: str):
        ## if tag does not exist, create
        pass

    def _get_running_task(self):
        running_task = self.storage.list_tasks(status=self.Status.running.value)
        return running_task[0] if len(running_task) > 0 else None

        

