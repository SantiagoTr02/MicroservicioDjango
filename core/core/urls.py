"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from drf_yasg.views import get_schema_view
from drf_yasg import openapi



# Configuración para la documentación de Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="Genetic Variants API",
        default_version='v1',
        description="Documentación completa de la API de variantes genéticas",
        terms_of_service="https://www.GeneticVariants",
        contact=openapi.Contact(email="trianacarvajalsantiago@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


# Todas las rutas definidas en genomics_api/urls.py van a vivir bajo el prefijo /genomics/
urlpatterns = [
    # microservicio genómico

    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-docs'),
    path('api/', include('api.urls')),

]
