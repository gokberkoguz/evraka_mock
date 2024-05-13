from celery import shared_task
from .models import LocationData
import json

@shared_task
def process_location_data(message):
    data = json.loads(message)

    # Create or update database records
    LocationData.objects.update_or_create(
        latitude=data['latitude'],
        longitude=data['longitude'],
        device_id=data['device_id']
    )
