from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('frontend.urls')),
] + staticfiles_urlpatterns() +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
