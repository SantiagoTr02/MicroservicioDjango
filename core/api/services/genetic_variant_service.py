from sqlite3 import IntegrityError

from django.core.exceptions import ObjectDoesNotExist
from drf_yasg.openapi import Response
from rest_framework import status

from ..exceptions.genetic_variant_exceptions import GeneticVariantInvalidDataFormatException, \
    GeneticVariantFieldNotFilledException, GeneNotFoundException, GeneticVariantNotFoundException, \
    GeneticVariantDeletionNotAllowedException, GeneticVariantAlreadyExistsException
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
    def create_variant(data: dict):
        """
        Crea una nueva variante genética con validaciones de dominio.
        Espera un dict ya validado por InDTOCreateGeneticVariant.
        """

        gene_id = data.get("geneId")
        chromosome = data.get("chromosome")
        position = data.get("position")
        reference_base = data.get("referenceBase")
        alternate_base = data.get("alternateBase")
        impact = data.get("impact")

        # 1) Campos obligatorios
        if gene_id is None:
            raise GeneticVariantFieldNotFilledException(
                "The field 'geneId' is required."
            )

        if chromosome is None or str(chromosome).strip() == "":
            raise GeneticVariantFieldNotFilledException(
                "The field 'chromosome' is required and cannot be empty."
            )

        if position is None:
            raise GeneticVariantFieldNotFilledException(
                "The field 'position' is required."
            )

        if reference_base is None or str(reference_base).strip() == "":
            raise GeneticVariantFieldNotFilledException(
                "The field 'referenceBase' is required and cannot be empty."
            )

        if alternate_base is None or str(alternate_base).strip() == "":
            raise GeneticVariantFieldNotFilledException(
                "The field 'alternateBase' is required and cannot be empty."
            )

        if impact is None or str(impact).strip() == "":
            raise GeneticVariantFieldNotFilledException(
                "The field 'impact' is required and cannot be empty."
            )

        # 2) Formato de 'position'
        try:
            pos_int = int(position)
            if pos_int <= 0:
                raise GeneticVariantInvalidDataFormatException(
                    "The field 'position' must be a positive integer."
                )
        except (TypeError, ValueError):
            raise GeneticVariantInvalidDataFormatException(
                "The field 'position' must be a valid integer."
            )

        # Guardamos position normalizado en el dict
        data["position"] = pos_int

        # 3) Normalizar strings (trim)
        data["chromosome"] = str(chromosome).strip()
        data["referenceBase"] = str(reference_base).strip()
        data["alternateBase"] = str(alternate_base).strip()
        data["impact"] = str(impact).strip()

        # 4) Validar que el gene exista
        gene = Gene.objects.filter(id=gene_id).first()
        if not gene:
            raise GeneNotFoundException(f"Gene with id {gene_id} does not exist.")

        # 4.5) ✅ Validar que NO exista una variante con exactamente los mismos datos
        already_exists = GeneticVariant.objects.filter(
            geneId=gene,
            chromosome=data["chromosome"],
            position=data["position"],
            referenceBase=data["referenceBase"],
            alternateBase=data["alternateBase"],
            impact=data["impact"],
        ).exists()

        if already_exists:
            raise GeneticVariantAlreadyExistsException(
                "A genetic variant with the same geneId, chromosome, position, "
                "referenceBase, alternateBase and impact already exists."
            )

        # 5) Crear la variante (pasando el objeto Gene, no el id)
        data["geneId"] = gene
        genetic_variant = GeneticVariant.objects.create(**data)
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
    def delete_variant(variant_id: str):
        """
        Elimina una variante genética.
        - Lanza GeneticVariantNotFoundException si no existe.
        - Lanza GeneticVariantDeletionNotAllowedException si hay conflicto de FK.
        """
        try:
            variant = GeneticVariant.objects.get(id=variant_id)
        except GeneticVariant.DoesNotExist:
            raise GeneticVariantNotFoundException(
                f"Genetic variant with id {variant_id} not found."
            )

        try:
            variant.delete()
        except IntegrityError:
            # Esto pasa si la variante está referenciada en patientvariantreport,
            # y la FK no tiene ON DELETE CASCADE.
            raise GeneticVariantDeletionNotAllowedException(
                "This genetic variant cannot be deleted because it is associated "
                "with one or more patient variant reports."
            )