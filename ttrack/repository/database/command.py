# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, ProjectStatus, Task, Tag, TaskStatus, TaskTag
from ttrack.repository.command import BaseCommand
from ttrack.repository.database.query import Query

class Command(BaseCommand):
    def __init__(self, session):
        self.session = session
        self.query = Query(session)

    def create_project(self, name):
        p = Project(name=name)
        self.session.add(p)
        self.session.commit()

    def create_task(self, name, project_name = None) -> Task:
        project = self._get_project_by_name(project_name)
        project_id = None

        if project != None:
            project_id = project.id

        t = Task(name=name, project_id=project_id)
        self.session.add(t)
        self.session.commit()

        return t

    def create_tag(self, name) -> Tag:
        tag = Tag(name=name)

        self.session.add(tag)
        self.session.commit()

        return tag

    def update_task_status(self, name, status):
        self.session.update(Task).where(Task.name == name).values(status = TaskStatus(status).value)
        self.session.commit()

    def update_project_status(self, name, status):
        self.session.update(Project).where(Project.name == name).values(status = ProjectStatus(status).value)
        self.session.commit()

    def add_tag_to_task(self, task_name, tag):
        task = self._get_task_by_name(task_name)

        self.session.add(TaskTag(task_id=task.id, tag_id=tag.id))
        self.session.commit()

    def remove_tag_from_task(self, task_name, tag_name):
        tag = self.query.find_tag(tag_name)
        task = self._get_task_by_name(task_name)

        if tag == None:
            raise Exception("Tag does not exist")

        if task == None:
            raise Exception("Task does not exist")

        self.session.delete(TaskStatus).where(task_id=task.id, tag_id=tag.id)
        self.session.commit()

    def _get_project_by_name(self, project_name):
        return self.session.query(Project).filter(Project.name == project_name).one()

    def _get_task_by_name(self, task_name):
        return self.session.query(Task).filter(Project.name == task_name).one()


