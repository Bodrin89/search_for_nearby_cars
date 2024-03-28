from rest_framework import generics

from apps.car.dao_car import CarDAO
from apps.car.serializers import UpdateCarSerializer


class UpdateCarView(generics.UpdateAPIView):

    serializer_class = UpdateCarSerializer
    http_method_names = ['put']

    def get_queryset(self):
        car_id = self.kwargs.get('pk')
        car = CarDAO.get_car_for_id(car_id)
        return car
