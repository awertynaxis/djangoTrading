from __future__ import absolute_import, unicode_literals

import os
from datetime import timedelta

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTrading.settings')

app = Celery('celery_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make-trade': {
        'task': 'user.tasks.making_trade',
        'schedule': crontab(minute='*/1'),
    },
}
