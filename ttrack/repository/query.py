from abc import abstractmethod

class BaseQuery:
    @abstractmethod
    def list_projects(self):
        pass

    def list_tasks(self):
        pass


