from geopy.distance import geodesic
from rest_framework.exceptions import ValidationError

from apps.car.dao_car import CarDAO
from apps.car.models import CarModel
from apps.cargo.dao_cargo import CargoDAO
from apps.location.models import LocationModel


class CargoService:
    """Сервис для груза"""

    @staticmethod
    def create_cargo(data):
        """Формирование данных для создания груза"""
        zip_pick_up = data.pop('zip_pick_up')
        zip_delivery = data.pop('zip_delivery')
        location_pick_up = LocationModel.objects.filter(zip=zip_pick_up).first()
        location_delivery = LocationModel.objects.filter(zip=zip_delivery).first()

        if not location_pick_up or not location_delivery:
            raise ValidationError('Неверный почтовый индекс')

        data['location_pick_up'] = location_pick_up
        data['location_delivery'] = location_delivery
        cargo = CargoDAO().dao_create_cargo(data)
        return cargo

    @staticmethod
    def get_nearest_cars(instance):
        """Получение груза и количество ближайших машин"""
        cars = CarDAO().dao_get_all_cars_with_location()

        nearest_cars = []

        location_cargo_lat: LocationModel = instance.location_pick_up.lat
        location_cargo_lng: LocationModel = instance.location_pick_up.lng

        for car in cars:
            location_cars_lat: CarModel = car.now_location.lat
            location_cars_lng: CarModel = car.now_location.lng

            distance_in_miles = geodesic((location_cargo_lat, location_cargo_lng),
                                         (location_cars_lat, location_cars_lng)).miles

            if distance_in_miles <= 450:
                nearest_cars.append(car)
        return {
            'count_nearest_cars': len(nearest_cars)
        }

    @staticmethod
    def get_info_cars(obj, cars):
        car_info_data = []

        location_cargo_lat = obj.location_pick_up.lat
        location_cargo_lng = obj.location_pick_up.lng

        for car in cars:
            location_cars_lat = car.now_location.lat
            location_cars_lng = car.now_location.lng

            distance_in_miles = geodesic((location_cargo_lat, location_cargo_lng),
                                         (location_cars_lat, location_cars_lng)).miles
            car_data = {
                'car_number': car.number,
                'distance': distance_in_miles
            }
            car_info_data.append(car_data)
        return car_info_data
