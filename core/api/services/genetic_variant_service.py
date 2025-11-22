from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.openapi import Response
from rest_framework import status

from ..models.entities.genetic_variant import GeneticVariant
from ..models.entities.gene import Gene  # Asegúrate de importar la entidad Gene
from ..models.serializers.genetic_variant_serializer import GeneticVariantSerializer


class GeneticVariantService:

    @staticmethod
    def list_variants():
        """Obtiene todas las variantes genéticas de la base de datos."""
        return GeneticVariant.objects.all()

    @staticmethod
    def get_variant_by_id(variant_id: str):
        """Obtiene una variante genética por su UUID."""
        try:
            # Buscar la variante genética por UUID
            variant = GeneticVariant.objects.get(id=variant_id)
            return variant
        except GeneticVariant.DoesNotExist:
            return None

    @staticmethod
    def create_variant(data):
        """Crea una nueva variante genética en la base de datos."""
        gene_id = data.get('geneId')

        # Verificar si el geneId es válido y si existe en la base de datos
        gene = Gene.objects.filter(id=gene_id).first()  # Usamos .filter().first() para obtener el gene si existe

        if not gene:
            # Si el geneId no está en la base de datos, retornamos un error
            return {"error": f"Gene with id {gene_id} does not exist"}, 400

        # Ahora, en lugar de pasar solo el geneId como ID, asignamos el objeto gene completo
        data['geneId'] = gene  # Asignamos el objeto completo de Gene

        # Si el geneId existe, entonces podemos proceder a crear la variante genética
        genetic_variant = GeneticVariant.objects.create(**data)  # Creación de la variante genética
        return genetic_variant

    @staticmethod
    def update_variant(variant_id, data):
        """Actualiza una variante genética por su ID (UUID)."""
        try:
            # Obtener la variante genética existente
            variant = GeneticVariant.objects.get(id=variant_id)

            # Si se especifica un nuevo geneId, actualizamos el geneId de la variante
            if data.get('geneId') is not None:
                new_gene_id = data['geneId']  # Solo el ID del nuevo Gene
                new_gene = Gene.objects.get(id=new_gene_id)
                variant.geneId = new_gene  # Actualizamos el geneId con el nuevo Gene

            # Actualizar solo los campos presentes en 'data', ignorando valores None
            if 'chromosome' in data:
                variant.chromosome = data['chromosome']
            if 'position' in data:
                variant.position = data['position']
            if 'referenceBase' in data:
                variant.referenceBase = data['referenceBase']
            if 'alternateBase' in data:
                variant.alternateBase = data['alternateBase']
            if 'impact' in data:
                variant.impact = data['impact']  # Solo actualizamos impact si está presente en el JSON

            # Guardamos la variante genética actualizada
            variant.save()

            # Convertimos geneId a diccionario con la información relevante del Gene
            gene_data = {
                "id": variant.geneId.id,
                "symbol": variant.geneId.symbol,
                "fullName": variant.geneId.fullName,
                "functionSummary": variant.geneId.functionSummary,
            }

            # Devolvemos la variante actualizada con el geneId como diccionario
            return {
                "id": variant.id,
                "geneId": gene_data,  # Solo los datos del Gene en un diccionario
                "chromosome": variant.chromosome,
                "position": variant.position,
                "referenceBase": variant.referenceBase,
                "alternateBase": variant.alternateBase,
                "impact": variant.impact,
            }

        except ObjectDoesNotExist:
            return {"error": "Genetic variant not found."}, 404  # Si la variante no existe

    @staticmethod
    def delete_variant(variant_id):
        """Elimina una variante genética de la base de datos por su ID (UUID)."""
        try:
            variant = GeneticVariant.objects.get(id=variant_id)  # Buscamos la variante por su ID
            variant.delete()  # Eliminamos la variante genética
            return {"message": "Genetic variant deleted successfully."}, 204  # Devolvemos un mensaje de éxito
        except ObjectDoesNotExist:
            return {"error": "Genetic variant not found."}, 404  # Si no se encuentra la variante, devolvemos un error 404
