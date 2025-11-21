from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from ..models.entities.genetic_variant import GeneticVariant
from ..models.serializers.genetic_variant_serializer import GeneticVariantSerializer
from ..services.genetic_variant_service import GeneticVariantService
from ..models.dto.inDTOCreateGeneticVariant import InDTOCreateGeneticVariant
from ..models.dto.inDTOUpdateGeneticVariant import InDTOUpdateGeneticVariant
from ..models.dto.outDTOCreateGeneticVariant import OutDTOCreateGeneticVariant
from ..models.dto.outDTOListGeneticVariant import OutDTOListGeneticVariant
from ..models.dto.outDTOUpdateGeneticVariant import OutDTOUpdateGeneticVariant
from pydantic import ValidationError

class GeneticVariantViewSet(viewsets.ModelViewSet):
    queryset = GeneticVariant.objects.all()
    serializer_class = GeneticVariantSerializer

    def create(self, request, *args, **kwargs):
        try:
            variant_data = InDTOCreateGeneticVariant(**request.data)
            variant_data_dict = variant_data.dict()

            created_variant = GeneticVariantService.create_variant(variant_data_dict)
            return Response(OutDTOCreateGeneticVariant.from_orm(created_variant).dict(), status=201)

        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def update(self, request, *args, **kwargs):
        try:
            variant_data = InDTOUpdateGeneticVariant(**request.data)
            variant = self.get_object()

            updated_variant = GeneticVariantService.update_variant(variant, variant_data.dict(exclude_unset=True))
            return Response(OutDTOUpdateGeneticVariant.from_orm(updated_variant).dict())

        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

        except Exception as e:
            return Response({"detail": str(e)}, status=500)

    def list(self, request, *args, **kwargs):
        # Obtener todas las variantes genéticas usando el servicio
        genetic_variants = GeneticVariantService.list_variants()

        # Convertir las variantes genéticas a DTOs de salida
        return Response([OutDTOListGeneticVariant.from_orm(variant).dict() for variant in genetic_variants])

    def retrieve(self, request, *args, **kwargs):
        try:
            variant = self.get_object()
            return Response(OutDTOListGeneticVariant.from_orm(variant).dict())
        except Exception as e:
            return Response({"detail": str(e)}, status=500)
