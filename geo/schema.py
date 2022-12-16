import graphene
from graphene_django.types import DjangoObjectType
from .models import Location
from products.models import Author


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class Query(object):
    all_locations = graphene.List(LocationType)
    all_auther = graphene.List(LocationType)

    def resolve_all_locations(self, info, **kwargs):
        return Location.objects.all()

    def resolve_all_auther(self, info, **kwargs):
        return Author.objects.all()


class CreateAuthor(graphene.Mutation):
    author = graphene.Field(AuthorType)

    class Arguments:
        name = graphene.String()

    def mutate(self, info, name):
        auth = Author(name=name)
        auth.save()
        return CreateAuthor(author=auth)


class CreateLocation(graphene.Mutation):
    location = graphene.Field(LocationType)

    class Arguments:
        lat = graphene.Float()
        lon = graphene.Float()
        name = graphene.String()

    def mutate(self, info, lat, lon, name):
        loc = Location(lat=lat, lon=lon, name=name)
        loc.save()
        return CreateLocation(location=loc)


class Mutation(graphene.ObjectType):
    create_location = CreateLocation.Field()
    create_author = CreateAuthor.Field()
