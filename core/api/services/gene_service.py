# core/api/services/gene_service.py

from ..models.entities.gene import Gene
from ..exceptions.gene_exceptions import FieldNotFilledException

class GeneService:

    @staticmethod
    def list_genes():
        """Obtiene todos los genes de la base de datos."""
        return Gene.objects.all()

    @staticmethod
    def get_gene(id):
        """Obtiene un gene específico por su id."""
        return Gene.objects.get(pk=id)

    @staticmethod
    def create_gene(data):
        """Crea un nuevo gene en la base de datos."""
        if not data['symbol']:
            raise FieldNotFilledException("Symbol is required")

        gene = Gene.objects.create(**data)  # Creación del gene en la base de datos
        return gene

    @staticmethod
    def update_gene(gene, validated_data):
        """Actualiza un gene existente."""
        for attr, value in validated_data.items():
            setattr(gene, attr, value)  # Establece el valor de cada campo actualizado
        gene.save()  # Guarda los cambios
        return gene

    @staticmethod
    def delete_gene(gene):
        """Elimina un gene de la base de datos."""
        gene.delete()
