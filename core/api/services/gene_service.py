
from ..models.entities.gene import Gene
from ..exceptions.gene_exceptions import (
    FieldNotFilledException,
    InvalidDataFormatException,
    NoFieldsToUpdateException,
    GeneSymbolAlreadyExistsException,
)
import re


class GeneService:

    @staticmethod
    def list_genes():
        #Obtiene todos los genes de la base de datos
        return Gene.objects.all()

    @staticmethod
    def get_gene(id):
        #Obtiene un gene específico por su id
        return Gene.objects.get(pk=id)

    @staticmethod
    def create_gene(data):

        #Crea un nuevo gene en la base de datos
        symbol = data.get("symbol")
        full_name = data.get("fullName")
        function_summary = data.get("functionSummary")

        #Campos obligatorios
        if symbol is None or str(symbol).strip() == "":
            raise FieldNotFilledException("The field 'symbol' is required and cannot be empty.")

        if full_name is None or str(full_name).strip() == "":
            raise FieldNotFilledException("The field 'fullName' is required and cannot be empty.")

        if function_summary is None or str(function_summary).strip() == "":
            raise FieldNotFilledException("The field 'functionSummary' is required and cannot be empty.")

        #Reglas de formato
        symbol_str = str(symbol).strip()
        if len(symbol_str) < 2:
            raise InvalidDataFormatException("The field 'symbol' must have at least 2 characters.")

        if not re.fullmatch(r"[A-Za-z0-9]+", symbol_str):
            raise InvalidDataFormatException("The field 'symbol' must contain only letters and numbers.")

        if Gene.objects.filter(symbol=symbol_str).exists():
            raise GeneSymbolAlreadyExistsException(f"Symbol '{symbol_str}' is already in use.")

        data["symbol"] = symbol_str  # normalizamos

        # Se crea el gene
        gene = Gene.objects.create(**data)
        return gene

    @staticmethod
    def update_gene(gene, validated_data):

        # Actualiza un gene existente

        # Nada para actualizar
        if not validated_data:
            raise NoFieldsToUpdateException("At least one field must be provided to update.")

        #Valida si symbol viene en el body
        if "symbol" in validated_data:
            symbol = validated_data.get("symbol")

            # Si lo mandan vacío
            if symbol is None or str(symbol).strip() == "":
                raise FieldNotFilledException("The field 'symbol' cannot be empty.")

            symbol_str = str(symbol).strip()

            if len(symbol_str) < 2:
                raise InvalidDataFormatException("The field 'symbol' must have at least 2 characters.")

            if not re.fullmatch(r"[A-Za-z0-9]+", symbol_str):
                raise InvalidDataFormatException("The field 'symbol' must contain only letters and numbers.")

            exists = Gene.objects.filter(symbol=symbol_str).exclude(id=gene.id).exists()
            if exists:
                raise GeneSymbolAlreadyExistsException(f"Symbol '{symbol_str}' is already in use.")

            validated_data["symbol"] = symbol_str

        # Aplicar cambios
        for attr, value in validated_data.items():
            setattr(gene, attr, value)

        gene.save()
        return gene

    @staticmethod
    def delete_gene(gene):
        """Elimina un gene de la base de datos."""
        gene.delete()
