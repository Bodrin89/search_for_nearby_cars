from django.contrib import admin

from apps.cargo.models import CargoModel


@admin.register(CargoModel)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id', 'location_pick_up', 'location_delivery', 'weight', 'description')
