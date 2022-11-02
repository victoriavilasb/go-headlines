# Here we will have methods that modify the database 

from ttrack.repository.models import Project, ProjectStatus, Task, Tag, TaskStatus, TaskTag
from ttrack.repository.storage import Storage
from sqlalchemy import create_engine, update, Enum
from sqlalchemy.orm import sessionmaker

class Database(Storage):    
    def __init__(self, connection_data: dict):
        db_string = connection_data["uri"]

        Session = sessionmaker()
        Session.configure(bind=create_engine(db_string))

        self.session = Session()

    def create_project(self, name):
        p = Project(name=name)
        self.session.add(p)
        self.session.commit()

    def create_task(self, name, project_name = None) -> Task:
        project = self.find_project(project_name)

        task = Task(name=name, project_id=project["id"] if "id" in project else None)
        
        self.session.add(task)
        self.session.commit()

        return task.as_dict()

    def create_tag(self, name) -> Tag:
        tag = Tag(name=name)

        self.session.add(tag)
        self.session.commit()

        return tag

    def update_task_status(self, name, status):
        stmt = (
            update(Task)
                .where(Task.name == name)
                .values(status=TaskStatus(status))
        )

        self.session.execute(stmt)
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

        self.session.delete(TaskTag).where(task_id=task.id, tag_id=tag.id)
        self.session.commit()

    def list_projects(self, status = None):
        s = self.session.query(Project)
        if status != None:
            s = s.filter(Project.status == ProjectStatus(status))
        
        return [project.as_dict() for project in s.all()]

    def list_tasks(self, status = None):
        s = self.session.query(Task)
        if status != None:
            s = s.filter(Task.status == TaskStatus(status))

        return [task.as_dict() for task in s.all()]

    def find_tag(self, name):
        tag = self.session.query(Tag).filter(Tag.name == name).one_or_none()
        return tag.as_dict() if tag != None else {}
    
    def find_project(self, name):
        if not name:
            return {}

        project = self.session.query(Project).filter(Project.name == name).one_or_none()
        return project.as_dict() if project != None else {}

    def find_task(self, name):
        task = self.session.query(Task).filter(Task.name == name).one_or_none()
        return task.as_dict() if task != None else {}

    def find_project_by_id(self, id) -> Project:
        project = self.session.query(Project).filter(Project.id == id).one_or_none()
        return project.as_dict if project != None else {}

    def _db_session(self, uri: str):
        db_string = uri
        s = sessionmaker().configure(bind=create_engine(db_string))
        return s()
