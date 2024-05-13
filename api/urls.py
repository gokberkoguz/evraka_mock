from django.urls import path
from graphene_django.views import GraphQLView
from .views import schema  # Import the schema from your app

urlpatterns = [
    # Other URL patterns
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
]
