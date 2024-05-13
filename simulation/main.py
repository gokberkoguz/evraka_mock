import requests
import time
import random
"""
Container to create devices and feeds location data to simulate real world scenario. 
PS: Sleeps first cause i felt lazy. 
"""
def create_device(name, description):
    mutation = """
    mutation createDevice($name: String!, $description: String!) {
        createDevice(name: $name, description: $description) {
            device {
                id
                name
                description
            }
        }
    }
    """

    # Define the variables for the mutation
    variables = {
        'name': name,
        'description': description
    }

    # Define the GraphQL endpoint URL
    graphql_url = 'http://django:8000/api/graphql/'  # Updated URL

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Send the mutation as a POST request
    response = requests.post(graphql_url, json={'query': mutation, 'variables': variables}, headers=headers)


def feed_location_data(device_id):
    mutation = """
        mutation AddLocationData($latitude: Float!, $longitude: Float!, $deviceId: ID!) {
            publishLocationData(latitude: $latitude, longitude: $longitude, deviceId: $deviceId) {
                success
            }
        }
    """

    # Define the variables for the mutation
    variables = {
        'latitude': random.uniform(-90, 90),
        'longitude': random.uniform(-180, 180),
        'deviceId': device_id
    }

    # Define the GraphQL endpoint URL
    graphql_url = 'http://django:8000/api/graphql/'  # Updated URL

    # Set up the request headers
    headers = {
        'Content-Type': 'application/json',
    }

    # Send the mutation as a POST request
    response = requests.post(graphql_url, json={'query': mutation, 'variables': variables}, headers=headers)
    return response

def run():
    for i in range(1, 6):
        create_device("Device_" + str(i), "Description_" + str(i))
    while True:
        for device_id in range(1, 6):
            feed_location_data(device_id)
        time.sleep(1)  # Simulate feeding location data every 1 seconds

if __name__ == "__main__":
    time.sleep(20)
    run()
