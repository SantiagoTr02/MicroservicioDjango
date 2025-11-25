# core/api/views/gene_views.py

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from ..models.entities.gene import Gene
from ..models.serializers.gene_serializer import GeneSerializer
from ..services.gene_service import GeneService
from ..models.dto.inDTOCreateGene import InDTOCreateGene
from ..models.dto.inDTOUpdateGene import InDTOUpdateGene
from ..models.dto.outDTOListGene import OutDTOListGene
from ..models.dto.outDTOCreateGene import OutDTOCreateGene
from ..models.dto.outDTOUpdateGene import OutDTOUpdateGene
from ..exceptions.gene_exceptions import (
    FieldNotFilledException,
    InvalidDataFormatException,
    NoFieldsToUpdateException,
    GeneSymbolAlreadyExistsException,
)
from pydantic import ValidationError


class GeneViewSet(viewsets.ModelViewSet):
    queryset = Gene.objects.all()
    serializer_class = GeneSerializer
    @swagger_auto_schema(
        operation_description="Crea un nuevo gen en la base de datos.")

    def create(self, request, *args, **kwargs):
        try:
            gene_data = InDTOCreateGene(**request.data)
            gene_data_dict = gene_data.dict()

            created_gene = GeneService.create_gene(gene_data_dict)

            return Response(
                OutDTOCreateGene.from_orm(created_gene).dict(),
                status=status.HTTP_201_CREATED,
            )

        except FieldNotFilledException as e:
            return Response(
                {"error": "FIELD_NOT_FILLED", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidDataFormatException as e:
            return Response(
                {"error": "INVALID_DATA_FORMAT", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GeneSymbolAlreadyExistsException as e:
            return Response(
                {"error": "GENE_SYMBOL_ALREADY_EXISTS", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                {"error": "VALIDATION_ERROR", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_description="Actualiza un gen en la base de datos.")
    def update(self, request, *args, **kwargs):
        """
        Atualiza un gene existente usando el servicio y maneja excepciones de dominio.
        """
        try:
            gene_data = InDTOUpdateGene(**request.data)
            gene = self.get_object()

            updated_gene = GeneService.update_gene(
                gene,
                gene_data.dict(exclude_unset=True)
            )

            return Response(OutDTOUpdateGene.from_orm(updated_gene).dict())

        except NoFieldsToUpdateException as e:
            return Response(
                {"error": "NO_FIELDS_TO_UPDATE", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except FieldNotFilledException as e:
            return Response(
                {"error": "FIELD_NOT_FILLED", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except InvalidDataFormatException as e:
            return Response(
                {"error": "INVALID_DATA_FORMAT", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except GeneSymbolAlreadyExistsException as e:
            return Response(
                {"error": "GENE_SYMBOL_ALREADY_EXISTS", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except ValidationError as e:
            return Response(
                {"error": "VALIDATION_ERROR", "detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @swagger_auto_schema(
        operation_description="Me lista cada uno de los genes creados en la base de datos.")
    def list(self, request, *args, **kwargs):
        genes = GeneService.list_genes()
        return Response([OutDTOListGene.from_orm(gene).dict() for gene in genes])

    def retrieve(self, request, *args, **kwargs):
        gene = self.get_object()
        return Response(OutDTOListGene.from_orm(gene).dict())


    @swagger_auto_schema(
        operation_description="Elimina a un gen según su ID.")
    def destroy(self, request, *args, **kwargs):
        gene = self.get_object()
        GeneService.delete_gene(gene)

        return Response(
            {
                "message": "Gene deleted successfully",
                "symbol": gene.symbol,
            },
            status=status.HTTP_200_OK,
        )
