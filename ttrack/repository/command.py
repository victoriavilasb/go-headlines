from abc import abstractmethod

class BaseCommand:
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
    def add_tag_to_task(self, tag_name, task_name):
        pass

    @abstractmethod
    def remove_tag_from_task(self, tag_name, task_name):
        pass
    