from django.contrib import admin
from django.urls import path, include   # <-- this line was missing
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
]

# Always serve media files (not just in DEBUG)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
