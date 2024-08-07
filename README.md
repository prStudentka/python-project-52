### Hexlet tests and linter status:
[![Actions Status](https://github.com/prStudentka/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/prStudentka/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/5187d7c7fe7ab0691712/maintainability)](https://codeclimate.com/github/prStudentka/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5187d7c7fe7ab0691712/test_coverage)](https://codeclimate.com/github/prStudentka/python-project-52/test_coverage)
[![Django CI](https://github.com/prStudentka/python-project-52/actions/workflows/django.yml/badge.svg)](https://github.com/prStudentka/python-project-52/actions/workflows/django.yml)

##  Task Manager
   website [Task Manager](https://task-manager-pu7v.onrender.com)

### About
Task manager - service for organizing tasks between registered users. Registration and authentication are required to work with the system.


![Main Image](https://raw.githubusercontent.com/prStudentka/python-project-52/main/media/mainWindow_taskManager.jpg)
      Image 1 - Main window app Task Manager 

### System requirements
- python = "^3.10"
- django = "4.1.3"
- django-bootstrap5 = "^23.3"
- python-dotenv = "^1.0.0"
- psycopg2-binary = "^2.9.9"
- django-filter = "^23.5"
- rollbar = "0.16.3"
- poetry = "^1.6.1"
- postgreSQL = "^15.0"
- dj-database-url = "^2.1.0"

### Install
  1) Install poetry:
  ```
       pip install poetry
  ```
  2) Clone repository:
  ```
       git clone https://github.com/prStudentka/python-project-52.git
	   cd python-project-52
  ```
  3) Install dependencies:
  ```
       make install
  ```
  4) Create file for enviromental variables:
  ```
      $ touch .env
  ```
  5) Create variables:
  
       - SECRET_KEY='{your secret key}'
	   - DATABASE_URL='postgresql://{username}:{password}@{host}:{port}/{databasename}'
  
  6) Create a new PostgreSQL database:
  ```
       whoami
       {username}
       sudo -u postgres createuser --createdb {username} 
       createdb {databasename}
  ```
  7) Make migrations:
  ```
       make migrate
  ```
  8) To create an admin superuser:
  ```
        poetry run python manage.py createsuperuser
  ```
  9) Run the development server:
  ```
       make run1
  ```
