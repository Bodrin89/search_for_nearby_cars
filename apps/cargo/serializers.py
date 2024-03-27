from rest_framework import serializers

from apps.cargo.models import CargoModel
from apps.cargo.services import CargoService


class CreateCargoSerializer(serializers.Serializer):
    """Сериализатор для создания груза"""

    zip_pick_up = serializers.CharField(max_length=10000, write_only=True)
    zip_delivery = serializers.CharField(max_length=10000, write_only=True)
    location_pick_up = serializers.PrimaryKeyRelatedField(read_only=True)
    location_delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    weight = serializers.IntegerField()
    description = serializers.CharField(max_length=10000)

    def create(self, validated_data):
        return CargoService().create_cargo(validated_data)


class CountNearestCarsSerializer(serializers.Serializer):
    """Сериализатор для получения груза и количество ближайших машин"""

    count_nearest_cars = serializers.IntegerField(read_only=True)

    def get_attribute(self, instance):
        return CargoService().get_nearest_cars(instance)


class GetCargoSerializer(serializers.Serializer):
    """Сериализатор для получения груза и количество ближайших машин"""

    location_pick_up = serializers.PrimaryKeyRelatedField(read_only=True)
    location_delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    count_nearest_cars = CountNearestCarsSerializer()


class CargoRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор для получения груза c номерами машин и расстоянием от них до груза"""
    car_info = serializers.SerializerMethodField()

    class Meta:
        model = CargoModel
        fields = ('id', 'location_pick_up', 'location_delivery', 'description', 'weight', 'car_info')

    def get_car_info(self, obj: CargoModel):
        return CargoService.get_info_cars(obj)
