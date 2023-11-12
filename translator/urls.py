
from django.urls import path
from .views import translate_video
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', translate_video, name='translate_video'),
]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
