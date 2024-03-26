from apps.car.models import CarModel


class CarDAO:

    @staticmethod
    def dao_get_all_cars_with_location():
        """Получение всех машин с локацией"""
        return CarModel.objects.select_related('now_location').all()
