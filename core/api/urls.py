from django.urls import path, include
from rest_framework.routers import DefaultRouter

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.gene_views import GeneViewSet
from .views.genetic_variant_views import GeneticVariantViewSet, GeneticVariantDetailView
from .views.patient_genetic_variant_views import AssignGeneticVariantToPatientView, ListPatientVariantReportsView
from .views.patient_views import CreatePatientView

router = DefaultRouter()
router.register(r'genetic-variants', GeneticVariantViewSet)
router.register(r'gene', GeneViewSet)
urlpatterns = [
    path('', include(router.urls)),
    # Aquí agregamos el endpoint para obtener una variante genética específica
    path('genetic-variants/<uuid:pk>/', GeneticVariantDetailView.as_view(), name='genetic_variant_detail'),
    path('patients/', CreatePatientView.as_view(), name='create_patient'),
    path('assign-genetic-variant/', AssignGeneticVariantToPatientView.as_view(), name='assign_genetic_variant_to_patient'),
    path('patient-variant-reports/', ListPatientVariantReportsView.as_view(), name='patient-variant-reports'),
]
