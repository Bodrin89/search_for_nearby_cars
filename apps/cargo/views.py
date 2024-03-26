from rest_framework import generics

from apps.cargo.serializers import CreateCargoSerializer


class CreateCargoView(generics.CreateAPIView):
    """View для создания груза"""

    serializer_class = CreateCargoSerializer
