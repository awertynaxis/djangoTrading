#!/usr/bin/bash

echo "Running migrations"
./manage.py migrate

echo "Starting gunicorn"
gunicorn djangoTrading.wsgi -c /opt/djangoTrading/configuration/gunicorn.conf.py