"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('users/', include('users.urls')),
    path('api/customers/', include('customers.urls')),  

    # Path for API schema generation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # UI Documentation
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

def json_404_view(request, exception=None):
    return JsonResponse({'error': True, 'message': 'Not found'}, status=404)

def json_500_view(request):
    return JsonResponse({'error': True, 'message': 'Internal server error'}, status=500)

handler404 = 'core.urls.json_404_view'
handler500 = 'core.urls.json_500_view'

