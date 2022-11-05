<div align="center">
  
<p>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Logo_UFMG.png/320px-Logo_UFMG.png" alt="alt text" width="210" height="82">
</p>


<p> <h2> Engenharia de Software II </h2> </p>

  
| [About](#TTrack) | [Set up environment](#Set-up-environment) | [Commands and descriptions](#Commands-and-descriptions) | [Members](#Members) | [Technologies](#Technologies) |

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

  - activate:   Activate projects
  - add-tag:     Add a tag to a project
  - archive:     Archive projects
  - config:      Prepare environment for ttrack
  - continue:    Resume a task
  - edit:        Adds or remove a project from a task 
  - finish:      Finishs a task or a project
  - list:        List project or task (check out parameters)
  - pause:       Pause a given task
  - remove-tag:  Remove tag from a task
  - resume:      Pause a given task
  - start:       Start a project or a task


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
