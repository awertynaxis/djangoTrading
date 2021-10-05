#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Starting celery worker"
celery -A djangoTrading.celery worker --loglevel=INFO --concurrency=1 -n worker2@%h