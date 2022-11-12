from fastapi import FastAPI
from celery import Celery
from celery import current_app as current_celery_app
import os
from dotenv import load_dotenv

load_dotenv()


SQLALCHEMY_DATABASE_URL = "postgresql://{}:{}@{}:{}/{}".format(
    os.environ.get("POSTGRES_USER", "postgres"),
    os.environ.get("POSTGRES_PASSWORD", "postgres"),
    os.environ.get("POSTGRES_HOST", "localhost"),
    os.environ.get("POSTGRES_PORT", "5432"),
    os.environ.get("POSTGRES_DB", "productimport")
)


def create_celery() -> Celery:
    app = current_celery_app
    app.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
    app.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
    return app


def create_app() -> FastAPI:
    app = FastAPI()
    app.celery_app = create_celery()
    return app



