from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def db_connect():
    db_string = environ['DB_URI']
    return create_engine(db_string)
    
Session = sessionmaker()
Session.configure(bind=db_connect())
session = Session()
