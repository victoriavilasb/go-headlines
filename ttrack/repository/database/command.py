# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, ProjectStatus, Task

class Command:
    def __init__(self, session):
        self.session = session

    def create_project(self, name):
        p = Project(name=name)
        self.session.add(p)
        self.session.commit()

    def create_task(self, name, project_name = None):
        project = self._get_project_by_name(project_name)
        project_id = None

        if project != None:
            project_id = project.id
            
        t = Task(name=name, project_id=project_id)
        self.session.add(t)
        self.session.commit()

    def archive_project(self, name):
        self.session.update(Project).where(Project.name == name).values(status = ProjectStatus.archived)
        self.session.commit()

    def list_projects(self):
        self.session.query(Project).all()

    def _get_project_by_name(self, project_name=None):
        if project_name != None:
            return self.session.query(Project).filter(Project.name == project_name).one()

