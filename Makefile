install:
	poetry install

build:
	install migrate

run:
	poetry run python3 manage.py runserver

PORT ?= 8000
run1:
	poetry run python3 manage.py runserver 0.0.0.0:$(PORT)
	
migrate:
	poetry run python manage.py migrate

lint:
	poetry run flake8 task_manager/
	
test:
	poetry run python manage.py test --verbosity 2

coverage:
	poetry run coverage run --source='task_manager' manage.py test -v 2
	poetry run coverage report -m && poetry run coverage xml -o coverage.xml
    

.PHONY: test