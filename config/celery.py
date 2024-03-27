
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'refresh_location_cars': {
        'task': 'apps.car.tasks.refresh_location_cars',
        'schedule': crontab(minute='*/3'),
    },
}
