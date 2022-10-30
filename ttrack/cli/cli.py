from enum import Enum
from typing import Optional
import typer

import os
from os import environ
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ttrack import __app_name__, __version__
from ttrack.app.project import ProjectApplication
from ttrack.app.task import TaskApplication

import yaml

ttrack = typer.Typer()
start_app = typer.Typer()
ttrack.add_typer(start_app, name = "start")

CONFIG_PATH = f"{os.environ['HOME']}/.ttrack/config.yaml"

class StorageType(Enum):
    database = "DATABASE"
    local = "LOCAL"
    blob = "BLOB"

def db_session(uri: str):
    db_string = uri
    sessionmaker().configure(bind=create_engine(db_string))
    return Session()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@ttrack.command()
def config(
    storage: str = typer.Option(..., "--storage", help="storage options are: DATABASE, LOCAL, BLOB"),
    uri: str = typer.Option(None, "--uri", help="address of your remote storage", show_default=False),
    path: str = typer.Option(None, "--path", help="path of your local storage", show_default=False)
):
    '''
    Prepare environment for ttrack
    '''
    connection = {}
    if StorageType.database == storage:
        connection = {
            'uri': uri
        }
    else:
        raise Exception("Storage is not an option")

    config = {
        'storage_type': storage,
        'connection': connection
    }

    if not os.path.exists(os.path.dirname(CONFIG_PATH)):
        os.makedirs(os.path.dirname(CONFIG_PATH))
        
    with open(CONFIG_PATH, 'w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False)


@start_app.command('task')
def start_task(
    name: str
):
    """
    Start a new task (unique name is expected as arg)
    """
    # self.task_app.start(name)
    print(name)

@start_app.command('task')
def project(
    name: str
):
    """
    Start a new project (unique name is expected as arg)
    """
    print(name)

@ttrack.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return