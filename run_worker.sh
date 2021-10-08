#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

# wait for RabbitMQ server to start
while ! nc -z rabbitmq 5672; do sleep 1; done

echo "Starting celery worker"
celery -A djangoTrading.celery worker --loglevel=INFO --concurrency=1 -n worker@%h