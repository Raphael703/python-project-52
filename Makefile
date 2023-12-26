PORT ?= 7777

install:
	poetry install

dev:
	poetry run ./manage.py runserver $(PORT)

lint:
	poetry run flake8 task_manager