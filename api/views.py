import graphene
from graphene_django.types import DjangoObjectType
from .models import Device, LocationData
from .celery import publish_to_rabbitmq


class DeviceType(DjangoObjectType):
    class Meta:
        model = Device


class LocationDataType(DjangoObjectType):
    class Meta:
        model = LocationData


# Define GraphQL mutations for creating and deleting devices
class CreateDevice(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String(required=True)

    device = graphene.Field(DeviceType)

    def mutate(self, info, name, description):
        device = Device(name=name, description=description)
        device.save()
        return CreateDevice(device=device)


class DeleteDevice(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    device = graphene.Field(DeviceType)

    def mutate(self, info, id):
        device = Device.objects.get(pk=id)
        device.delete()
        return "Deleted"


class PublishLocationData(graphene.Mutation):
    class Arguments:
        latitude = graphene.Float(required=True)
        longitude = graphene.Float(required=True)
        device_id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, latitude, longitude, device_id):
        try:
            location_data = {
                'latitude': latitude,
                'longitude': longitude,
                'device_id': device_id
            }

            publish_to_rabbitmq(location_data)

            return PublishLocationData(success=True)  # Returning instance with success=True
        except Exception as e:
            # Log the error for debugging purposes
            print(f"Error occurred while publishing location data to RabbitMQ: {e}")
            return PublishLocationData(success=False)


class DeleteAllLocationData(graphene.Mutation):
    success = graphene.Boolean()
    def mutate(self, info):
        try:
            LocationData.objects.all().delete()
            return DeleteAllLocationData(success=True)
        except Exception as e:
            return DeleteAllLocationData(success=False)


# Define Mutation and Query classes
class Mutation(graphene.ObjectType):
    create_device = CreateDevice.Field()
    delete_device = DeleteDevice.Field()
    publish_location_data = PublishLocationData.Field()  # New mutation field
    delete_all_location_data = DeleteAllLocationData.Field()


class Query(graphene.ObjectType):
    all_devices = graphene.List(DeviceType)
    all_location_data = graphene.List(LocationDataType)
    location_history_by_device = graphene.List(LocationDataType, device_id=graphene.Int())
    last_location_for_all_devices = graphene.List(LocationDataType)

    def resolve_all_devices(self, info, **kwargs):
        return Device.objects.all()

    def resolve_all_location_data(self, info, **kwargs):
        return LocationData.objects.all()

    def resolve_location_history_by_device(self, info, device_id):
        return LocationData.objects.filter(device_id=device_id)

    def resolve_last_location_for_all_devices(self, info):
        last_locations = []
        devices = Device.objects.all()
        for device in devices:
            last_location = LocationData.objects.filter(device=device).order_by('-timestamp').first()
            if last_location:
                last_locations.append(last_location)
        return last_locations

# Create the schema
schema = graphene.Schema(query=Query, mutation=Mutation)
