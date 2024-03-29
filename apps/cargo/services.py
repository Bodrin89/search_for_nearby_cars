from geopy.distance import geodesic
from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel
from apps.cargo.dao_cargo import CargoDAO
from apps.location.models import LocationModel


class CargoService:
    """Сервис для груза"""

    @staticmethod
    def sorted_distance_cars(data, arg, key):
        """Сортировка ближайших машин по расстоянию от груза"""
        _reverse = arg == '-distance'
        for i in data:
            sorted_distance = sorted(i[key], key=lambda x: x.get('distance_car'), reverse=_reverse)
            i[key] = sorted_distance
        return data

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
    def get_nearest_cars(instance, cars, args):
        """Получение груза и количество ближайших машин"""
        nearest_cars = []

        location_cargo_lat: LocationModel = instance.location_pick_up.lat
        location_cargo_lng: LocationModel = instance.location_pick_up.lng

        response_key = 'car_info'
        for car in cars:
            location_cars_lat: CarModel = car.now_location.lat
            location_cars_lng: CarModel = car.now_location.lng

            distance_in_miles = geodesic((location_cargo_lat, location_cargo_lng),
                                         (location_cars_lat, location_cars_lng)).miles

            if distance := args.get('distance'):
                if args.get('len_cars'):
                    if distance_in_miles <= int(distance):
                        nearest_cars.append(car)
                else:
                    response_key = 'count_nearest_cars'
                    nearest_cars.append({'distance_car': distance_in_miles, 'car_id': car.pk, 'car_number': car.number})
            else:
                car_data = {
                    'car_number': car.number,
                    'distance_car': distance_in_miles
                }
                nearest_cars.append(car_data)
        if args.get('distance'):
            if args.get('len_cars'):
                response_key = 'count_nearest_cars'
                return {response_key: len(nearest_cars)}
        return {response_key: nearest_cars}
