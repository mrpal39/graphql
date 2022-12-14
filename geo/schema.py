import graphene
from graphene_django.types import DjangoObjectType
from .models import Location


class LocationType(DjangoObjectType):
    class Meta:
        model = Location


class Query(object):
    all_locations = graphene.List(LocationType)

    def resolve_all_locations(self, info, **kwargs):
        return Location.objects.all()


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
