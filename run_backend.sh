#!/usr/bin/bash

# wait for Postgresql server to start
while ! nc -z postgres 5432; do sleep 1; done

echo "Running migrations"
./manage.py migrate

echo "Starting gunicorn"
gunicorn djangoTrading.wsgi -c /opt/djangoTrading/configuration/gunicorn.conf.py