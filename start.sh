# psql -h postgres -U postgres -c 'CREATE DATABASE productimport;'
alembic revision --autogenerate -m 'init'
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000