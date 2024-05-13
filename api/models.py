from django.db import models

class Device(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class LocationData(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='location_data')
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Location data for {self.device.name} at {self.timestamp}"
