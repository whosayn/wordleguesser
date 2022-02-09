from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import index,get_guesses


urlpatterns = [
    path('', index, name='main'),
    path('get_guesses/', get_guesses, name='get_guesses'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
