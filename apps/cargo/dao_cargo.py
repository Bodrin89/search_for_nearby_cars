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
