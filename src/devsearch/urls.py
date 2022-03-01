from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from devsearch.settings import MEDIA_ROOT, MEDIA_URL
from projects import urls as proj_urls
from users import urls as user_urls
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('projects/', include(proj_urls)),
    path('', include(user_urls)),
]


urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,
                      document_root=settings.STATIC_ROOT)
