### Tests and linter status:
[![Actions Status](https://github.com/Raphael703/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/Raphael703/python-project-52/actions)
[![PyCI](https://github.com/Raphael703/python-project-52/actions/workflows/pyci.yml/badge.svg)](https://github.com/Raphael703/python-project-83/actions/workflows/pyci.yml)
[![Test Coverage](https://api.codeclimate.com/v1/badges/bf5d3f463b1c9091b039/test_coverage)](https://codeclimate.com/github/Raphael703/python-project-52/test_coverage)
[![Maintainability](https://api.codeclimate.com/v1/badges/bf5d3f463b1c9091b039/maintainability)](https://codeclimate.com/github/Raphael703/python-project-52/maintainability)


_____

# Task Manager 📝

Welcome to the Task Manager project! This powerful task management system is designed to streamline your workflow by providing a comprehensive solution for task organization, assignment, and tracking. Whether you're working solo or managing a team, Task Manager has got you covered.

## Features

- **Task Creation**: Easily create tasks with detailed information, including name, description, and creation date.

- **Task Assignment**: Assign tasks to specific team members for clear responsibility and accountability.

- **Labels and Categories**: Categorize tasks with custom labels to organize and prioritize your workload effectively.

- **Status Tracking**: Monitor the progress of your tasks by assigning various status labels, keeping everyone informed about task completion.

- **User-Friendly Interface**: Intuitive and user-friendly design ensures a seamless experience for both beginners and seasoned users.





## Content
- [Used packages](#used-packages)
- [Prod server](#prod-server)
- [For Dev](#for-dev)
- [How to deploy](#how-to-deploy)
- [Author](#author)

## Requirements
- [Python 3.10+](https://www.python.org/downloads/release/python-3100/)
- [Poetry](https://python-poetry.org/)
- [Postgres](https://www.postgresql.org/)

## Used packages
 - [Django](https://www.djangoproject.com/) 
 - [gunicorn](https://gunicorn.org/)
 - [psycopg2-binary](https://www.psycopg.org/docs/install.html)
 - [python-dotenv](https://github.com/theskumar/python-dotenv)
 - [django-bootstrap5](https://pypi.org/project/django-bootstrap5/)
 - [django-filter](https://django-filter.readthedocs.io/en/stable/)
 - [rollbar](https://app.rollbar.com/a/raphael.mukha/FirstProject/onboarding/embark)

## Prod server
Go to link: https://task-manager-n8xi.onrender.com/



______
## For Dev
#### Clone this repository:
```sh
git clone https://github.com/Raphael703/python-project-52.git
```

#### Install dependencies
```sh
make install
```

#### Create .env file in sources root and fill it (example)
```dotenv
SECRET_KEY=notsosecret
DEBUG=True
DATABASE_URL=postgresql://pguser:pgpass@localhost:5434/pgdb
ROLLBAR_TOKEN=get_your_post_client_item_token
```

#### Up postgres DB (Docker for example):
```sh
docker run -d \
    --name dev_page_analyzer \
    -e POSTGRES_USER=pguser \
    -e POSTGRES_PASSWORD=pgpass \
    -e POSTGRES_DB=pgdb \
    -p 5434:5432 \
    postgres:latest
```

#### Run local server:
```shell
make dev
```

### Go to 
http://127.0.0.1:7777

#### Run linter in project use
```sh
make lint
```
#### Run test local
```sh
make test
```

## How to deploy

1. The project should be deployed on PaaS like [render.com](https://render.com)
2. Start Postgres DB and get external DB URL
3. Fill in the environment variables (like in example with DB url)

## Author
- [Rafael Mukhametshin](https://github.com/Raphael703)