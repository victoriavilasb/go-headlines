# Here we will have methods that modify the database 

from ttrack.repository.database.models import Project

class Query:
    def __init__(self, session):
        self.session = session

    def get_project_id_by_name(self, name):
        pass