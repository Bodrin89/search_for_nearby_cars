
import factory
import pytest
from django.urls import reverse

from apps.cargo.services import CargoService
from tests.factories import CarFactory, CargoFactory, LocationFactory
from utils.gen_coordinates import generate_random_coordinates, generate_random_coordinates_not_radius
from utils.gen_number_car import generate_custom_code


@pytest.mark.django_db
class TestCreateCargo:
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


@pytest.mark.django_db
class TestGetCargoWithCar:
    """Тестирование получения грузов с ближайшими машинами"""

    def test_get_cargo_with_car(self, client, cargo_factory, location_factory, car_factory):
        """Тестирование получения грузов с ближайшими машинами которые попадают в заданный радиус"""
        location: LocationFactory = location_factory()

        cargo = cargo_factory(location_pick_up=location)
        NEAREST_CAR_COUNT = 10

        car = []
        for _ in range(NEAREST_CAR_COUNT):
            new_lat, new_lng = generate_random_coordinates(location, 450)
            new_location = location_factory(lat=new_lat, lng=new_lng)
            car_item: CarFactory = car_factory(number=generate_custom_code(), now_location=new_location)
            car.append(car_item)

        expected_response = {
            'location_pick_up': cargo.location_pick_up.id,
            'location_delivery': cargo.location_delivery.id,
            'count_nearest_cars': {'count_nearest_cars': NEAREST_CAR_COUNT}
        }

        url = reverse('get-cargo')
        response = client.get(path=url)
        assert response.status_code == 200
        assert response.data[0] == expected_response

    def test_get_cargo_with_not_car(self, client, cargo_factory, location_factory, car_factory):
        """Тестирование получения грузов с ближайшими машинами которые НЕ попадают в заданный радиус"""
        location: LocationFactory = location_factory()

        cargo = cargo_factory(location_pick_up=location)
        NEAREST_CAR_COUNT = 10

        car = []
        for _ in range(NEAREST_CAR_COUNT):
            new_lat, new_lng = generate_random_coordinates_not_radius(location, 4500)
            new_location = location_factory(lat=new_lat, lng=new_lng)
            car_item: CarFactory = car_factory(number=generate_custom_code(), now_location=new_location)
            car.append(car_item)

        expected_response = {
            'location_pick_up': cargo.location_pick_up.id,
            'location_delivery': cargo.location_delivery.id,
            'count_nearest_cars': {'count_nearest_cars': 0}
        }

        url = reverse('get-cargo')
        response = client.get(path=url)
        assert response.status_code == 200
        assert response.data[0] == expected_response


@pytest.mark.django_db
class TestGetCargoId:
    """Тест на получение груза по id и списка со всеми машинами"""

    def test_get_cargo_id(self, client, cargo_factory, car_factory):
        """Тест на получение груза по id и списка со всеми машинами и расстоянием до pick-up"""
        car = []
        for _ in range(10):
            car.append(car_factory(number=generate_custom_code()))

        cargo = cargo_factory()
        car_info = CargoService.get_info_cars(cargo, car)
        url = reverse('retrieve-cargo', kwargs={'pk': cargo.id})
        response = client.get(path=url)

        expected_response = {
            'id': cargo.id,
            'location_pick_up': cargo.location_pick_up.id,
            'location_delivery': cargo.location_delivery.id,
            'weight': cargo.weight,
            'description': cargo.description,
            'car_info': car_info
        }

        assert response.status_code == 200
        assert response.data == expected_response


@pytest.mark.django_db
class TestUpdateCargo:
    """Тест на обновление груза"""

    def test_update_cargo(self, client, cargo_factory):
        """Обновление описания и веса груза по id"""
        cargo = cargo_factory()

        url = reverse('update-cargo', kwargs={'pk': cargo.id})
        data_for_update = {
            'description': 'test',
            'weight': 100
        }
        response = client.put(path=url, data=data_for_update)

        expected_response = {
            'id': cargo.id,
            'location_pick_up': cargo.location_pick_up.id,
            'location_delivery': cargo.location_delivery.id,
            'weight': data_for_update['weight'],
            'description': data_for_update['description']
        }

        assert response.status_code == 200
        assert response.data == expected_response
