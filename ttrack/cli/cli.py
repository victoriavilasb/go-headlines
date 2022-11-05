from enum import Enum
from typing import Optional
import typer

import os
from os import environ
from pathlib import Path

from ttrack import __app_name__, __version__
from ttrack.app.project import ProjectApplication
from ttrack.app.task import TaskApplication
from ttrack.app.config import Configuration
from ttrack.repository.storage import StorageType
from ttrack.repository.database import Database

# Main command
ttrack = typer.Typer()

# Sub commands
start_app = typer.Typer()
edit_app = typer.Typer()

ttrack.add_typer(start_app, name = "start")
ttrack.add_typer(edit_app, name = "edit")

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
    Configuration(CONFIG_PATH).create_or_update(uri, path, storage)

@start_app.command('task')
def start_task(
    name: str,
    project: str = typer.Option(None, "--project", help="associates your task to an existent project", show_default=False),
    force: bool = typer.Option(False, "--force", help="forces to create a task even if there is a running task")
):
    """
    Start a new task (unique name is expected as arg)
    As humans beings are not multithreaded, ttrack records just one task at a time
    """
    _task_application(name, project).start(force)

@edit_app.command('task')
def edit_task(
    name: str,
    project: str = typer.Option("", "--add-project", help="associates your task to an existent project", show_default=False),
    remove: bool = typer.Option(False, "--remove-project", help="associates your task to an existent project", show_default=False),
):
    """
    Start a new task (unique name is expected as arg)
    As humans beings are not multithreaded, ttrack records just one task at a time
    """
    if len(project):
        project_application().add_project_to_task(project, name)
    if remove:
        project_application().remove_project_from_task(name)
        

@ttrack.command("add-tag")
def tag(
    tag: str = typer.Option(..., "--tag", help="tag name"),
    task: str = typer.Option(..., "--task", help="task name"),
):
    _task_application(task).add_tag_to_task(tag)

@ttrack.command("remove-tag")
def tag(
    tag: str = typer.Option(..., "--tag", help="tag name"),
    task: str = typer.Option(..., "--task", help="task name"),
):
    _task_application(task).remove_tag_from_task(tag)

@ttrack.command('finish')
def finish(
    task: str = typer.Option(None, "--task", help="task name", show_default=False),
    tasks: str = typer.Option([], "--tasks", help="a list of tasks separated by comma", show_default=False)
):
    """
    Finishs a task or a project
    """
    tasks = tasks.split(",") if len(tasks) != 0 else []
    if task:
        tasks.append(task)

    for task_name in tasks:
        _task_application(task_name).finish()

@ttrack.command('continue')
def finish(
    task: str = typer.Option(None, "--task", help="task name", show_default=False),
):
    """
    Resume a task
    """
    _task_application().resume(task)

@ttrack.command('archive')
def archive(
    project: str = typer.Option(None, "--project", help="project name", show_default=False),
    projects: str = typer.Option([], "--projects", help="a list of projects separated by comma", show_default=False)
):
    """
    Archive projects
    """
    projects = projects.split(",") if len(projects) != 0 else []
    if project:
        projects.append(project)

    for project_name in projects:
        project_application().archive(project_name)

@ttrack.command('activate')
def activate(
    project: str = typer.Option(None, "--project", help="project name", show_default=False),
    projects: str = typer.Option([], "--projects", help="a list of projects separated by comma", show_default=False)
):
    """
    Activate projects
    """
    projects = projects.split(",") if len(projects) != 0 else []
    if project:
        projects.append(project)

    for project_name in projects:
        project_application().activate(project_name)


@ttrack.command("pause")
def pause(
    task: str = typer.Option(None, "--task", help="task name", show_default=False)
):
    """
    Pause a given task
    """

    _task_application(task).pause()

@ttrack.command("resume")
def resume(
    task: str = typer.Option(None, "--task", help="task name", show_default=False)
):
    """
    Pause a given task
    """

    _task_application(task).resume()

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
    elif projects:
        print_projects(project_application().list(status))
    elif tasks:
        print_tasks(_task_application().list(status))
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

def _task_application(name = None, project_name = None):
    config = Configuration(CONFIG_PATH)
    return TaskApplication(config.instance_database(), name, project_name)

def project_application():
    config = Configuration(CONFIG_PATH)
    return ProjectApplication(config.instance_database())

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
        
