
from django.contrib import admin
from django.urls import include, path

from config.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cargo/', include('apps.cargo.urls')),
    path('car/', include('apps.car.urls')),
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
