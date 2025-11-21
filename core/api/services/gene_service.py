# core/api/services/gene_service.py
from core.api.exceptions.gene_exceptions import FieldNotFilledException
from core.api.models.entities.gene import Gene
class GeneService:

    @staticmethod
    def list_genes():
        return Gene.objects.all()

    @staticmethod
    def get_gene(id):
        return Gene.objects.get(pk=id)

    @staticmethod
    def create_gene(data):
        symbol = data.get("symbol")
        full_name = data.get("fullName")
        function_summary = data.get("functionSummary")

        if not symbol or symbol.strip() == "":
            raise FieldNotFilledException("symbol is required")

        if not full_name or full_name.strip() == "":
            raise FieldNotFilledException("fullName is required")

        if not function_summary or function_summary.strip() == "":
            raise FieldNotFilledException("functionSummary is required")

        return Gene.objects.create(**data)

    @staticmethod
    def update_gene(instance, validated_data):
        symbol = validated_data.get("symbol")
        fullName = validated_data.get("fullName")
        functionSummary = validated_data.get("functionSummary")

        if not symbol or symbol.strip() == "":
            raise FieldNotFilledException("symbol is required")

        if not fullName or fullName.strip() == "":
            raise FieldNotFilledException("fullName is required")

        if not functionSummary or functionSummary.strip() == "":
            raise FieldNotFilledException("functionSummary is required")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    @staticmethod
    def delete_gene(instance):
        instance.delete()
