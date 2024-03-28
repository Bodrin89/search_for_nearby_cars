from django.contrib import admin

from apps.location.models import LocationModel


@admin.register(LocationModel)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'state', 'zip', 'lat', 'lng')
    search_fields = ('city', 'state', 'zip')
    search_help_text = 'Поиск по городу, штату и почтовому индексу'
    list_filter = ('city', 'state', 'zip')
