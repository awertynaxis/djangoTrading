#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

function start_backend() {

  echo "Collecting static"
  ./manage.py collectstatic

  echo "Starting gunicorn"
  gunicorn djangoTrading.wsgi \
          --bind 0.0.0.0:8000 \
          --reload \
          --max-requests 100 \
          --threads 2 \
          --access-logfile -
}

function start_worker() {
    echo "Starting celery worker"
    celery -A djangoTrading.celery worker --loglevel=INFO --concurrency=1 -n worker2@%h
}

function start_beat() {
    echo "Starting celery beat"
    celery -A djangoTrading.celery beat
}

case $SERVICE in
backend)
  start_backend
  ;;
worker)
  start_worker
  ;;
beat)
  start_beat
  ;;
esac