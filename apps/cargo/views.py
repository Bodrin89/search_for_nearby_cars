from rest_framework import generics

from apps.cargo.dao_cargo import CargoDAO
from apps.cargo.serializers import CreateCargoSerializer, GetCargoSerializer


class CreateCargoView(generics.CreateAPIView):
    """View для создания груза"""

    serializer_class = CreateCargoSerializer


class GetCargoView(generics.ListAPIView):
    """View для получения груза и количество ближайших машин"""

    serializer_class = GetCargoSerializer
    queryset = CargoDAO().dao_get_cargo_with_location()
