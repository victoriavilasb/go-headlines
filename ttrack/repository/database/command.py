# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, Task

class Command:
    def __init__(self, session):
        self.session = session

    def create_project(self, name):
        p = Project(name=name)
        self.session.add(p)
        self.session.commit()

    def create_task(self, name, project_name = None):
        project = self._get_project_id_by_name(project_name) or {}
        t = Task(name=name, project_id=project.id)
        self.session.add(t)
        self.session.commit()

    def archive_project(self, name):
        pass

    def list_projects():
        pass

    def _get_project_by_name(self, project_name=None):
        if project_name != None:
            return self.session.query(Project).filter(Project.name == project_name).one()

