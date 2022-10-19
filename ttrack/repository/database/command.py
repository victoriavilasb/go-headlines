# Here we will have methods that modify the database 

from connect import session
from models import Project

def create_project(name):
    p = Project(name=name)
    session.add(p)
    session.commit()

def archive_project(id):
    pass

def list_projects():
    pass

def main():
    create_project("tes_2")

if __name__ == "__main__":
    main()