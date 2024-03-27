from django.urls import path

from apps.car.views import UpdateCarView

urlpatterns = [
    path('update/<int:pk>/', UpdateCarView.as_view(), name='update-car'),
]
