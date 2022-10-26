from enum import Enum
from ttrack.repository.database.command import Command
from ttrack.repository.database.query import Query

class TaskApplication:
    class TaskStatus(Enum):
        running = 'RUNNING'
        paused = 'PAUSED'
        finished = 'FINISHED'
        
    def __init__(self, command: Command, query: Query):
        self.command = command
        self.query = query

    def start(self, name: str, project_name: str = None):
        self.command.create_task(name, project_name)

    def finish():
        pass

    def pause():
        pass

    def resume():
        pass

    def tag(self, tag_name: str):
        ## if tag does not exist, create
        pass


