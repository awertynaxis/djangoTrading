from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoTrading.settings')

app = Celery('celery_tasks')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make-trade': {
        'task': 'user.tasks.make_trade',
        'schedule': crontab(minute='*/1'),
    },
}
