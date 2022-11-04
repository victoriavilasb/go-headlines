<div align="center">
  
<p>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Logo_UFMG.png/320px-Logo_UFMG.png" alt="alt text" width="210" height="82">
</p>


<p> <h2> Engenharia de Software II </h2> </p>

  
| [About](#TTrack) | [Set up environment](#Set-up-environment) | [Commands and descriptions](#Commands-and-descriptions) | [Database Relationship Model](#Database-Relationship-Model)| [Members](#Members) | [Technologies](#Technologies)|
| - | - | - | - | - |

</div>


# TTrack
ttrack is an application built in python to track work.

### Set up environment
It is mandatory having docker installed in order to build the project

```cli
 docker-compose up -d db
 python -m pip install -r requirements.txt
 alembic upgrade head
```

### Commands and descriptions

| command     | description                                                       | default |
|-------------|-------------------------------------------------------------------|---------|
| version     | prints the current version of the project                         | -       |
| help        | shows the global help message for the entire application          | -       |
| start       | starts a new task. -i option creates an interruption              |         |
| finish      | finishes a task. default is the running task. -t specifies a task |         |
| report      | TODO                                                              |         |

### Database Relationship Model

<img width="446" alt="Captura de Tela 2022-10-15 às 22 15 00" src="https://user-images.githubusercontent.com/19718423/196013324-da075e7a-28bb-419f-8214-5706ada445d7.png">


### Members

- Gabriel Magalhães Monteiro Sales
- João Lucas Rocha dos Santos
- Victoria Olivia Araujo Vilas Boas
- Vinicius Rodrigues Oliveira


### Technologies

- Python is the software development technology used in this project
- PostgreSQL is the database system used in this project
- Docker is used in this project to run the database in a container
