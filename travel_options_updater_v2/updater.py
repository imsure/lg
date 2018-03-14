"""
Celery periodic tasks for updating travel options.
"""

from __future__ import absolute_import, unicode_literals

from celery import Celery
from kombu import Queue, Exchange
from celery.schedules import crontab
from celery.utils.log import get_task_logger

# from tasks import parade_otp_updater, uber_updater

app = Celery('updater', broker='amqp://')

CELERY_QUEUES = (
    Queue('uber', Exchange('uber'), routing_key='uber'),
    Queue('parade_otp', Exchange('parade_otp'), routing_key='parade_otp'),
)

CELERY_DEFAULT_QUEUE = 'uber'
CELERY_DEFAULT_EXCHANGE = 'uber'
CELERY_DEFAULT_ROUTING_KEY = 'uber'

CELERY_ROUTES = {
    # -- HIGH PRIORITY QUEUE -- #
    'updater.parade_otp_updater': {'queue': 'parade_otp'},
    # -- LOW PRIORITY QUEUE -- #
    'updater.uber_updater': {'queue': 'uber'},
}

app.conf.beat_schedule = {
    'task-parade-otp-1': {  # schedule to run at everyday midnight Pacific Standard Time
        'task': 'updater.parade_otp_updater',
        # 'schedule': crontab(minute=5, hour=8),  # UTC is 8 hours ahead of PST
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
        'schedule': 5.0,  # every 5 seconds, for testing purpose
        'options': {'queue': 'parade_otp'},
        'args': (1, 32),
    },
    'task-parade-otp-2': {  # schedule to run at everyday midnight Pacific Standard Time
        'task': 'updater.parade_otp_updater',
        # 'schedule': crontab(minute=5, hour=8),  # UTC is 8 hours ahead of PST
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
        'schedule': 30.0,  # every 30 seconds, for testing purpose
        'options': {'queue': 'parade_otp'},
        'args': (33, 64),
    },
    'task-parade-otp-3': {  # schedule to run at everyday midnight Pacific Standard Time
        'task': 'updater.parade_otp_updater',
        # 'schedule': crontab(minute=5, hour=8),  # UTC is 8 hours ahead of PST
        # 'schedule': crontab(minute='*/1'),  # for testing purpose
        'schedule': 30.0,  # every 30 seconds, for testing purpose
        'options': {'queue': 'parade_otp'},
        'args': (65, 96),
    },
}
app.conf.timezone = 'UTC'

logger = get_task_logger(__name__)


@app.task
def parade_otp_updater(slot_id_start, slot_id_end):
    print('{} - {}'.format(slot_id_start, slot_id_end))


@app.task
def uber_updater(slot_id_start, slot_id_end):
    print('{} - {}'.format(slot_id_start, slot_id_end))
