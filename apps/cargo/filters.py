import django_filters
from django_filters.rest_framework import FilterSet

from apps.cargo.models import CargoModel


class WeightFilter(FilterSet):
    weight = django_filters.RangeFilter(field_name='weight')

    class Meta:
        model = CargoModel
        fields = ('weight',)
