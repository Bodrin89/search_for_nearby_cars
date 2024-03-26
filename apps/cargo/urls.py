from django.urls import path

from apps.cargo.views import CreateCargoView

urlpatterns = [
    path('create/', CreateCargoView.as_view(), name='create-cargo'),
]
