from rest_framework import viewsets
from rest_framework.response import Response

from ..models.entities.gene import Gene
from ..models.serializers.gene_serializer import GeneSerializer
from ..services.gene_service import GeneService  # Usamos el servicio
from ..models.dto.inDTOCreateGene import InDTOCreateGene
from ..models.dto.inDTOUpdateGene import InDTOUpdateGene
from ..models.dto.outDTOListGene import OutDTOListGene
from ..models.dto.outDTOCreateGene import OutDTOCreateGene
from ..models.dto.outDTOUpdateGene import OutDTOUpdateGene
from pydantic import ValidationError

class GeneViewSet(viewsets.ModelViewSet):
    # El queryset ya no se utiliza directamente porque ahora vamos a usar el servicio
    queryset = Gene.objects.all()  # Se mantiene por si se usa para búsquedas rápidas
    serializer_class = GeneSerializer

    def create(self, request, *args, **kwargs):
        try:
            # Validar los datos de entrada usando InDTOCreateGene
            gene_data = InDTOCreateGene(**request.data)  # Se valida con el DTO
            gene_data_dict = gene_data.dict()  # Convertimos a un diccionario

            # Usamos GeneService para crear el gene en la base de datos
            created_gene = GeneService.create_gene(gene_data_dict)

            # Devolvemos el gene creado con el OutDTOCreateGene
            return Response(OutDTOCreateGene.from_orm(created_gene).dict(), status=201)
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

    def update(self, request, *args, **kwargs):
        try:
            # Validar los datos de entrada usando InDTOUpdateGene
            gene_data = InDTOUpdateGene(**request.data)  # Validamos los datos con el DTO
            gene = self.get_object()  # Obtener el gene existente de la base de datos

            # Usamos GeneService para actualizar el gene
            updated_gene = GeneService.update_gene(gene, gene_data.dict(exclude_unset=True))

            # Devolvemos el gene actualizado con el OutDTOUpdateGene
            return Response(OutDTOUpdateGene.from_orm(updated_gene).dict())
        except ValidationError as e:
            return Response({"detail": str(e)}, status=400)

    def list(self, request, *args, **kwargs):
        # Obtener todos los genes usando el GeneService
        genes = GeneService.list_genes()

        # Convertir los genes a DTOs de salida (OutDTOListGene)
        return Response([OutDTOListGene.from_orm(gene).dict() for gene in genes])

    def retrieve(self, request, *args, **kwargs):
        # Obtener un gene específico usando el GeneService
        gene = self.get_object()

        # Devolver el gene usando OutDTO
        return Response(OutDTOListGene.from_orm(gene).dict())
