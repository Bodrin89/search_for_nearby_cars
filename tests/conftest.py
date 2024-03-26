from pytest_factoryboy import register

from tests.factories import CargoFactory, LocationFactory

pytest_plugins = 'tests.fixtures'

register(LocationFactory)
register(CargoFactory)
