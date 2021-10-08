#!/usr/bin/bash

# wait for RabbitMQ server to start
while ! nc -z rabbitmq 5672; do sleep 1; done

echo "Starting celery beat"
celery -A djangoTrading.celery beat