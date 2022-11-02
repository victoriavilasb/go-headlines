from abc import abstractmethod
from enum import Enum

class Storage:
    @abstractmethod
    def create_task(self, name, project_name = None):
        pass

    @abstractmethod
    def create_project(self, name, project_name = None):
        pass

    @abstractmethod
    def create_tag(self, name):
        pass

    @abstractmethod
    def update_task_status(self, name, status):
        pass

    @abstractmethod
    def update_project_status(self, name, status):
        pass

    @abstractmethod
    def add_tag_to_task(self, tag, task):
        pass

    @abstractmethod
    def remove_tag_from_task(self, tag, task):
        pass

    @abstractmethod
    def add_project_to_task(self, project, task):
        pass

    @abstractmethod
    def remove_project_from_task(self, task):
        pass

    @abstractmethod
    def list_projects(self):
        pass

    @abstractmethod
    def list_tasks(self):
        pass

    @abstractmethod
    def find_tag(self, name):
        pass

    @abstractmethod
    def find_task(self, name):
        pass

    @abstractmethod
    def find_project(self, name):
        pass

class StorageType(Enum):
    BLOB = "blob"
    LOCAL = "local"
    DATABASE = "database"
    