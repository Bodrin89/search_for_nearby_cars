from rest_framework import serializers

from apps.car.models import CarModel


class GetCarInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для получения номера всех машин и расстояний до груза"""

    class Meta:
        model = CarModel
        fields = ('id', 'number', 'now_location', 'lifting_capacity')
