<div align="center">
  
<p>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Logo_UFMG.png/320px-Logo_UFMG.png" alt="alt text" width="210" height="82">
</p>


<p> <h2> Engenharia de Software II </h2> </p>

  
| [About](#TTrack) | [Set up environment](#Set-up-environment) | [Commands and descriptions](#Commands-and-descriptions) | [Members](#Members) | [Technologies](#Technologies) |
| - | - | - | - | - |

</div>


# TTrack
ttrack is an application built in python to track work.

### Set up environment
It is mandatory having docker installed in order to build the project

```cli
sudo apt install docker.io docker-compose
sudo apt install python3.8-venv
```
Clone this repository
```cli
git clone https://github.com/victoriavilasb/ttrack.git
```
Create and activate virtual environment
```cli
python3 -m venv ./venv
source venv/bin/activate
```
Install dependencies
```cli
python3 -m pip install -r requirements.txt
```
Build docker
```cli
docker-compose up -d db
```
Run migrations
```cli
alembic upgrade head
```
Run program 
```cli
python -m ttrack --help
```

### Commands and descriptions

Commands:

  - config: prepare environment for ttrack
  - start a task:
    ```cli
    python -m ttrack start task <task_name> --project <task_project> --force <force>
    ```
  - start a project:
    ```cli
    python -m ttrack start project <project_name>
    ```
  - add or remove a project from a task: 
    ```cli
    python -m ttrack edit task <task_name> --add-project <task_project> --remove-project <remove>
    ```
  - add a tag to a task:
    ```cli
    python -m ttrack add-tag --tag <tag_name> --task <task_name>
    ```
  - remove a tag from a task: 
    ```cli
    python -m ttrack remove-tag --tag <tag_name> --task <task_name>
    ```
  - resume a task:
    ```cli
    python -m ttrack continue --task <task_name>
    ```
  - pause a task:
    ```cli
    python -m ttrack pause --task <task_name>
    ```
  - finish one or more tasks: 
    ```cli
    python -m ttrack finish --task <task_name> --tasks <task_name_0,task_name_1,...>
    ```
  - activate one or more tasks:
    ```cli
    python -m ttrack activate --project <project_name> --projects <project_name_0,project_name_1,...>
    ```
  - archive one or more projects:
    ```cli
    python -m ttrack archive --project <project_name> --projects <project_name_0,project_name_1,...>
    ```
  - list tasks or projects:
    ```cli
    python -m ttrack list --projects <show_projects> --tasks <show_tasks> --status <status_to_be_shown>
    ```
  - create a shortcut:
    ```cli
    python -m ttrack create shortcut <shortcut_name> --programs <list of programs> --web-pages <list of web pages>
    ```
  - open a shortcut:
    ```cli
    python -m ttrack open shortcut <shortcut_name>
    ```
  - edit a shortcut:
    ```cli
    python -m ttrack edit shortcut <shortcut_name>
    ```

### Members

- Gabriel Magalhães Monteiro Sales
- João Lucas Rocha dos Santos
- Victoria Olivia Araujo Vilas Boas
- Vinicius Rodrigues Oliveira

### Technologies

- Python: Python was chosen because of it simplicity, and because all members from the group knows the technology
- PostgreSQL: Is a powerful system chosen as storage
- Docker: Database run as a container, and docker was chosen in order to build and run the database container
- Typer: is a python library to build powerful CLI applications
- SQLAlchemy: as the orm to query and persist data
- Alembic: to manage database migrations
