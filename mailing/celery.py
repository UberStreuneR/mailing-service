import os


from django.conf import settings
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailing.settings')

app = Celery('mailing')

app.config_from_object('django.conf:settings', namespace="CELERY")

app.autodiscover_tasks()

app.conf.task_queues = (
    Queue('default', Exchange('default', auto_delete=True), routing_key='default'),
    Queue('mailing', Exchange('mailing', type='topic', auto_delete=True), routing_key='mailing.*'),
)

app.conf.task_routes = {
    'api.tasks.*': {'exchange': 'mailing', 'routing_key': 'mailing.tasks'},
    'main.tasks.*': {'exchange': 'default', 'routing_key': 'default'}
} 