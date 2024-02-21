from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static

urlpatterns = [
    path("configuracion/administrativa/", admin.site.urls),
    path("", include("main.urls"), name="main"),
    path("auth/", include("authentication.urls"), name="authentication"),
    path("biblioteca/", include("biblioteca_SC.urls"), name="biblioteca"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#      urlpatterns += path('admin/', admin.site.urls)
