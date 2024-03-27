from rest_framework.exceptions import ValidationError

from apps.cargo.models import CargoModel


class CargoDAO:

    @staticmethod
    def dao_create_cargo(data):
        """Запись в БД груза"""
        cargo = CargoModel.objects.create(**data)
        return cargo

    @staticmethod
    def dao_get_cargo_with_location():
        """Получение всех грузов с локацией"""
        return CargoModel.objects.select_related('location_pick_up', 'location_delivery').all()

    @staticmethod
    def dao_get_retrieve_cargo(cargo_id):
        """Получение груза по id"""
        try:
            if CargoModel.objects.filter(id=cargo_id):
                return CargoModel.objects.filter(id=cargo_id)
            else:
                raise ValidationError('Груз не найден')
        except CargoModel.DoesNotExist:
            raise ValidationError('Груз не найден')
