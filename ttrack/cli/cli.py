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

# Main command
ttrack = typer.Typer()

# Sub commands
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
    name: str,
    project: str = typer.Option(None, "--project", help="associates your to an existent project", show_default=False),
    force: bool = typer.Option(False, "--force", help="forces to create a task even if there is a running task")
):
    """
    Start a new task (unique name is expected as arg)
    As humans beings are not multithreaded, ttrack records just one task at a time
    """
    task_application().start(name, project, force)

@ttrack.command("add-tag")
def tag(
    tag: str = typer.Option(..., "--tag", help="tag name"),
    task: str = typer.Option(..., "--task", help="task name"),
):
    task_application().add_tag_to_task(tag, task)

@ttrack.command("remove-tag")
def tag(
    tag: str = typer.Option(..., "--tag", help="tag name"),
    task: str = typer.Option(..., "--task", help="task name"),
):
    task_application().remove_tag_from_task(tag, task)

@ttrack.command('finish')
def finish(
    project: str = typer.Option(None, "--project", help="project name", show_default=False),
    projects: str = typer.Option([], "--projects", help="a list of projects separated by comma", show_default=False),
    task: str = typer.Option(None, "--task", help="task name", show_default=False),
    tasks: str = typer.Option([], "--tasks", help="a list of tasks separated by comma", show_default=False)
):
    """
    Finishs a task or a project
    """

    projects = projects.split(",") if len(projects) != 0 else []
    projects.append(project)

    tasks = tasks.split(",") if len(tasks) != 0 else []
    tasks.append(task)

    for project_name in projects:
        project_application().archive(project_name)

    for task_name in tasks:
        task_application().finish(task_name)

@ttrack.command("pause")
def pause(
    task: str = typer.Option(None, "--task", help="task name", show_default=False)
):
    """
    Pause a given task
    """

    task_application().pause(task)

@ttrack.command("resume")
def resume(
    task: str = typer.Option(None, "--task", help="task name", show_default=False)
):
    """
    Pause a given task
    """

    task_application().resume(task)

@start_app.command('project')
def project(
    name: str
):
    """
    Start a new project (unique name is expected as arg)
    """
    project_application().start(name)

@ttrack.command("list")
def list(
    projects: bool = typer.Option(False, "--projects", help="option to list all projects", show_default=False), 
    tasks: bool = typer.Option(False, "--tasks", help="option to list all tasks", show_default=False), 
    status: str = typer.Option("", "--status", help="status of the given resource", show_default=False), 
):
    if projects and tasks:
        print("ERROR: choose only one resource to list")
        return
    elif projects:
        print_projects(project_application().list(status))
    elif tasks:
        print_tasks(task_application().list(status))
    else:
        print("ERROR: please choose a resource to list (projects or tasks")

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

def print_projects(resources):
    table = [["NAME", "STATUS"]]
    for r in resources:
        table.append([r["name"], r["status"]])

    for row in table:
        print("{: <20} {: ^20}".format(*row))

def print_tasks(resources):
    table = [["NAME", "STATUS", "PROJECT", "CREATED_AT", "UPDATED_AT"]]
    for r in resources:
        table.append([r["name"], r["status"], r["project_id"]])

    for row in table:
        print("{: <20} {: ^20} {: ^20}".format(*row))
        
