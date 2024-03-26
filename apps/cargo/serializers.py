from rest_framework import serializers

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
