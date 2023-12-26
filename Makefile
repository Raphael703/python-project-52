PORT ?= 7777

install:
	poetry install

dev:
	poetry run ./manage.py runserver $(PORT)

lint:
	poetry run flake8 task_manager

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi:application