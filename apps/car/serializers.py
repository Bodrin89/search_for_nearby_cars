from rest_framework import serializers

from apps.car.models import CarModel
from apps.location.dao_location import LocationDAO


class GetCarInfoSerializer(serializers.ModelSerializer):
    """Сериализатор для получения номера всех машин и расстояний до груза"""

    class Meta:
        model = CarModel
        fields = ('id', 'number', 'now_location', 'lifting_capacity')


class UpdateCarSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления машины"""

    zip_now_location = serializers.CharField(max_length=10000, write_only=True)
    now_location = serializers.PrimaryKeyRelatedField(read_only=True)
    number = serializers.CharField(max_length=10000, required=False)
    lifting_capacity = serializers.IntegerField(required=False)

    class Meta:
        model = CarModel
        fields = ('id', 'number', 'now_location', 'lifting_capacity', 'zip_now_location')

    def update(self, instance, validated_data):

        zip_now_location = validated_data.pop('zip_now_location')

        location = LocationDAO.get_location_for_zip(zip_now_location)

        instance.number = validated_data.get('number', instance.number)
        instance.now_location = location
        instance.lifting_capacity = validated_data.get('lifting_capacity', instance.lifting_capacity)
        instance.save()
        return instance
