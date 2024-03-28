from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.settings import DEBUG

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cargo/', include('apps.cargo.urls')),
    path('car/', include('apps.car.urls')),

    path('docs/schema', SpectacularAPIView.as_view(), name='schema'),
    path('docs/swagger', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger')
]

if DEBUG:
    urlpatterns += [
        path('__debug__/', include('debug_toolbar.urls')),
    ]
