### Hexlet tests and linter status:
[![Actions Status](https://github.com/prStudentka/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/prStudentka/python-project-52/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/5187d7c7fe7ab0691712/maintainability)](https://codeclimate.com/github/prStudentka/python-project-52/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/5187d7c7fe7ab0691712/test_coverage)](https://codeclimate.com/github/prStudentka/python-project-52/test_coverage)

##  Task Manager
   website [Task Manager]()

### About
Task manager - service for organizing tasks between registered users.Registration and authentication are required to work with the system.

### System requirements
- python = "^3.10"
- django = "4.1.3"
- django-bootstrap5 = "^23.3"
- python-dotenv = "^1.0.0"
- dj-database-url = "^2.1.0"
- psycopg2-binary = "^2.9.9"
- django-filter = "^23.5"
- rollbar = "0.16.3"
- poetry = "^1.6.1"
- postgreSQL = "^15.0"

### Install
  1) Clone repository:
    git clone [Repository](https://github.com/prStudentka/python-project-83.git)
  2) Install dependencies:
    make install
  3) Create file for enviromental variables
     .env 
  4) Create a new PostgreSQL database
  5) Make migrations
     make migrate
  6) Create superuser
  7) Run the development server
     make run
