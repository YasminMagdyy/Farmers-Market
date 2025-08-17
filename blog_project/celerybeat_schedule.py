# celerybeat_schedule.py
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    'update-event-statuses': {
        'task': 'eventHandler.tasks.update_event_statuses',
        'schedule': crontab(minute='*/1'),  # Every 15 minutes
    },
}