from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.location.models import LocationModel


class CarModel(models.Model):
    """Модель машины"""

    class Meta:
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'
        db_table = 'car_car'

    number = models.CharField(max_length=5, verbose_name='Номер', unique=True)
    now_location = models.ForeignKey(LocationModel, on_delete=models.PROTECT, related_name='now_location', verbose_name='Текущая локация')
    lifting_capacity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], verbose_name='Грузоподъемность')

