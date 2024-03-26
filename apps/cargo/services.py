from rest_framework.exceptions import ValidationError

from apps.cargo.dao import CargoDAO
from apps.location.models import LocationModel


class CargoService:

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
