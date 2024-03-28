from django.contrib import admin

from apps.car.models import CarModel


@admin.register(CarModel)
class CarAdmin(admin.ModelAdmin):
    list_display = ('id', 'number', 'now_location', 'lifting_capacity')
    search_fields = ('number', 'lifting_capacity')
    search_help_text = 'Поиск по номеру и грузоподъемности'
    list_filter = ('number', 'lifting_capacity')
