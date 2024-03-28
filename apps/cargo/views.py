from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from apps.cargo.dao_cargo import CargoDAO
from apps.cargo.filters import WeightFilter
from apps.cargo.serializers import (CargoRetrieveSerializer,
                                    CreateCargoSerializer,
                                    GetCargoSerializer,
                                    UpdateCargoSerializer,)


class CreateCargoView(generics.CreateAPIView):
    """View для создания груза"""

    serializer_class = CreateCargoSerializer


class GetCargoView(generics.ListAPIView):
    """View для получения груза и количество ближайших машин"""

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id', 'weight')
    ordering = ['weight']
    filterset_class = WeightFilter

    serializer_class = GetCargoSerializer
    queryset = CargoDAO().dao_get_cargo_with_location()


class GetCargoIdView(generics.RetrieveAPIView):
    """View для получения груза c номерами машин и расстоянием от них до груза"""

    serializer_class = CargoRetrieveSerializer

    def get_queryset(self):
        cargo_id = self.kwargs.get('pk')
        cargo = CargoDAO().dao_get_retrieve_cargo(cargo_id)
        return cargo


class UpdateCargoView(generics.UpdateAPIView):
    """View для обновления груза"""

    serializer_class = UpdateCargoSerializer

    def get_queryset(self):
        cargo_id = self.kwargs.get('pk')
        cargo = CargoDAO().dao_get_retrieve_cargo(cargo_id)
        return cargo


class DeleteCargoView(generics.DestroyAPIView):
    """View для удаления груза"""

    def destroy(self, request, *args, **kwargs):
        cargo_id = self.kwargs.get('pk')
        cargo = CargoDAO().dao_get_retrieve_cargo(cargo_id)
        cargo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
