from fastapi import FastAPI
from celery import Celery
from celery import current_app as current_celery_app
import os
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER"),
    os.environ.get("POSTGRES_PASSWORD"),
    os.environ.get("POSTGRES_HOST"),
    os.environ.get("POSTGRES_PORT"),
    os.environ.get("POSTGRES_DB")
)

def create_celery() -> Celery:
    app = current_celery_app
    app.conf.broker_url = os.environ.get("CELERY_BROKER_URL")
    app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND")
    return app


def create_app() -> FastAPI:
    app = FastAPI()
    app.celery_app = create_celery()
    return app



