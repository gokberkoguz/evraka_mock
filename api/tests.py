from django.test import TestCase
from graphene.test import Client
from .views import schema
from .models import Device, LocationData


class GraphQLTestCase(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_all_devices_query(self):
        # Create some devices
        Device.objects.create(name="Device 1", description="Description 1")
        Device.objects.create(name="Device 2", description="Description 2")

        # Construct a GraphQL query to fetch all devices
        query = '''
        {
            allDevices {
                id
                name
                description
            }
        }
        '''

        # Execute the GraphQL query
        result = self.client.execute(query)
        devices = result.get('data').get('allDevices')

        # Assert the expected number of devices and their attributes
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['name'], 'Device 1')
        self.assertEqual(devices[1]['name'], 'Device 2')

    def test_create_device_mutation(self):
        # Construct a GraphQL mutation to create a new device
        mutation = '''
        mutation {
            createDevice(name: "New Device", description: "New Description") {
                device {
                    id
                    name
                    description
                }
            }
        }
        '''

        # Execute the GraphQL mutation
        result = self.client.execute(mutation)
        new_device = result.get('data').get('createDevice').get('device')

        # Assert the newly created device's attributes
        self.assertEqual(new_device['name'], 'New Device')
        self.assertEqual(new_device['description'], 'New Description')

    def test_all_location_data_query(self):
        # Create some location data
        device = Device.objects.create(name="Device 1", description="Description 1")
        LocationData.objects.create(latitude=10.0, longitude=20.0, device=device)
        LocationData.objects.create(latitude=30.0, longitude=40.0, device=device)

        # Construct a GraphQL query to fetch all location data
        query = '''
           {
               allLocationData {
                   id
                   latitude
                   longitude
               }
           }
           '''

        # Execute the GraphQL query
        result = self.client.execute(query)
        location_data = result.get('data').get('allLocationData')

        # Assert the expected number of location data entries and their attributes
        self.assertEqual(len(location_data), 2)
        self.assertEqual(location_data[0]['latitude'], 10.0)
        self.assertEqual(location_data[1]['longitude'], 40.0)

    def test_location_history_by_device_query(self):
        # Create a device with location data
        device = Device.objects.create(name="Device 1", description="Description 1")
        LocationData.objects.create(latitude=10.0, longitude=20.0, device=device)
        LocationData.objects.create(latitude=30.0, longitude=40.0, device=device)

        # Construct a GraphQL query to fetch location history by device ID
        query = '''
           {
               locationHistoryByDevice(deviceId: %s) {
                   id
                   latitude
                   longitude
               }
           }
           ''' % device.id

        # Execute the GraphQL query
        result = self.client.execute(query)
        location_history = result.get('data').get('locationHistoryByDevice')

        # Assert the expected number of location data entries and their attributes
        self.assertEqual(len(location_history), 2)
        self.assertEqual(location_history[0]['latitude'], 10.0)
        self.assertEqual(location_history[1]['longitude'], 40.0)

    def test_invalid_query(self):
        # Construct an invalid GraphQL query
        query = '''
           {
               nonExistentField
           }
           '''

        # Execute the GraphQL query
        result = self.client.execute(query)

        # Assert that the response contains errors
        self.assertTrue('errors' in result)


def test_delete_device_mutation(self):
    # Create a device
    device = Device.objects.create(name="Device 1", description="Description 1")

    # Construct a GraphQL mutation to delete the device
    mutation = '''
        mutation {
            deleteDevice(id: %s) {
                device {
                    id
                }
            }
        }
        ''' % device.id

    # Execute the GraphQL mutation
    result = self.client.execute(mutation)
    deleted_device = result.get('data').get('deleteDevice').get('device')

    # Assert that the device was deleted
    self.assertIsNone(deleted_device)


def test_delete_all_location_data_mutation(self):
    # Create some location data
    device = Device.objects.create(name="Device 1", description="Description 1")
    LocationData.objects.create(latitude=10.0, longitude=20.0, device=device)
    LocationData.objects.create(latitude=30.0, longitude=40.0, device=device)

    # Construct a GraphQL mutation to delete all location data
    mutation = '''
        mutation {
            deleteAllLocationData {
                success
            }
        }
        '''

    # Execute the GraphQL mutation
    result = self.client.execute(mutation)
    success = result.get('data').get('deleteAllLocationData').get('success')

    # Assert that the location data was deleted successfully
    self.assertTrue(success)