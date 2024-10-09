#!/bin/bash

app/docker/wait-for-it.sh "$DB_HOST:$DB_PORT" --timeout=60 --strict -- echo "PostgreSQL is up"

alembic upgrade head

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4