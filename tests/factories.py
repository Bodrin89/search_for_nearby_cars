import factory
from factory.django import DjangoModelFactory

from apps.cargo.models import CargoModel
from apps.location.models import LocationModel


class LocationFactory(DjangoModelFactory):
    class Meta:
        model = LocationModel

    city = factory.Faker('city')
    state = factory.Faker('state')
    zip = factory.Faker('postcode')
    lat = factory.Faker('latitude')
    lng = factory.Faker('longitude')


class CargoFactory(DjangoModelFactory):
    class Meta:
        model = CargoModel

    location_pick_up = factory.SubFactory(LocationFactory)
    location_delivery = factory.SubFactory(LocationFactory)
    weight = factory.Faker('pyint', min_value=1, max_value=1000)
    description = factory.Faker('text', max_nb_chars=1000)
