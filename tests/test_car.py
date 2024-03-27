import pytest
from django.urls import reverse

from apps.car.models import CarModel
from apps.location.models import LocationModel
from config.settings import LOGGER
from utils.gen_number_car import generate_custom_code


@pytest.mark.django_db
class TestCar:
    """Тесты для машин"""

    def test_update_car(self, client, car_factory, location_factory):
        """Тест на обновление машины"""
        car: CarModel = car_factory()
        url = reverse('update-car', kwargs={'pk': car.id})
        car_number = generate_custom_code()
        location: LocationModel = location_factory()
        data_for_update = {
            'number': car_number,
            'lifting_capacity': 100,
            'zip_now_location': location.zip
        }
        response = client.put(path=url, data=data_for_update)

        expected_response = {
            'id': car.id,
            'number': car_number,
            'now_location': location.id,
            'lifting_capacity': 100

        }
        assert response.status_code == 200
        assert response.data == expected_response


