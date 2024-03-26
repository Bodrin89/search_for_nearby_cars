import factory
import pytest
from django.urls import reverse

from tests.factories import CargoFactory


@pytest.mark.django_db
class TestCargo:
    """Тестирование модели груза"""

    url_cargo_create = reverse('create-cargo')

    def test_create_cargo(self, client, cargo_factory):
        """Тестирование создания груза"""
        cargo: CargoFactory = cargo_factory()
        url = self.url_cargo_create
        data = {
            'zip_pick_up': cargo.location_pick_up.zip,
            'zip_delivery': cargo.location_delivery.zip,
            'weight': cargo.weight,
            'description': cargo.description,
        }
        response = client.post(path=url, data=data)

        expected_response = {
            'location_pick_up': cargo.location_pick_up.id,
            'location_delivery': cargo.location_delivery.id,
            'weight': cargo.weight,
            'description': cargo.description
        }

        assert response.status_code == 201
        assert response.data == expected_response

    def test_create_cargo_invalid_zip_pick_up(self, client, cargo_factory):
        """Тестирование создания груза с невалидным почтовым индексом zip_pick_up"""
        cargo: CargoFactory = cargo_factory()
        url = self.url_cargo_create
        data = {
            'zip_pick_up': factory.Faker('postcode'),
            'zip_delivery': cargo.location_delivery.zip,
            'weight': cargo.weight,
            'description': cargo.description,
        }
        response = client.post(path=url, data=data)

        assert response.status_code == 400

    def test_create_cargo_invalid_zip_delivery(self, client, cargo_factory):
        """Тестирование создания груза с невалидным почтовым индексом zip_delivery"""
        cargo: CargoFactory = cargo_factory()
        url = self.url_cargo_create
        data = {
            'zip_pick_up': cargo.location_pick_up.zip,
            'zip_delivery': factory.Faker('postcode'),
            'weight': cargo.weight,
            'description': cargo.description,
        }
        response = client.post(path=url, data=data)

        assert response.status_code == 400
