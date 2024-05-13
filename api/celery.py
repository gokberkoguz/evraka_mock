# celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import json

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'evreka.settings')

# Create a Celery instance
app = Celery('evreka')

# Load task modules from all registered Django app configs.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in all applications included in INSTALLED_APPS
app.autodiscover_tasks()

def publish_to_rabbitmq(message):
    try:
        app.send_task('api.tasks.process_location_data', args=[json.dumps(message)])
        print("Message published successfully to RabbitMQ")
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error occurred while publishing message to RabbitMQ: {e}")