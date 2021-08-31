from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from authentication.views import login_view, sign_up_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('login/', login_view),
    path('signup/', sign_up_view),
    path('api/', include('api.urls')),
    path('auth/', include('authentication.urls')),
] + staticfiles_urlpatterns() +\
              static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
