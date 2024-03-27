from rest_framework.exceptions import ValidationError

from apps.location.models import LocationModel


class LocationDAO:

    @staticmethod
    def get_location_for_zip(zip_code):
        try:
            return LocationModel.objects.filter(zip=zip_code).first()
        except LocationModel.DoesNotExist:
            raise ValidationError('Локация не найдена')
