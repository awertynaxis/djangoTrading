#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Starting celery beat"
celery -A djangoTrading.celery beat