from abc import abstractmethod

class BaseQuery:
    @abstractmethod
    def list_projects(self):
        pass

    @abstractmethod
    def list_tasks(self):
        pass

    @abstractmethod
    def find_tag(self):
        pass
