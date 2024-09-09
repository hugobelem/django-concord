from django.contrib import admin
from django.urls import path, include

from base import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls'), name='base'),
    path("api/", include('base.api.urls')),
]
