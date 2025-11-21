from ..models.entities.gene import Gene
from ..models.entities.genetic_variant import GeneticVariant

class GeneticVariantService:

    @staticmethod
    def list_variants():
        return GeneticVariant.objects.all()

    @staticmethod
    def create_variant(data):
        gene_id = data.get("geneId_id")  # Aseguramos que es el ID de Gene que se recibe en el JSON

        try:
            # Buscamos la instancia de Gene usando el ID proporcionado
            gene = Gene.objects.get(id=gene_id)
        except Gene.DoesNotExist:
            raise ValueError(f"Gene with id {gene_id} not found")

        # Ahora pasamos la instancia de Gene a la creación de GeneticVariant
        genetic_variant = GeneticVariant.objects.create(
            geneId=gene,  # Aseguramos que aquí se pasa la instancia de Gene
            chromosome=data["chromosome"],
            position=data["position"],
            referenceBase=data["referenceBase"],
            alternateBase=data["alternateBase"],
            impact=data["impact"]
        )
        return genetic_variant

    @staticmethod
    def update_variant(variant, validated_data):
        for attr, value in validated_data.items():
            setattr(variant, attr, value)
        variant.save()
        return variant

    @staticmethod
    def delete_variant(variant):
        variant.delete()
