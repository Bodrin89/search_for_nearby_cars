from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class CargoModel(models.Model):
    """Модель груза"""

    class Meta:
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'
        db_table = 'cargo_cargo'

    location_pick_up = ...
    location_delivery = ...
    weight = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)],
                                              verbose_name='Вес')
    description = models.TextField(verbose_name='Описание')



