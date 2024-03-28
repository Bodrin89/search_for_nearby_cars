from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import generics, status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from apps.cargo.dao_cargo import CargoDAO
from apps.cargo.filters import WeightFilter
from apps.cargo.serializers import (CargoRetrieveSerializer,
                                    CreateCargoSerializer,
                                    DistanceSortedSerializer,
                                    GetCargoSerializer,
                                    UpdateCargoSerializer,)


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
    queryset = CargoDAO().dao_get_cargo_with_location()

    serializer_class = GetCargoSerializer

    def list(self, request, *args, **kwargs):
        cargo = CargoDAO().dao_get_cargo_with_location()
        arg = self.request.query_params.get('ordering')
        if arg in ['distance', '-distance']:
            _reverse = False
            if arg == '-distance':
                _reverse = True

            serializer = DistanceSortedSerializer(context={'request': self.request}, instance=cargo, many=True)
            data = serializer.data

            for i in data:
                sorted_distance = sorted(i['count_nearest_cars'], key=lambda x: x.get('distance_car'), reverse=_reverse)
                i['count_nearest_cars'] = sorted_distance
            return Response(data)
        else:
            serializer = GetCargoSerializer(instance=cargo, many=True)
            return Response(serializer.data)


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
