from django.core.validators import MaxValueValidator, MinValueValidator
from rest_framework import serializers

from apps.cargo.models import CargoModel
from apps.cargo.services import CargoService


class CreateCargoSerializer(serializers.Serializer):
    """Сериализатор для создания груза"""

    zip_pick_up = serializers.CharField(max_length=10000, write_only=True)
    zip_delivery = serializers.CharField(max_length=10000, write_only=True)
    location_pick_up = serializers.PrimaryKeyRelatedField(read_only=True)
    location_delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    weight = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = serializers.CharField(max_length=10000)

    def create(self, validated_data):
        return CargoService().create_cargo(validated_data)


class GetCargoSerializer(serializers.ModelSerializer):
    """Сериализатор для получения груза и количество ближайших машин"""

    location_pick_up = serializers.PrimaryKeyRelatedField(read_only=True)
    location_delivery = serializers.PrimaryKeyRelatedField(read_only=True)
    car_info = serializers.SerializerMethodField()

    class Meta:
        model = CargoModel
        fields = ('id', 'location_pick_up', 'location_delivery', 'car_info')

    def validate(self, attrs):
        return attrs

    def to_representation(self, instance):
        data = super().to_representation(instance)
        value = data.pop('car_info')
        if value.get('car_info'):
            data['car_info'] = value.get('car_info')
        else:
            value.get('count_nearest_cars')
            data['count_nearest_cars'] = value.get('count_nearest_cars')
        return data

    def get_car_info(self, instance):
        cars = self.context['cars']
        distance = self.context.get('distance')
        len_cars = self.context.get('len_cars')
        return CargoService().get_nearest_cars(instance, cars, args={'distance': distance, 'len_cars': len_cars})


class UpdateCargoSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления груза"""

    description = serializers.CharField(max_length=10000, required=False)
    weight = serializers.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], required=False)

    class Meta:
        model = CargoModel
        fields = ('id', 'location_pick_up', 'location_delivery', 'description', 'weight')
        read_only_fields = ('id', 'location_pick_up', 'location_delivery')

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.description)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.save()
        return instance


class CargoRetrieveSerializer(GetCargoSerializer):
    """Сериализатор для получения груза c номерами машин и расстоянием от них до груза"""
    car_info = serializers.SerializerMethodField()

    class Meta:
        model = CargoModel
        fields = ('id', 'location_pick_up', 'location_delivery', 'description', 'weight', 'car_info')
