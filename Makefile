PORT ?= 7777

install:
	poetry install

dev:
	poetry run ./manage.py runserver $(PORT)

lint:
	poetry run flake8 task_manager

makemessages:
	poetry run ./manage.py makemessages -l ru

compilemessages:
	poetry run ./manage.py compilemessages

makemigrations:
	poetry run ./manage.py makemigrations

migrate:
	poetry run ./manage.py migrate

shell:
	poetry run ./manage.py shell

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application

prod: migrate start

test:
	poetry run ./manage.py test

test-coverage:
	poetry run coverage run --source='.' manage.py test
	poetry run coverage xml
