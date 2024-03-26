import random

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.location.models import LocationModel
from validators.number_car_validator import validate_custom_number


def generate_random_location_id():
    max_id = LocationModel.objects.aggregate(max_id=models.Max('id'))['max_id']
    return random.randint(1, max_id)


class CarModel(models.Model):
    """Модель машины"""

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        db_table = 'car_car'

    number = models.CharField(max_length=5, verbose_name='Номер', validators=[validate_custom_number], unique=True)
    now_location = models.ForeignKey(LocationModel, on_delete=models.PROTECT, related_name='now_location',
                                     default=generate_random_location_id, verbose_name='Текущая локация')
    lifting_capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)],
                                                        verbose_name='Грузоподъемность')
