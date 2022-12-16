from django.urls import path, include, re_path

from django.views.decorators.csrf import csrf_exempt

from graphene_django.views import GraphQLView
from .schema import *

urlpatterns = [
    # ...
    path("token/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path("users/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schemaUser))),

]
