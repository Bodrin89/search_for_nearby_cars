from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.car.dao_car import CarDAO
from apps.cargo.dao_cargo import CargoDAO
from apps.cargo.filters import WeightFilter
from apps.cargo.serializers import (CargoRetrieveSerializer,
                                    CreateCargoSerializer,
                                    GetCargoSerializer,
                                    UpdateCargoSerializer,)
from apps.cargo.services import CargoService
from config.settings import DISTANCE_MILES


class CreateCargoView(generics.CreateAPIView):
    """View для создания груза"""

    serializer_class = CreateCargoSerializer


@extend_schema(
    parameters=[
        OpenApiParameter(name='ordering',
                         location=OpenApiParameter.QUERY,
                         description='Сортировка ближайших машин по расстоянию от груза',
                         required=False,
                         enum=['distance', '-distance'],
                         type=str),
    ],
)
class GetCargoView(generics.ListAPIView):
    """View для получения груза и количество ближайших машин"""

    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ('id', 'weight')
    ordering = ['weight']
    filterset_class = WeightFilter
    pagination_class = PageNumberPagination

    queryset = CargoDAO.dao_get_cargo_with_location()
    serializer_class = GetCargoSerializer

    def get(self, request, *args, **kwargs):
        distance = DISTANCE_MILES
        cars = CarDAO.dao_get_all_cars_with_location()
        cargo = CargoDAO.dao_get_cargo_with_location()
        serializer = self.get_serializer(cargo, context={'cars': cars, 'len_cars': True, 'distance': distance}, many=True)
        arg = self.request.query_params.get('ordering')
        if arg in ['distance', '-distance']:

            serializer = self.get_serializer(context={'request': self.request, 'cars': cars, 'distance': distance},
                                             instance=cargo, many=True)
            data = serializer.data

            CargoService.sorted_distance_cars(data, arg, key='count_nearest_cars')
            return Response(data)
        else:
            return Response(serializer.data)


class GetCargoIdView(generics.RetrieveAPIView):
    """View для получения груза по id c номерами машин и расстоянием от них до груза"""

    serializer_class = CargoRetrieveSerializer

    def get(self, request, *args, **kwargs):
        cars = CarDAO.dao_get_all_cars_with_location()
        cargo_id = self.kwargs.get('pk')
        cargo = CargoDAO().dao_get_retrieve_cargo(cargo_id)
        if not cargo:
            raise ValidationError('Груз не найден')
        serializer = self.get_serializer(cargo, context={'cars': cars},
                                         many=True)
        arg = self.request.query_params.get('ordering')
        if arg in ['distance', '-distance']:
            serializer = self.get_serializer(context={'request': self.request, 'cars': cars},
                                             instance=cargo,
                                             many=True)
            data = serializer.data

            CargoService.sorted_distance_cars(data, arg, key='car_info')

            return Response(data)
        return Response(serializer.data)

    def get_queryset(self):
        cargo_id = self.kwargs.get('pk')
        cargo = CargoDAO().dao_get_retrieve_cargo(cargo_id)
        return cargo


class UpdateCargoView(generics.UpdateAPIView):
    """View для обновления груза"""

    serializer_class = UpdateCargoSerializer
    http_method_names = ['put']

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
