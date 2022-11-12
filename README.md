# FastAPI API to import csv to database and manage products

To run the service docker and docker compose are needed to be installed
1. `git clone https://github.com/mieltn/product-import.git -b develop` to clone develop branch
2. `docker compose build` to create images
3. `docker compose up` to run the service

The main app will be available at `http://0.0.0.0:8000`. The easiest way to test endpoints - `http://0.0.0.0:8000/docs`

## Structure explained
`main.py` - initializes FastAPI and Celery apps, declares the endpoints and their functions

`database.py` - sets up the sqlalchemy database connection handlers

`models.py` - sqlalchemy models

`schemas.py` - pydantic models for reading and returning JSON

`crud.py` - core functions handling db interaction

`tasks.py` - celery import task to run as a backgroud process

`config.py` - reading from dotenv + defining factory functions for initialization of FastAPI and Celery apps

`utils.py` - several helpers