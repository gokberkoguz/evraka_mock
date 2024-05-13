```markdown
# Evreka Mock

This is a basic CRUD application that utilizes GraphQL on top of Django. It uses RabbitMQ as a queue and Celery to consume it.

## Run

```sh
docker-compose build
docker-compose up
```

## Endpoints

- **API Endpoint:** [http://0.0.0.0:8000/api/graphql](http://0.0.0.0:8000/api/graphql)
- **RabbitMQ Interface:** [http://0.0.0.0:15672/](http://0.0.0.0:15672/)
  - **Username:** guest
  - **Password:** guest

## API Queries

### Create Device

```graphql
mutation createDevice($name: String!, $description: String!) {
    createDevice(name: $name, description: $description) {
        device {
            id
            name
            description
        }
    }
}
```

### Delete Device

```graphql
mutation {
    deleteDevice(id: 1) {
        device {
            id
            name
            description
        }
    }
}
```

### Get All Devices

```graphql
query {
  allDevices {
    id
    name
    description
  }
}
```

### Location History by Device

```graphql
query {
    locationHistoryByDevice(deviceId: 1) {
        id
        latitude
        longitude
        timestamp
    }
}
```

### Publish Location Data for a Device

```graphql
mutation {
  publishLocationData(latitude: 0, longitude: 0, deviceId: 1) {
    success
  }
}
```

### Get Last Location for All Devices

```graphql
query {
  lastLocationForAllDevices {
    id
    latitude
    longitude
    device { id }
    timestamp
  }
}
```

## Explanation

Ideally i would use flask for a small crud project but graphql extension of flask repository is not updated for a while and conflicts with new version of werkzeug thus i moved to django.
All of the services defined and runs through docker-compose. (DB,Rabbitmq,django,celery,simulation). Celery is responsible to consume the queue without any error handling :)). Simulation is responsible to feed location data. Initially i add a 1 sec timeout but when i tested without timeout i could hit 160 rps on my local which is around 13m request per day. 
This is the first time i have been using graphql thus most of the code is chatgpt generated (api/views.py). Ideally i would separate the models and views for device and location to get closer to the microservice architecture as much as you can do using django. 

For tests, instead of expanding the tests coverage i went out with friends. 

And i used my work computer which is setted up for a different github user and zip the project. Thus no commit history :) 



```

