# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project, ProjectStatus, Task, Tag, TaskStatus, TaskTag
from ttrack.repository.command import BaseCommand

class Command(BaseCommand):
    def __init__(self, session):
        self.session = session

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

    def change_task_status(self, name, status):
        self.session.update(Task).where(Task.name == name).values(status = TaskStatus(status).value)
        self.session.commit()

    def change_project_status(self, name, status):
        self.session.update(Project).where(Project.name == name).values(status = ProjectStatus(status).value)
        self.session.commit()

    def add_tag_to_task(self, task_name, tag_name):
        tag = self.session.query(Tag).filter(Tag.name == tag_name).one()
        task = self.session.query(Task).filter(Task.name == task_name).one()

        if tag == None:
            tag = self.create_tag(tag_name)

        self.session.add(TaskTag(task_id=task.id, tag_id=tag.id))
        self.session.commit()

    # def remove_tag_from_task(self, task_name, tag_name):
    #     task = self.session.query(Task).filter(Task.name == task_name).one()
    #     tag = self.session.query(Tag).filter(Tag.name == tag_name).one()

    #     if tag == None or task == None:
    #         raise

    #     TODO: fi

    def create_tag(self, name) -> Tag:
        tag = Tag(name=name)

        self.session.add(tag)
        self.session.commit()

        return tag

    def _get_project_by_name(self, project_name=None):
        if project_name != None:
            return self.session.query(Project).filter(Project.name == project_name).one()
