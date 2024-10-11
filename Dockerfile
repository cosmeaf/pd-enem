# pull the official base image
FROM python:3.9-slim

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="America/Sao_Paulo"

# set work directory
WORKDIR /app

# install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    tzdata \
    cron \
    build-essential \
    libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# copy project files
COPY . /app

# collect static files
RUN python manage.py collectstatic --noinput

# expose port 7000
EXPOSE 7000

# Entry point script to handle multiple services (Gunicorn + Celery)
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# run the entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
