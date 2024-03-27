from pytest_factoryboy import register

from tests.factories import CarFactory, CargoFactory, LocationFactory

pytest_plugins = 'tests.fixtures'

register(LocationFactory)
register(CargoFactory)
register(CarFactory)
