from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Frontend Pages
    path('', include('laundry.frontend_urls')),

    # API Endpoints
    path('api/', include('laundry.api_urls')),
]
