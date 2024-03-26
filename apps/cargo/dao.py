from apps.cargo.models import CargoModel


class CargoDAO:

    @staticmethod
    def dao_create_cargo(data):
        cargo = CargoModel.objects.create(**data)
        return cargo
