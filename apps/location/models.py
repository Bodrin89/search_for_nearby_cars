from django.db import models


class LocationModel(models.Model):
    """Модель локации"""

    class Meta:
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
        db_table = 'location_location'

    city = models.CharField(max_length=100, verbose_name='Город')
    state = models.CharField(max_length=100, verbose_name='Штат')
    zip = models.CharField(max_length=100, verbose_name='Почтовый индекс')
    lat = models.FloatField(verbose_name='Широта')
    lng = models.FloatField(verbose_name='Долгота')
