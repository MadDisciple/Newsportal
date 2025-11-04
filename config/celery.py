import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('config.settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send_weekly_newsletter_monday_8am': {
        'task': 'news.tasks.send_weekly_newsletter_task',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}