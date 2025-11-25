from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..exceptions.genetic_variant_exceptions import GeneNotFoundException, GeneticVariantInvalidDataFormatException, \
    GeneticVariantFieldNotFilledException, GeneticVariantDeletionNotAllowedException, GeneticVariantNotFoundException, \
    GeneticVariantAlreadyExistsException
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
        try:
            # 1) Validar input con Pydantic
            dto = InDTOCreateGeneticVariant(**request.data)
            data = dto.dict()

            # 2) Crear usando el servicio (validaciones de dominio)
            created_variant = GeneticVariantService.create_variant(data)

            # 3) Responder con DTO de salida
            return Response(
                OutDTOCreateGeneticVariant.from_orm(created_variant).dict(),
                status=status.HTTP_201_CREATED,
            )

        except GeneticVariantFieldNotFilledException as e:
            return Response(
                {"error": "FIELD_NOT_FILLED", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GeneticVariantInvalidDataFormatException as e:
            return Response(
                {"error": "INVALID_DATA_FORMAT", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GeneNotFoundException as e:
            return Response(
                {"error": "GENE_NOT_FOUND", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GeneticVariantAlreadyExistsException as e:
            return Response(
                {"error": "GENETIC_VARIANT_ALREADY_EXISTS", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            # Errores de Pydantic (tipos, campos faltantes, etc.)
            return Response(
                {"error": "VALIDATION_ERROR", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
        """
        Elimina una variante genética usando su ID (UUID)
        y devuelve mensajes bonitos.
        """
        variant_id = kwargs.get("pk")

        try:
            GeneticVariantService.delete_variant(variant_id)

            return Response(
                {
                    "message": "Genetic variant deleted successfully",
                    "id": variant_id,
                },
                status=status.HTTP_200_OK,
            )

        except GeneticVariantNotFoundException as e:
            return Response(
                {
                    "error": "GENETIC_VARIANT_NOT_FOUND",
                    "detail": str(e),
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except GeneticVariantDeletionNotAllowedException as e:
            return Response(
                {
                    "error": "GENETIC_VARIANT_DELETION_NOT_ALLOWED",
                    "detail": str(e),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


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