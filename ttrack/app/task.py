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


    def start(self, name: str, project_name: str, force: bool):
        if project_name and self.storage.find_project(project_name) == None:
            print("this project does not exist. You should choose an existent project.")
            print("run ttrack list --project to see all projects available")
            return
            
        running_task = self._get_running_task()
        if running_task:
            if force:
                self.pause(running_task["name"])
            else:
                print("Task <{}> is running. You should finish or pause this task before starting another.".format(running_task["name"]))
                return
        
        self.storage.create_task(name, project_name)

    def finish(self, name):
        self.storage.update_task_status(name, self.Status.finished.value)

    def pause(self, name):
        status = self.get_task_status(name)
        if status and status == self.Status.finished.value:
            print("failed: {} already finished".format(name))
            
        self.storage.update_task_status(name, self.Status.paused.value)

    def get_task_status(self, name):
         task = self.storage.find_task(name)
         return task["status"] if "status" in task else None
        
    def get_task_duration_in_hours(self, name):
        task = self.storage.find_task(name)
        duration = 0

        if task.status == self.Status.finished.value:
            duration = datetime(task.update_at) - datetime(task.created_at)
        else:
            duration = datetime.now - task.created_at

        duration_in_seconds = duration.total_seconds()

        return divmod(duration_in_seconds, 3600)[0]

    def list(self, status):
        myStatus = None

        try:
            myStatus = self.Status(status.upper()).value if len(status) > 0 else None
        except:
            print("Status <{}> is not a option".format(status))
            return

        return self.storage.list_tasks(myStatus)

    def resume(self):
        pass

    def tag(self, tag_name: str):
        ## if tag does not exist, create
        pass

    def _get_running_task(self):
        running_task = self.storage.list_tasks(status=self.Status.running.value)
        return running_task[0] if len(running_task) > 0 else None

        

