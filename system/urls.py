import debug_toolbar
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from ecogenius import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                   static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + \
                   static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
