from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.gene_views import GeneViewSet
from .views.genetic_variant_views import GeneticVariantViewSet

router = DefaultRouter()
# Crea automáticamente todas las rutas REST para estos ViewSets
# GET     /ViewSet/
# POST    /ViewSet/
# GET     /ViewSet/{pk}/
# PUT     /ViewSet/{pk}/
# PATCH   /ViewSet/{pk}/
# DELETE  /ViewSet/{pk}/
router.register(r'gene', GeneViewSet)
router.register(r'genetic-variants', GeneticVariantViewSet)

# Inserta todas las URLs generadas por router dentro de este archivo.
urlpatterns = [
    path('', include(router.urls)),
]