from enum import Enum
from typing import Optional
import typer
import yaml

import os
from os import environ
from pathlib import Path

from ttrack import __app_name__, __version__
from ttrack.app.project import ProjectApplication
from ttrack.app.task import TaskApplication
from ttrack.repository.storage import StorageType
from ttrack.repository.database import Database

ttrack = typer.Typer()
start_app = typer.Typer()
ttrack.add_typer(start_app, name = "start")

CONFIG_PATH = "{}/.ttrack/config.yaml".format(environ['HOME'])

@ttrack.command()
def config(
    storage: str = typer.Option(..., "--storage", help="storage options are: database, local, blob"),
    uri: str = typer.Option(None, "--uri", help="address of your remote storage", show_default=False),
    path: str = typer.Option(None, "--path", help="path of your local storage", show_default=False)
):
    '''
    Prepare environment for ttrack
    '''
    config = {
        'storage_type': storage,
        'connection': mount_connection_data(storage, uri, path)
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
    task_application().start(name)

@start_app.command('project')
def project(
    name: str
):
    """
    Start a new project (unique name is expected as arg)
    """
    project_application().start(name)

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

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

def mount_connection_data(storage, uri, path):
    connection = {}
    s = StorageType(storage)
    if s == StorageType.DATABASE:
        connection = {
            'uri': uri
        }
    elif s == StorageType.LOCAL:
        connection = {
            'path': path
        }
    elif s == StorageType.BLOB:
        connection = {}
    else:
        raise Exception("Storage is not an option")

    return connection

def storage_from_configuration():
    config = {}
    with open(CONFIG_PATH) as f:
        config = yaml.safe_load(f)

        storage_type = config["storage_type"]
        connection = config["connection"]

        s = StorageType(storage_type)
        if s == StorageType.DATABASE:
            return Database(connection)
        else:
            raise NotImplementedError("Storage were not implemented")

def task_application():
    return TaskApplication(storage_from_configuration())

def project_application():
    return ProjectApplication(storage_from_configuration())
        
