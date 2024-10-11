#!/bin/bash

# Start Gunicorn (ou substitua por python manage.py runserver para desenvolvimento)
/opt/pd-enem/venv/bin/gunicorn --workers 4 --bind 0.0.0.0:7000 core.wsgi:application --log-level debug &

# Start Celery worker
/opt/pd-enem/venv/bin/celery -A core worker --loglevel=info &

# Wait for all background processes to finish
wait
