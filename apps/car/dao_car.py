from rest_framework.exceptions import ValidationError

from apps.car.models import CarModel


class CarDAO:

    @staticmethod
    def dao_get_all_cars_with_location():
        """Получение всех машин с локацией"""
        try:
            return CarModel.objects.select_related('now_location').all()
        except CarModel.DoesNotExist:
            raise ValidationError('Машины не найдены')

    @staticmethod
    def get_car_for_id(car_id):
        """Получение машины по id"""
        try:
            return CarModel.objects.filter(id=car_id)
        except CarModel.DoesNotExist:
            raise ValidationError('Машина не найдена')
