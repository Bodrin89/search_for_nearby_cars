from apps.cargo.models import CargoModel


class CargoDAO:

    @staticmethod
    def dao_create_cargo(data):
        """Запись в БД груза"""
        cargo = CargoModel.objects.create(**data)
        return cargo
