# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, ProjectStatus, Task, TaskStatus, Tag
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

    def find_tag(self, name) -> Tag:
        return self.session.query(Tag).filter(Tag.name == name).one()
    
    def find_project(self, name) -> Project:
        return self.session.query(Project).filter(Project.name == name).one()

    def find_task(self, name) -> Task:
        return self.session.query(Task).filter(Task.name == name).one()
