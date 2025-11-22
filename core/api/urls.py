from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.genetic_variant_views import GeneticVariantViewSet, GeneticVariantDetailView

router = DefaultRouter()
router.register(r'genetic-variants', GeneticVariantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Aquí agregamos el endpoint para obtener una variante genética específica
    path('genetic-variants/<uuid:pk>/', GeneticVariantDetailView.as_view(), name='genetic_variant_detail'),
]
