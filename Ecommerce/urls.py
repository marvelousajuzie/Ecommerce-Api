from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView 

urlpatterns = [
    path('unique-admin/', admin.site.urls),
    path('api/', include('Ecomapi.urls')),
    path('schema/', SpectacularAPIView.as_view(), name= 'schema'),
    path('', SpectacularSwaggerView.as_view(url_name ='schema'))
]
