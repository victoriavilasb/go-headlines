# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, ProjectStatus, Task, TaskStatus
from ttrack.repository.query import BaseQuery

class Query(BaseQuery):
    def __init__(self, session):
        self.session = session

    def list_projects(self, status = None):
        s = self.session.query(Project)
        if status != None:
            s.filter(status = ProjectStatus(status).value)
        
        return s.all()

    def list_tasks(self, status = None):
        s = self.session.query(Task)
        if status != None:
            s.filter(status = TaskStatus(status).value)
        
        return s.all()
