from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import goodreads, home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', goodreads, name='goodreads'),
    path('home/', home, name='home'),
    path('users/', include('users.urls', namespace='users')),
    path('books/', include('books.urls', namespace='books')),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
