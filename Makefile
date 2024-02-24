install:
	poetry install

build:
	poetry build

run:
	poetry run python3 manage.py runserver

run1:
	poetry run python3 manage.py runserver 0.0.0.0:8000
	
migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager/
	
test:
	poetry run python manage.py test --verbosity 2


.PHONY: test