from django.urls import path

from apps.cargo.views import CreateCargoView, GetCargoView

urlpatterns = [
    path('create/', CreateCargoView.as_view(), name='create-cargo'),
    path('get/', GetCargoView.as_view(), name='get-cargo'),
]
