from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.dto.inDTOUpdateGeneticVariant import InDTOUpdateGeneticVariant
from ..models.dto.outDTOGetSpecificGeneticVariant import OutDTOGetSpecificGeneticVariant
from ..models.dto.outDTOListGeneticVariant import OutDTOListGeneticVariant
from ..models.dto.outDTOUpdateGeneticVariant import OutDTOUpdateGeneticVariant
from ..models.entities.genetic_variant import GeneticVariant
from ..models.serializers.genetic_variant_serializer import GeneticVariantSerializer
from ..services.genetic_variant_service import GeneticVariantService
from ..models.dto.inDTOCreateGeneticVariant import InDTOCreateGeneticVariant
from ..models.dto.outDTOCreateGeneticVariant import OutDTOCreateGeneticVariant
from pydantic import ValidationError

class GeneticVariantViewSet(viewsets.ModelViewSet):
    queryset = GeneticVariant.objects.all()
    serializer_class = GeneticVariantSerializer

    def create(self, request, *args, **kwargs):
        # Obtenemos los datos de la solicitud
        variant_data = request.data

        # Usamos el servicio para crear la variante genética
        result = GeneticVariantService.create_variant(variant_data)

        if isinstance(result, tuple) and result[1] == 400:  # Si es un error, devolvemos el mensaje de error
            return Response(result[0], status=status.HTTP_400_BAD_REQUEST)

        # Si la creación fue exitosa, devolvemos solo los detalles básicos de la variante
        return Response(OutDTOCreateGeneticVariant.from_orm(result).dict(), status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        variants = GeneticVariantService.list_variants()  # Obtenemos todas las variantes

        # Convertimos las variantes en el formato esperado del DTO
        return Response([OutDTOListGeneticVariant.from_orm(variant).dict() for variant in variants])

    def update(self, request, *args, **kwargs):
        variant_id = kwargs.get('pk')  # Extraemos el ID de la variante desde la URL

        # Validamos los datos de entrada usando InDTOUpdateGeneticVariant
        variant_data = InDTOUpdateGeneticVariant(**request.data)

        # Usamos el servicio para actualizar la variante genética
        updated_variant = GeneticVariantService.update_variant(variant_id, variant_data.dict())

        if isinstance(updated_variant, tuple) and updated_variant[1] == 404:  # Si no se encuentra la variante
            return Response(updated_variant[0], status=status.HTTP_404_NOT_FOUND)

        # Si la actualización fue exitosa, devolvemos la variante actualizada con el Gene completo
        return Response(updated_variant, status=status.HTTP_200_OK)


    def destroy(self, request, *args, **kwargs):
        """Elimina una variante genética usando su ID (UUID)."""
        variant_id = kwargs.get('pk')  # Extraemos el ID de la variante desde la URL

        result, http_status = GeneticVariantService.delete_variant(variant_id)

        return Response(result, status=http_status)


class GeneticVariantDetailView(APIView):
    """Vista para obtener una variante genética específica por su UUID."""

    def get(self, request, pk, *args, **kwargs):
        # Usamos el servicio para obtener la variante genética por su UUID
        variant = GeneticVariantService.get_variant_by_id(pk)

        if variant is None:
            # Si la variante no existe, devolvemos un error 404
            return Response({"detail": "Genetic variant not found."}, status=status.HTTP_404_NOT_FOUND)

        # Si la variante existe, la serializamos con el DTO de salida
        response_data = OutDTOGetSpecificGeneticVariant(
            id=variant.id,
            geneId={
                "id": variant.geneId.id,
                "symbol": variant.geneId.symbol,
                "fullName": variant.geneId.fullName,
                "functionSummary": variant.geneId.functionSummary
            },
            chromosome=variant.chromosome,
            position=variant.position,
            referenceBase=variant.referenceBase,
            alternateBase=variant.alternateBase,
            impact=variant.impact
        )

        # Devolvemos la variante con el formato adecuado
        return Response(response_data.dict(), status=status.HTTP_200_OK)